from django.urls import path
from .views import MyTokenObtainPairView,RegisterView,getRoutes,mistral,phi,deepseek,deepseek2,plant_info,semantic_search_view
from rest_framework_simplejwt.views import (TokenRefreshView,)
urlpatterns = [
    path('', getRoutes,name="routes"),
    path('plants/',plant_info),
    path('plants/search/',semantic_search_view),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
 
    path('ai-mistral/',mistral,name='mistral'),
    path('ai-phi/',phi,name='phi'),
    path('ai-deepseek/',deepseek,name='deepseek'),
    path('ai-deepseek2/',deepseek2,name='deepseek2')

]
