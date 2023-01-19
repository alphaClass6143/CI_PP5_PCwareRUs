'''
Urlpatterns
'''
from django.urls import path

from product import views

urlpatterns = [
    path(
        'categories/<str:category_handle>/<str:product_handle>',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'product/add_product',
        views.add_product,
        name='add_product'
    ),
    path(
        'product/add_review',
        views.add_review,
        name='add_review'
    ),
    path(
        'product/edit_review/<str:review_id>',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'product/edit_product/<str:product_handle>',
        views.edit_product,
        name='edit_product'
    ),
]
