import datetime

from rest_framework import serializers
from orders.models import Order
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Order."""
    createdAt = serializers.SerializerMethodField()
    fullName = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    phone = serializers.StringRelatedField()
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def get_createdAt(self, instance: Order)  -> str:
        """Функция возвращает дату создания заказа в формате '%d.%m.%Y %H:%M'."""
        date = instance.createdAt + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')

class OrderIdSerializer(serializers.Serializer):
    """Сериализатор для Order id"""
    orderId = serializers.IntegerField()
