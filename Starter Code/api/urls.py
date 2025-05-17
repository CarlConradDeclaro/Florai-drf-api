from django.urls import path
from .views import MyTokenObtainPairView,RegisterView,ProfileView, getRoutes,chatbot_flor2,plant_info,semantic_search_view,chatbot_flor
from rest_framework_simplejwt.views import (TokenRefreshView,)
from .views.image_classification import ImageClassificationView,predicted_image
from .views.plant_disease import ImageDiseaseView


urlpatterns = [
    path('', getRoutes,name="routes"),
    path('plants/',plant_info),
    path('plants/search/',semantic_search_view),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/',ProfileView.as_view(),name="profile_view"),
 
    path('ai-deepseek2/',chatbot_flor2,name='deepseek2'),
    path('ai-deepseek2_json/',chatbot_flor,name='deepseek2'),

    path('classify/', ImageClassificationView.as_view(), name='classify-image'),
    path('predicted_image_details/', predicted_image, name='predicted_image'),
    path('plant_disease/', ImageDiseaseView.as_view(), name='plant_disease'),

]
