from django.shortcuts import render

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)
    return {
        "refresh" : str(refresh),
        "access" : str(refresh.access_token),
    }

def home(request):
    return HttpResponse("Welcome to Coding Arena Backend 🚀")

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    def post(self,request):

        email = request.data.get("email")
        password  = request.data.get('password')

        user =  authenticate(username = email,password = password)

        if user is None:
           return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        tokens = get_tokens_for_user(user)

        print('Token :', tokens)

        response = Response(
            {"message" : "Login successfull"},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite="None"
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite="None"

        )

        return response
