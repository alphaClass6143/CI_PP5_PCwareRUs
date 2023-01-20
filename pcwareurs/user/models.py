'''
User models
'''
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Address(models.Model):
    '''
    Address model
    '''
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
    )

    full_name = models.CharField(
        max_length=255
    )

    street = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=255
    )

    zip = models.CharField(
        max_length=32
    )

    state = models.CharField(
        max_length=255
    )

    country = models.CharField(
        max_length=255
    )

    is_used = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    address_created_at = models.DateTimeField(
        default=datetime.now
    )
