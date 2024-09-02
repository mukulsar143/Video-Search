from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

# Create your views here.

# Register Users API


class Register(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserRegister(data = data)
            if serializer.is_valid():
                serializer.save()    
                return Response({'message' : serializer.data, 'success' : True})
            
                    
            return Response({ 
                'status' : 400, 
                'success' : False,
                'message' : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)  
         
        except Exception as e:
            print(e)
            return Response({
                'status' : 500,
                'message' : 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
            

# Login Users API            
            
class Login(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginUser(data = data)
            if serializer.is_valid():
                response = serializer.get_token(data)
                return Response(response, status=status.HTTP_201_CREATED)  
                
            return Response({
                'status' : 400, 
                'message' : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)   
        
        except Exception as e:
            print(e)
            return Response({
                'status' : 500,
                'message' : 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
                                