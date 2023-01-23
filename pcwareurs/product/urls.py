'''
Urlpatterns
'''
from django.urls import path

from product import views

urlpatterns = [
    path(
        'product/add_review/<int:product_id>',
        views.add_review,
        name='add_review'
    ),
    path(
        'product/edit_review/<int:review_id>',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'product/delete_review/<int:review_id>',
        views.delete_review,
        name='delete_review'
    ),
    path(
        'staff/add_product',
        views.add_product,
        name='add_product'
    ),
    path(
        'staff/edit_product/<str:product_handle>',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'staff/delete_product/<str:product_handle>',
        views.delete_product,
        name='delete_product'
    ),
    path(
        'categories/<str:category_handle>/<str:product_handle>',
        views.product_detail,
        name='product_detail'
    ),
]
