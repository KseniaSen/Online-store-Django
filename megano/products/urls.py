from django.urls import path
from .views import (
    ProductDetail,
    TagsList,
    CategoryList,
    BannersList,
    LimitedList,
    PopularList,
    ReviewCreateView,
    SalesList,
    ProductListView,
)

urlpatterns = [
    path('api/product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('api/tags/', TagsList.as_view(), name='tags_list'),
    path('api/categories/', CategoryList.as_view(), name='categories_list'),
    path('api/banners/', BannersList.as_view(), name='banners_list'),
    path('api/products/limited/', LimitedList.as_view(), name='limited_list'),
    path('api/products/popular/', PopularList.as_view(), name='popular'),
    path('api/product/<int:pk>/reviews', ReviewCreateView.as_view(), name='review-create'),
    path('api/sales/', SalesList.as_view(), name='sales_list'),
    path('api/catalog/', ProductListView.as_view(), name='product-list'),
]
