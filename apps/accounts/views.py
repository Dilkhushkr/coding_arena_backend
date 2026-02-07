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
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail




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

class ForgotPasswordView(APIView):
    def post(self,request):
        email = request.data.get("email")

        if not email:
            return Response(

                {'error' : 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user  = User.objects.filter(email = email).first()
        if user : 
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_decode(force_bytes(user.pk))
            resset_link = f"http://frontend-app.com/reset-password/{uid}/{token}"

            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {resset_link}",
                from_email=None,
                recipient_list=[email],
                fail_silently=True
            )

        return Response(
            {'message' : 'If an account with that email exists, a password reset link has been sent.'},
            status=status.HTTP_200_OK
        )
    

class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {'error' : 'New password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {'message' : 'Password reset successful'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error' : 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )


