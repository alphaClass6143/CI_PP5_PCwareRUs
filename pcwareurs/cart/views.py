'''
Cart views
'''
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from product.models import Product
from django.template.loader import render_to_string



# Create your views here.
def cart_add(request):
    '''
    Adds product to cart
    '''
    if request.method == "POST":
        print(request.body)
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
    product_id = request.POST['product_id']

    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]

        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Product not in cart'})


def cart_update(request):
    '''
    Update product in cart
    '''
    product_id = request.POST['product_id']
    quantity = request.POST['quantity']

    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id] = int(quantity)

        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Product not in cart'})


def render_cart(request):
    """
    Renders the cart HTML and returns a JSON response
    """
    cart = request.session.get('cart', {})
    print(cart)
    cart_html = render_to_string('cart/cart.html', {'cart': cart})
    return JsonResponse({'success': True, 'cart_html': cart_html})
