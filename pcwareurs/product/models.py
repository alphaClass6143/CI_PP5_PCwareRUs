'''
Product models
'''
from django.db import models
from category.models import Category


# Create your models here.
class Manufacturer(models.Model):
    '''
    Manufacturer model
    '''
    manufacturer_name = models.CharField(
        max_length=255
    )

    manufacturer_added_at = models.DateTimeField(
        auto_now_add=True
    )


class Product(models.Model):
    '''
    Product model
    '''
    product_name = models.CharField(
        max_length=255
    )

    product_handle = models.CharField(
        max_length=255
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
        auto_now_add=True
    )

    product_modified_at = models.DateTimeField(
        null=True
    )
