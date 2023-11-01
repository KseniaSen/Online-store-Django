from django.contrib import admin

from .models import Avatar, Profile


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
    ordering = ['pk']


class IconInline(admin.StackedInline):
    model = Avatar
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'phone']
    inlines = [IconInline]
    ordering = ['pk']
