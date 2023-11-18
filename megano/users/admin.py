from django.contrib import admin

from .models import Avatar, Profile


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Avatar."""
    list_display = ['pk', '__str__']
    ordering = ['pk']


class IconInline(admin.StackedInline):
    """Класс для отображения изображений Avatar в админке профиля."""
    model = Avatar
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Profile."""
    list_display = ['pk', 'user', 'fullName', 'phone', 'email']
    inlines = [IconInline]
    ordering = ['pk']
