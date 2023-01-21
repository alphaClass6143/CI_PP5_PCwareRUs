'''
Admin model
'''
from django.contrib import admin

from category.models import Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
    Category list in the admin panel
    '''
    list_filter = ['category_created_at']
    search_fields = ['category_created_at', 'category_name']
    list_display = [
        'category_name',
        'category_description',
        'category_created_at',
        'category_modified_at'
    ]
