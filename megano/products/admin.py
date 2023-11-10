from django.contrib import admin
from .models import Product, ProductImage, Tag, Review, Specification, Category, CategoryIcon, Sale


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'value']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'product']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'count', 'date', 'rating', 'active']
    list_display_links = ['pk', 'title']
    search_fields = ['title', 'description']
    inlines = [ImageInline]
    ordering = ['pk']


class IconInline(admin.StackedInline):
    model = CategoryIcon
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'parent']
    inlines = [IconInline]
    ordering = ['pk']


@admin.register(CategoryIcon)
class CategoryIconAdmin(admin.ModelAdmin):
    list_display = ['pk', 'src', 'alt']
    list_display_links = ['pk']
    ordering = ['pk']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'date', 'product', 'rate']
    list_display_links = ['pk']
    ordering = ['pk']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['pk']
    ordering = ['pk']
