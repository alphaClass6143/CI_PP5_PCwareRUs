'''
Admin panel models
'''
from django.contrib import admin

from product.models import Review, Product, Manufacturer


# Register your models here.
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    '''
    Manufacturer list in the admin panel
    '''
    list_filter = ['manufacturer_added_at']
    search_fields = ['manufacturer_name', 'manufacturer_added_at', 'manufacturer_modified_at']
    list_display = ['manufacturer_name', 'manufacturer_added_at', 'manufacturer_modified_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    Product list in the admin panel
    '''
    list_filter = ['product_created_at']
    search_fields = ['product_created_at', 'product_name']
    list_display = ['product_name', 'product_description', 'category', 'manufacturer', 'product_created_at', 'product_modified_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    '''
    Review list in the admin panel
    '''
    list_filter = ['review_created_at', 'rating']
    search_fields = ['review_created_at', 'content']
    list_display = ['user', 'rating', 'content', 'review_created_at']
