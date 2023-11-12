from django.urls import path

from cart.views import BasketView

app_name = 'cart'

urlpatterns = [
    path('api/basket', BasketView.as_view(), name='basket'),
    path('api/cart/', BasketView.as_view(), name='cart'),
]