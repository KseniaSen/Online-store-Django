import datetime
from rest_framework import serializers
from typing import List, Dict

from .models import Product, Tag, Review, Specification, Category, CategoryIcon, Sale


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор для спецификаций продукта."""
    class Meta:
        model = Specification
        fields = 'id', 'name', 'value'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов о продукте."""
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date', 'product'

    def get_date(self, instance: Review) -> str:
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')


class TagsProductSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов продукта."""
    class Meta:
        model = Tag
        fields = 'id', 'name'


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор для скидок на продукты."""
    images = serializers.SerializerMethodField()
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    dateFrom = serializers.DateField(format='%d.%b')
    dateTo = serializers.DateField(format='%d.%b')

    def get_images(self, instance: Sale) -> List[Dict[str, str]]:
        images = []
        images_tmp = instance.product.images.all()
        for image in images_tmp:
            images.append({"src": f"/media/{image.__str__()}", "alt": image.name})
        return images

    class Meta:
        model = Sale
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, required=False)
    tags = TagsProductSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, instance: Product) -> List[Dict[str, str]]:
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({'src': f'/media/{image.__str__()}', 'alt': image.name})
        return images

    def get_price(self, instance: Product) -> float:
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)

    def get_rating(self, instance: Product) -> float:
        return float(instance.rating)

    def get_salePrice(self, instance: Product) -> float:
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка продуктов."""
    images = serializers.SerializerMethodField()
    tags = TagsProductSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    reviews = serializers.IntegerField(source='reviews.count')
    price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, instance: Product) -> List[Dict[str, str]]:
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({'src': f'/media/{image.__str__()}', 'alt': image.name})
        return images

    def get_price(self, instance: Product) -> float:
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)

    def get_rating(self, instance: Product) -> float:
        return float(instance.rating)

    def get_salePrice(self, instance: Product) -> float:
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)


class CategoryIconSerializer(serializers.ModelSerializer):
    """Сериализатор для иконок категорий."""
    class Meta:
        model = CategoryIcon
        fields = 'id', 'src', 'alt'


class SubcategoriesCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий категории."""
    image = CategoryIconSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    image = CategoryIconSerializer(many=False, required=False)
    subcategories = SubcategoriesCategorySerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
