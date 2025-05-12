 
from api.models import User
from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class ProfileView(APIView):
    permission_classes =  [IsAuthenticated]


    def get(self,request):
        serializers = UserSerializer(request.user)
        return Response(serializers.data)
    
    def put(self,request):
        serializers = UserSerializer(request.user,data =request.data,partial=true)
        if serializers.is_valid:
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)