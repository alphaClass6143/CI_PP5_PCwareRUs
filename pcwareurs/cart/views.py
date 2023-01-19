'''
Cart views
'''
import json

from django.http import JsonResponse
from django.shortcuts import render
from product.models import Product
from django.template.loader import render_to_string



# Create your views here.
def cart_add(request):
    '''
    Adds product to cart
    '''
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data['product_id']
        quantity = data['quantity']
        
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            cart = request.session.get('cart', {})

            if str(product.id) in cart.keys():
                cart[str(product.id)]["quantity"] += int(quantity)
            else:
                cart[str(product.id)] = {
                    "product_id": product_id,
                    "product_name": product.product_name,
                    "product_handle": product.product_handle,
                    "category_handle": product.category.category_handle,
                    # TODO: Add image
                    "product_image": "nope",
                    'quantity': int(quantity)
                }

            request.session['cart'] = cart
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
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            cart = request.session.get('cart', {})
            if str(product.id) in cart.keys():
                del cart[str(product.id)]

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
        product_id = data['product_id']
        quantity = data['quantity']
        
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            cart = request.session.get('cart', {})

            if str(product.id) in cart.keys():
                if quantity < 1:
                    del cart[str(product.id)]
                else:
                    cart[str(product.id)]["quantity"] = int(quantity)

                request.session['cart'] = cart
                return render_cart(request)
            return JsonResponse({'error': 'This product is not in the cart'})
        return JsonResponse({'error': 'Product does not exist'})
    return JsonResponse({'error': 'Invalid request method'})


def render_cart(request):
    """
    Renders the cart HTML and returns a JSON response
    """
    cart = request.session.get('cart', {})
    cart_html = render_to_string('cart/cart.html', {'cart': cart})
    return JsonResponse({'success': True, 'cart_html': cart_html})
