from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiRequest, OpenApiParameter
from rest_framework import serializers

from cart.cart import Cart
from cart.serializers import BasketSerializer
from products.models import Product


def get_products(cart: Cart) -> BasketSerializer:
    """Функция для получения товаров в корзине"""
    products_in_cart = [product for product in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_in_cart)
    serializer = BasketSerializer(products, many=True, context=cart.cart)
    return serializer
class OrderIdSerialize(serializers.Serializer):
    """Сериализатор для Order id"""
    id = serializers.IntegerField()
    count = serializers.IntegerField()

class BasketView(APIView):
    """Api для получения, добавления, удаления товаров в корзине"""

    serializer_class = BasketSerializer

    def get(self, *args, **kwargs) -> Response:
        """Функция для получения списока товаров в корзине."""

        cart = Cart(self.request)
        serializer = get_products(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=serializer_class,
                description="successful operation"
            ),
        },
        examples=[
            OpenApiExample(
                "Post example",

                description="Test example for the post",
                value=
                {
                    "id": 1,
                    "count": 5
                },

                status_codes=[""],
            ),
        ],
    )


    def post(self, *args, **kwargs) -> Response:
        """Функция для добавления товара в корзину."""

        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        cart.add(product=product, count=self.request.data.get('count'))
        serializer = get_products(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(

        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                response=serializer_class,
                description="successful operation"
            ),
        },
    )

    def delete(self, *args, **kwargs) -> Response:
        """Функция для удаления товара в корзине"""

        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        count = self.request.data.get('count', False)
        cart.remove(product, count=count)
        serializer = get_products(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
