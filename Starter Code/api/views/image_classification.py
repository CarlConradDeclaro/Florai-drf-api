import os
import tensorflow as tf
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from keras.models import load_model
from api.common.services.ollama.deepseek import image_classification_response

 
model_path = os.path.join(settings.BASE_DIR, 'Flower_Recog_Model.h5')
model = load_model(model_path)


class ImageClassificationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
     
        file = request.FILES.get('image')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage(location='upload/')
        filename = fs.save(file.name, file)
        file_path = fs.path(filename) 

     
        outcome = self.classify_image(file_path)
        print("result is:", outcome)
    
        if os.path.exists(file_path):
            os.remove(file_path)

        return Response({'flower_name': outcome['flower_name'] , 'confidence':outcome['confidence']}, status=status.HTTP_200_OK)

    def classify_image(self, file_path):
        input_image = tf.keras.utils.load_img(file_path, target_size=(180, 180))
        input_image_array = tf.keras.utils.img_to_array(input_image)
        input_image_exp_dim = tf.expand_dims(input_image_array, 0)

        prediction = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(prediction[0])

        predicted_class = np.argmax(result)
        confidence = np.max(result)

        flower_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

        return  {
            'flower_name': flower_names[predicted_class],
            'confidence': f"{confidence * 100:.2f}%"
        }

@api_view(["POST"])
def predicted_image(request):
    data = request.data

    prompt = data.get("prompt",[])
    print("the prompt",prompt)
    user_prompt =  image_classification_response(prompt)
    if(user_prompt):
        print("response: ", user_prompt)
    return Response(user_prompt)
