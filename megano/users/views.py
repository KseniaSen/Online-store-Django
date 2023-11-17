import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Profile, Avatar, User
from .serializers import ProfileSerializer, UserSerializer


class ProfileDetail(APIView):
    """API для получения и изменения профиля пользователя."""

    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        """Получение профиля пользователя."""
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        serialized = ProfileSerializer(profile, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Изменение данных профиля пользователя."""
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        profile.fullName = request.data.get('fullName')
        profile.phone = request.data.get('phone')
        profile.email = request.data.get('email')
        profile.save()
        serialized = ProfileSerializer(profile, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
    """Api для изменения пароля"""

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description="successful operation"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description="Bad Request"
            ),
        }
    )

    def post(self, request: Request) -> Response:
        user = request.user

        if not user.check_password(request.data.get("currentPassword")):
            return Response({"passwordCurrent": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get("newPassword") == request.data.get("currentPassword"):
            return Response({'password': ['Passwords ']}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data.get('newPassword'))
        user.save()
        try:
            user = authenticate(username=user.username, password=user.password)
            login(request, user)
        except Exception as e:
            pass

        return Response(status=status.HTTP_200_OK)


class AvatarUpdateView(APIView):
    """Api для изменения аватарки"""

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description="successful operation"
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=None,
                description="Bad Request"
            ),
        }
    )

    def post(self, request: Request) -> Response:
        new_avatar = request.data.get('avatar')
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        avatar, created = Avatar.objects.get_or_create(profile_id=profile.pk)

        if str(new_avatar).endswith(('.png', '.jpg', '.jpeg', '.jpg.webp')):
            avatar.image = new_avatar
            avatar.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class SingInView(APIView):
    """Api для входа на сайт"""

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description="successful operation"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="unsuccessful operation"
            ),
        }
    )

    def post(self, request: Request) -> Response:

        data = json.loads(list(request.data.keys())[0])
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class SingOutView(APIView):
    """Api для выхода с сайта"""

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description="successful operation"
            ),
        }
    )

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SingUpView(APIView):
    """Api для регистрации на сайте"""

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=None,
                description="successful creation"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="unsuccessful operation"
            ),
        }
    )

    def post(self, request: Request) -> Response:
        data = json.loads(list(request.data.keys())[0])
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            name = data.get('name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.create_user(username=username, password=password, first_name=name)
                user.save()
                Profile.objects.create(user=user, fullName=name)
                user = authenticate(username=username, password=password)
                login(request, user)
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
