from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Order."""
    list_display = ['pk', 'user', 'createdAt', 'totalCost', 'city', 'status']
    list_display_links = ['pk', 'user']
    ordering = ['pk']
