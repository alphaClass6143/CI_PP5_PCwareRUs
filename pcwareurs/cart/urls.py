'''
Urlpatterns
'''

from django.urls import path
from cart.views import cart_add, cart_remove, cart_update

urlpatterns = [
    path('cart/add/', cart_add, name='cart_add'),
    path('cart/remove/', cart_remove, name='cart_remove'),
    path('cart/update/', cart_update, name='cart_update'),
]
