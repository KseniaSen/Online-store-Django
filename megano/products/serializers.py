import datetime
from rest_framework import serializers

from .models import Product, Tag, Review, Specification


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


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, required=False)
    tags = TagsProductSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)


    class Meta:
        model = Product
        fields = "__all__"

    def get_images(self, instance):
        images = []
        images_tmp = instance.images.all()
        for image in images_tmp:
            images.append({'src': f'/media/{image.__str__()}', 'alt': image.name})
            print(images)
        return images
