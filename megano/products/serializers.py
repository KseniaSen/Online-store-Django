import datetime
from rest_framework import serializers

from .models import Product, Tag, Review, Specification, Category, CategoryIcon, Sale


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = 'id', 'name', 'value'


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date', 'product'

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')


class TagsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name'


class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    title = serializers.StringRelatedField()
    href = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    dateFrom = serializers.DateField(format='%d.%b')
    dateTo = serializers.DateField(format='%d.%b')

    def get_images(self, instance):
        images = []
        images_tmp = instance.product.images.all()
        for image in images_tmp:
            images.append({"src": f"/media/{image.__str__()}", "alt": image.name})
        return images

    class Meta:
        model = Sale
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
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

    def get_images(self, instance):
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({'src': f'/media/{image.__str__()}', 'alt': image.name})
        return images

    def get_price(self, instance):
        # return float(instance.price)
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)

    def get_rating(self, instance):
        return float(instance.rating)

    def get_salePrice(self, instance):
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)


class ProductListSerializer(serializers.ModelSerializer):
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

    def get_images(self, instance):
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({'src': f'/media/{image.__str__()}', 'alt': image.name})
        return images

    def get_price(self, instance):
        # return float(instance.price)
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)


    def get_rating(self, instance):
        return float(instance.rating)

    def get_salePrice(self, instance):
        today = datetime.date.today()
        sales = Sale.objects.filter(
            dateFrom__lte=today, dateTo__gte=today, product=instance.pk).values('salePrice').first()
        if sales:
            return sales['salePrice']
        return float(instance.price)


class CategoryIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryIcon
        fields = 'id', 'src', 'alt'


class SubcategoriesCategorySerializer(serializers.ModelSerializer):
    image = CategoryIconSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    image = CategoryIconSerializer(many=False, required=False)
    subcategories = SubcategoriesCategorySerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
