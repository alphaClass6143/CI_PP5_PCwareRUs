'''
Urlpatterns
'''
from django.urls import path
from . import views

urlpatterns = [
    path('categories/<str:category_handle>/<str:product_handle>', views.product_detail, name='product_detail'),
]