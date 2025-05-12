import os
import tensorflow as tf
import numpy as np
import torch
from PIL import Image
from torchvision import models
import albumentations as A
from albumentations.pytorch import ToTensorV2
 
 

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from keras.models import load_model
from api.common.services.ollama.deepseek import image_classification_response


 
 


# 🧠 Set class names from your training
class_names = ['Healthy', 'Powdery Mildew', 'Rust']

# ✅ Load model globally
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'plant_disease_model.pt')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model, device

model, device = load_model()


# ✅ Prediction Function
def predict_image(image_path):
    transform = A.Compose([
        A.Resize(128, 128),
        ToTensorV2()
    ])
    image = np.array(Image.open(image_path).convert("RGB"), dtype=np.float32)
    transformed = transform(image=image)
    tensor = transformed['image'].unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        pred_idx = torch.argmax(outputs, dim=1).item()
        pred_class = class_names[pred_idx]
        confidence = torch.nn.functional.softmax(outputs, dim=1)[0][pred_idx].item()
    return pred_class, confidence


# ✅ API View
class ImageDiseaseView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('image')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded image
        fs = FileSystemStorage(location='upload/')
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        try:
            prediction, confidence = predict_image(file_path)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        return Response({
            'leaf_condition': prediction,
            'confidence': f"{confidence * 100:.2f}%"
        }, status=status.HTTP_200_OK)