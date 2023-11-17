from django.db import models

from products.models import Product
from users.models import Profile


class Order(models.Model):
    """Модель для хранения информации о заказах."""
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['pk']

    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, null=False, blank=False, related_name='orders')
    deliveryType = models.CharField(max_length=150, default='')
    paymentType = models.CharField(max_length=150, default='')
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=150,  default='')
    city = models.CharField(max_length=255,  default='')
    address = models.TextField(max_length=255,  default='')
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f'{self.pk}'

    def fullName(self) -> str:
        return self.user.fullName

    def email(self) -> str:
        return self.user.email

    def phone(self) -> str:
        return self.user.phone

    def orderId(self) -> str:
        return f'{self.pk}'


class ProductOrder(models.Model):
    """Модель для хранения информации о продуктах в заказе."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
