from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .messages import messages
from .validations.auth import LoginValidator, RegisterValidator


class RegisterUser(APIView):
    def post(self, request):
        validator = RegisterValidator(data=request.data)
        if not validator.is_valid():
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": messages["VALIDATION_ERROR"],
                    "data": validator.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializer(data=validator.validated_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": messages["USER_CREATED"],
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": messages["VALIDATION_ERROR"],
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginUser(APIView):
    def post(self, request):
        validator = LoginValidator(data=request.data)
        if not validator.is_valid():
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": messages["VALIDATION_ERROR"],
                    "data": validator.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = validator.validated_data["email"]
        password = validator.validated_data["password"]

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": messages["LOGIN_SUCCESS"],
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": messages["LOGIN_FAILED"],
                "data": None,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
