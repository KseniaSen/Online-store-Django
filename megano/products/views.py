from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count
from datetime import datetime, date
from urllib.parse import unquote

from .serializers import ProductSerializer, TagsProductSerializer, CategoriesSerializer, ReviewSerializer, \
    SaleSerializer, ProductListSerializer
from .models import Product, Tag, Category, Review, Sale


class ProductDetail(APIView):
    """Api для получения продукта по id"""
    def get(self, request: Request, pk) -> Response:
        product = Product.objects.get(pk=pk)
        serialized = ProductSerializer(product, many=False)
        return Response(serialized.data)


class TagsList(APIView):
    """Api для получения списка tags"""
    def get(self, request: Request) -> Response:
        category_pk = request.GET.get('category')
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            tags = category.tags.all()
        else:
            tags = Tag.objects.all()
        data = TagsProductSerializer(tags, many=True)
        return Response(data.data)


class CategoryList(APIView):
    """Api для получения списка categories"""
    def get(self, request: Request) -> Response:
        categories = Category.objects.filter(parent=None)
        data = CategoriesSerializer(categories, many=True)
        return Response(data.data)


class BannersList(APIView):
    """Api для получения списка продуктов для баннера"""
    def get(self, request: Request) -> Response:
        categories_favourite = Category.objects.filter(favourite=True)[:3]
        banners = []

        for category in categories_favourite:
            random_product = Product.objects.filter(category=category).order_by('?').first()
            if random_product:
                banners.append(random_product)

        serialized = ProductListSerializer(banners, many=True)
        return Response(serialized.data)


class LimitedList(APIView):
    """Api для получения списка продуктов c ограниченным тиражом"""
    def get(self, request: Request):
        products = Product.objects.filter(limited=True)[:16]
        serialized = ProductListSerializer(products, many=True)
        return Response(serialized.data)


class PopularList(APIView):
    """Api для получения списка популярных продуктов"""
    def get(self, request: Request):
        products = Product.objects.filter(active=True).annotate(
            count_reviews=Count('reviews')).order_by('-count_reviews')[:8]
        serialized = ProductListSerializer(products, many=True)
        return Response(serialized.data)


class ReviewCreateView(APIView):
    """Api для добавления нового отзыва"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        request.data['product'] = product.pk
        request.data['date'] = datetime.now()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product = serializer.instance.product
            product.update_rating()
            reviews = Review.objects.filter(product=pk)
            serialized = ReviewSerializer(reviews, many=True)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesList(APIView):
    """Api для получения списка продуктов cо скидками"""
    def get(self, request: Request):
        today = date.today()
        sales = Sale.objects.filter(dateFrom__lte=today, dateTo__gte=today).order_by('dateFrom')
        paginator = Paginator(sales, 4)
        page_number = request.GET.get('currentPage', 1)
        current_page = paginator.page(page_number)
        serialized = SaleSerializer(current_page, many=True)
        return Response({'items': serialized.data, 'currentPage': current_page.number,
                         'lastPage': paginator.num_pages})


def filter_products(request):
    """Функция для фильтрации списка продуктов"""
    name = request.query_params.get('filter[name]')
    min_price = request.query_params.get('filter[minPrice]')
    max_price = request.query_params.get('filter[maxPrice]')
    free_delivery = request.query_params.get('filter[freeDelivery]')
    available = request.query_params.get('filter[available]')
    category_id = request.GET.get('category')
    tags = request.query_params.getlist('tags[]')
    try:
        filter_catalog = str(request.META['HTTP_REFERER'].split('/')[4])
        if filter_catalog.startswith('?filter=') and not name:
            name = unquote(str(filter_catalog).split('=')[1])
    except:
        pass

    products = Product.objects.all()

    if category_id:
        categories = [obj.pk for obj in Category.objects.filter(parent_id=category_id)]
        categories.append(int(category_id))
        products = products.filter(category_id__in=categories)

    if tags:
        products = products.filter(tags__in=tags)

    if name:
        products = products.filter(title__icontains=name)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if free_delivery is not None:
        if free_delivery == 'true':
            products = products.filter(freeDelivery=True)

    if available is not None:
        if available == 'true':
            products = products.filter(active=True)

    return products


def sort_products(request, products):
    """Функция для сортировки списка продуктов"""
    products = products.annotate(num_reviews=Count('reviews'))
    sort_by = request.GET.get('sort', 'pk')
    sort_type = request.GET.get('sortType', 'inc')

    if sort_by == 'reviews':
        if sort_type == 'inc':
            products = products.order_by('num_reviews')
        elif sort_type == 'dec':
            products = products.order_by('-num_reviews')
    elif sort_type == 'inc':
        products = products.order_by(sort_by)
    elif sort_type == 'dec':
        products = products.order_by(f'-{sort_by}')

    return products


class ProductListView(APIView):
    """Api для получения списка продуктов для каталога"""
    def get(self, request, *args, **kwargs):

        products = filter_products(request)
        products = sort_products(request, products)

        paginator = Paginator(products, int(request.GET.get('limit', 20)))
        page_number = request.GET.get('currentPage', 1)
        paginated_queryset = paginator.page(page_number)

        serializer = ProductListSerializer(paginated_queryset, many=True)

        return Response({"items": serializer.data, 'currentPage': paginated_queryset.number,
                         'lastPage': paginator.num_pages})
