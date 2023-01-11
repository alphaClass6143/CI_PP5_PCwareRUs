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
    )

    street = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=255
    )

    zip = models.IntegerField()

    state = models.CharField(
        max_length=255
    )

    country = models.CharField(
        max_length=255
    )

    is_used = models.BooleanField(
        default=False
    )

    address_created_at = models.DateTimeField(
        default=datetime.now
    )
