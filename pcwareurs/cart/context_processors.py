'''
Context processors (cart provider)
'''
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from product.models import Product


def cart_info(request):
    '''
    Provide general cart info
    '''
    return {'cart_info': request.session.get('cart_info', {})}


def cart_list(request):
    '''
    Provide cart
    '''

    cart = request.session.get('cart', {})
    cart_info = request.session.get('cart_info', {})

    cart_list = []
    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)

        cart_list.append({
            "product_id": product.id,
            "product_name": product.product_name,
            "product_handle": product.product_handle,
            "category_handle": product.category.category_handle,
            "product_image": product.image.url,
            'quantity': item_data["quantity"]
        })

    return {
        'cart_list': cart_list,
        'cart_info': cart_info
    }
