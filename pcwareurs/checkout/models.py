'''
Checkout models
'''
import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Order(models.Model):
    '''
    Order model
    '''
    order_id = models.CharField(
        max_length=32,
        null=False,
        unique=True,
        editable=False
    )

    total = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )

    email = models.EmailField()

    ordered_at = models.DateTimeField(
        default=datetime.now
    )

    payment_id = models.CharField(
        max_length=255
    )

    payment_successful = models.BooleanField(
        default=False
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

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()


class OrderPosition(models.Model):
    '''
    OrderPosition model
    '''
    position = models.PositiveIntegerField()

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField()
