'''
Models for the category app
'''
from datetime import datetime
from django.db import models


# Create your models here.
class Category(models.Model):
    '''
    Category model
    '''
    name = models.CharField(
        max_length=255
    )

    category_handle = models.CharField(
        max_length=255
    )

    description = models.TextField()

    category_created_at = models.DateTimeField(
        default=datetime.now
    )

    category_modified_at = models.DateTimeField(
        null=True,
        blank=True
    )
