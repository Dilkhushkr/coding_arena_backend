from django.shortcuts import render

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

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
        remember_me = request.data.get('remember_me')

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
        
        if remember_me:
            refresh_max_age = 7 * 24 * 60 * 60  
        else:
            refresh_max_age = 24 * 60 * 60

        response.set_cookie(
            key="access_token",
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite="None",
            max_age=15*60
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite="None",
            max_age=refresh_max_age
        )
        return response

class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return Response(
                {"error" : "Authentication credentials were not Provided "},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            access = AccessToken(token)
            user_id = access.get("user_id")
            user = User.objects.get(id=user_id)

        except Exception :
            return Response(
                {"error" : "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = {
            "email" : user.email,
            "name" : user.name,
            "rank" : user.rank,
            "wins" : user.wins,
            "losses" : user.losses
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        response = Response({"message" : "Logout successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class CheckAuthView(APIView):
    def get(self, request):
        token = request.COOKIES.get("access_token")
        print('Check Auth Token :', token)
        if not token:
            return Response(
                {"isAuthenticated": False},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            access = AccessToken(token)
            return Response(
                {"isAuthenticated": True},
                status=status.HTTP_200_OK
            )
        except Exception: 
            return Response(
                {"isAuthenticated": False},
                status=status.HTTP_401_UNAUTHORIZED
            )


