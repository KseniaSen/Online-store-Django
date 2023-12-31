import datetime
from decimal import Decimal
from typing import Any

from megano.settings import CART_SESSION_ID
from products.models import Product, Sale


class Cart(object):
    """Класс Cart представляет корзину покупок в интернет-магазине."""

    def __init__(self, request: Any) -> None:
        """Функция для инициализации объекта Cart."""
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, count: int) -> None:
        """Функция для добавления товаров в корзину."""
        product_id = str(product.id)
        available_quantity = Product.objects.filter(pk=product.id).values('count').first()
        if product_id not in self.cart and available_quantity != 0:
            today = datetime.date.today()
            sales = Sale.objects.filter(
                dateFrom__lte=today, dateTo__gte=today, product=product_id).values('salePrice').first()
            if sales:
                self.cart[product_id] = {'count': count,
                                         'price': str(sales['salePrice'])}
            else:
                self.cart[product_id] = {'count': count,
                                         'price': str(product.price)}
        else:
            if available_quantity['count'] >= self.cart[product_id]['count'] + count:
                self.cart[product_id]['count'] += count
        self.save()

    def remove(self, product: Product, count: int) -> None:
        """Функция для удаления товаров из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            if count == 1 and self.cart[product_id]['count'] > 1:
                self.cart[product_id]['count'] -= int(count)
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self) -> None:
        """Итератор по товарам в корзине."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
            yield item

    def total_count(self) -> int:
        """Функция для возвращения общего количества товаров в корзине."""
        return sum(item['count'] for item in self.cart.values())

    def total_price(self) -> Decimal:
        """Функция для возвращения общей стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['count'] for item in
                   self.cart.values())

    def clear(self) -> None:
        """Функция для очищения корзины от всех товаров."""
        del self.session[CART_SESSION_ID]
        self.session.modified = True

    def save(self) -> None:
        """Функция для сохранения состояние корзины в сессии."""
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True
