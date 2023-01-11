'''
Checkout models
'''
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class PaymentMethod(models.Model):
    '''
    PaymentMethod model
    '''
    payment_name = models.CharField(
        max_length=255
    )


class Order(models.Model):
    '''
    Order model
    '''
    total = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )

    ordered_at = models.DateTimeField(
        default=datetime.now
    )

    payment_method = models.ForeignKey(
        'PaymentMethod',
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        'category.Category',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    delivery_address = models.ForeignKey(
        'user.Address',
        on_delete=models.CASCADE,
        related_name='delivery_address'
    )

    billing_address = models.ForeignKey(
        'user.Address',
        on_delete=models.CASCADE,
        related_name='billing_address'
    )


class OrderPosition(models.Model):
    '''
    OrderPosition model
    '''
    position = models.IntegerField()

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField()
