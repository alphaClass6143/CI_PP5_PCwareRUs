'''
Cart views
'''
import json

from django.http import JsonResponse
from django.shortcuts import render
from product.models import Product
from django.template.loader import render_to_string

from cart.context_processors import cart_list



# Create your views here.
def cart_add(request):
    '''
    Adds product to cart
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data['product_id']
        quantity = data['quantity']
        
        if Product.objects.filter(id=int(product_id)).exists():
            cart = request.session.get('cart', {})
            print(product_id)

            if product_id in cart.keys():
                cart[product_id]["quantity"] += int(quantity)
            else:
                cart[product_id] = {
                    'quantity': int(quantity)
                }
            print(cart)
            request.session['cart'] = cart

            print(request.session.get('cart', {}))
    
            return render_cart(request)
        return JsonResponse({'error': 'Product does not exist'})
    return JsonResponse({'error': 'Invalid request method'})


def cart_remove(request):
    '''
    Remove product from cart
    '''
    data = json.loads(request.body)
    product_id = data['product_id']

    if request.method == "POST":
        if Product.objects.filter(id=int(product_id)).exists():

            cart = request.session.get('cart', {})
            if product_id in cart.keys():
                del cart[product_id]

                request.session['cart'] = cart
                return render_cart(request)
        return JsonResponse({'error': 'Product not in cart'})
    return JsonResponse({'error': 'Invalid request method'})


def cart_update(request):
    '''
    Update product in cart
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = str(data['product_id'])
        quantity = data['quantity']
        
        if Product.objects.filter(id=int(product_id)).exists():
            cart = request.session.get('cart', {})
            print(cart.keys())
            print(data['product_id'])
            if product_id in cart.keys():
                if quantity < 1:
                    del cart[product_id]
                else:
                    cart[product_id]["quantity"] = int(quantity)

                request.session['cart'] = cart
                return render_cart(request)
            return JsonResponse({'error': 'This product is not in the cart'})
        return JsonResponse({'error': 'Product does not exist'})
    return JsonResponse({'error': 'Invalid request method'})


def render_cart(request):
    """
    Renders the cart HTML and returns a JSON response
    """
    cart_html = render_to_string('cart/cart.html', cart_list(request))
    return JsonResponse({'success': True, 'cart_html': cart_html})
