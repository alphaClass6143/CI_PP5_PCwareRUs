'''
Urlpatterns
'''
from django.urls import path
from cart import views


urlpatterns = [
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),
]
