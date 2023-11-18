from decimal import Decimal
from typing import Dict, List

from rest_framework import serializers

from products.models import Product


class BasketSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины покупок."""
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_count(self, obj: Product) -> int:
        """Функция для возвращения количества товаров в корзине."""

        return self.context.get(str(obj.pk)).get('count')

    def get_price(self, obj: Product) -> Decimal:
        """Функция для возвращения цены товара в корзине."""
        return Decimal(self.context.get(str(obj.pk)).get('price'))

    def get_images(self, instance: Product) -> List[Dict[str, str]]:
        """Функция для возвращения списка изображений товара."""
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({"src": f"/media{image.__str__()}", "alt": image.name})
        return images
