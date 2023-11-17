from rest_framework import serializers 
from django.contrib.auth.models import User
from .models import Profile, Avatar


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Avatar."""
    class Meta:
        model = Avatar
        fields = ['src', 'alt']


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Profile."""
    avatar = AvatarSerializer(many=False, required=False)
    
    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ['username', 'password']
