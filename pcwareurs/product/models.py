'''
Product models
'''
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Manufacturer(models.Model):
    '''
    Manufacturer model
    '''
    manufacturer_name = models.CharField(
        max_length=255
    )

    manufacturer_added_at = models.DateTimeField(
        default=datetime.now
    )

    manufacturer_modified_at = models.DateTimeField(
        null=True
    )

    def __str__(self):
        '''
        Returns manufacturer name
        '''
        return self.manufacturer_name


class Product(models.Model):
    '''
    Product model
    '''
    product_name = models.CharField(
        max_length=255
    )

    product_handle = models.CharField(
        max_length=255,
        unique=True
    )

    product_description = models.TextField()

    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        'category.Category',
        on_delete=models.CASCADE,
    )

    product_created_at = models.DateTimeField(
        default=datetime.now
    )

    product_modified_at = models.DateTimeField(
        null=True
    )

    def __str__(self):
        '''
        Returns product name
        '''
        return self.product_name


class Review(models.Model):
    '''
    Review model
    '''
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    content = models.TextField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )

    review_created_at = models.DateTimeField(
        default=datetime.now
    )

    review_modified_at = models.DateTimeField(
        null=True
    )
