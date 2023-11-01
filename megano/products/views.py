from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import ProductSerializer
from .models import Product


class ProductDetail(APIView):
    def get(self, request: Request, pk):
        product = Product.objects.get(pk=pk)
        serialized = ProductSerializer(product, many=False)
        return Response(serialized.data)
