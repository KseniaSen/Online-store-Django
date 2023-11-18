from django.contrib import admin
from .models import Product, ProductImage, Tag, Review, Specification, Category, CategoryIcon, Sale


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Tag."""
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Specification."""
    list_display = ['pk', 'name', 'value']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели ProductImage."""
    list_display = ['pk', 'name', 'product']
    list_display_links = ['pk', 'name']
    ordering = ['pk']


class ImageInline(admin.StackedInline):
    """Класс для отображения изображений продукта в админке Product."""
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Product."""
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
    """Настройки панели администратора для модели Category."""
    list_display = ['pk', 'title', 'parent', 'active', 'favourite']
    list_display_links = ['pk', 'title']
    inlines = [IconInline]
    ordering = ['pk']


@admin.register(CategoryIcon)
class CategoryIconAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели CategoryIcon."""
    list_display = ['pk', 'src']
    list_display_links = ['pk']
    ordering = ['pk']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Review."""
    list_display = ['pk', 'author', 'date', 'product', 'rate']
    list_display_links = ['pk']
    ordering = ['pk']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Настройки панели администратора для модели Sale."""
    list_display = ['pk', 'title', 'salePrice', 'dateFrom', 'dateTo']
    list_display_links = ['pk']
    ordering = ['pk']
