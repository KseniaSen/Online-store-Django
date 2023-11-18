from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from cart.cart import Cart
from .models import Order, ProductOrder
from orders.serializers import OrderSerializer, OrderIdSerializer
from products.models import Product
from products.serializers import ProductSerializer


class Orders(APIView):
    """Api для добавления товаров в заказ"""

    serializer_class = OrderSerializer

    @extend_schema(
        request=ProductSerializer,
        responses={
            status.HTTP_200_OK: OrderIdSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description="unsuccessful operation"
                ),
        },
    )

    def post(self, request: Request, *args, **kwargs) -> Response:
        products_in_order = [(obj["id"], obj["count"], obj["price"]) for obj in request.data]
        products = Product.objects.filter(id__in=[obj[0] for obj in products_in_order])
        if str(request.user) == 'AnonymousUser':
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        order = Order.objects.create(
            user=request.user.profile,
            totalCost=Cart(request).total_price(),
        )
        data = {
            "orderId": order.pk,
        }
        order.products.set(products)
        order.save()
        return Response(data, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        data = Order.objects.filter(user_id=request.user.profile.pk)
        serialized = OrderSerializer(data, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class OrderDetail(APIView):
    """Api для получения и оформления заказа"""

    serializer_class = OrderSerializer

    def get(self, request: Request, pk) -> Response:
        """Функция для получения заказа."""
        data = Order.objects.get(pk=pk)
        serialized = OrderSerializer(data)
        cart = Cart(request).cart
        data = serialized.data

        try:
            products_in_order = data['products']
            query = ProductOrder.objects.filter(order_id=pk)
            prods = {obj.product.pk: obj.count for obj in query}
            for prod in products_in_order:
                prod['count'] = prods[prod['id']]
        except:
            products_in_order = data['products']
            for prod in products_in_order:
                prod['count'] = cart[str(prod['id'])]['count']
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=None,
                description="successful creation"
            ),
        }
    )

    def post(self, request: Request, pk) -> Response:
        """Функция для оформления заказаза."""
        order = Order.objects.get(pk=pk)
        data = request.data
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        order.deliveryType = data['deliveryType']
        order.city = data['city']
        order.address = data['address']
        order.paymentType = data['paymentType']
        order.status = 'Ожидает оплаты'
        if data['deliveryType'] == 'express':
            order.totalCost += 500
        else:
            if order.totalCost < 2000:
                order.totalCost += 200

        for product in data['products']:
            ProductOrder.objects.get_or_create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count']
            )

        order.save()
        Cart(request).clear()
        return Response(request.data, status=status.HTTP_201_CREATED)


class PaymentView(APIView):
    """Api для оплаты заказа"""

    @extend_schema(
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=None,
                description="successful operation"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="unsuccessful operation"
            ),
        },
        examples=[
            OpenApiExample(
                "Post example",
                description="Test example for the post",
                value=
                {
                    "number": "9999999999999999",
                    "name": "Ivan Ivanov",
                    "month": "03",
                    "year": "2026",
                    "code": "123"
                },
                status_codes=[str(status.HTTP_200_OK)],
            ),
        ],
    )

    def post(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        if int(request.data['number']) % 2 == 0 and int(request.data['number']) % 10 != 0:
            order.status = 'Оплачен'
            order.save()
            return Response(status=status.HTTP_200_OK)
        else:
            order.status = 'Ошибка при оплате'
            order.save()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
