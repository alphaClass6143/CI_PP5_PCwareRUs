from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from product.models import Product, Stock


def cart_info(request):
    '''
    Provide general cart info
    '''
    return {'cart_info': request.session.get('cart_info', {})}


def cart_list(request):
    '''
    Provide cart
    '''
    cart = request.session.get('bag', {})

    cart_list = []
    for item_id, item_data in cart.items():
        stock = get_object_or_404(Stock, pk=item_id)
        cart_list.append({
            "stock_id": stock.id,
            "product_id": stock.product.id,
            "product_name": stock.product.product_name,
            "product_handle": stock.product_handle,
            "category_handle": stock.product.category.category_handle,
            # TODO: Add image
            "product_image": "nope",
            'quantity': item_data[quantity]
        })

    return cart_list
