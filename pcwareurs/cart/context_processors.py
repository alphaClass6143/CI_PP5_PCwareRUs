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
    
    cart_list = []
    print(cart.items())
    for item_id, item_data in cart.items():
        stock = get_object_or_404(Product, pk=item_id)
        print(stock)
        print(item_data["quantity"])

        cart_list.append({
            "product_id": stock.id,
            "product_name": stock.product_name,
            "product_handle": stock.product_handle,
            "category_handle": stock.category.category_handle,
            # TODO: Add image
            "product_image": "nope",
            'quantity': item_data["quantity"]
        })

    print(cart_list)
    return {
        'cart_list': cart_list
    }
