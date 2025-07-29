from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import RegistrationSerializer, LoginSerializer
from config.responses import APIResponse

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return APIResponse(
                    status=status.HTTP_201_CREATED,
                    data={
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    message="User registered successfully",
                )
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="User registration failed",
                errors=serializer.errors,
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                errors={"detail": str(e)},
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                access_token = AccessToken.for_user(user)
                return APIResponse(
                    status=status.HTTP_200_OK,
                    message="User logged in successfully",
                    data={
                        "type": "Bearer",
                        "access_token": str(access_token),
                    },
                )
            return APIResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="User login failed",
                errors=serializer.errors,
            )
        except Exception as e:
            return APIResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                errors={"detail": str(e)},
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        return APIResponse(
            status=status.HTTP_200_OK,
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            message="User profile retrieved successfully",
        )