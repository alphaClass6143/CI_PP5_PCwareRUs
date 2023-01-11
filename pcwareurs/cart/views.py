'''
Cart views
'''
from django.http import JsonResponse
from django.shortcuts import render
from product.models import Product



# Create your views here.
def cart_add(request):
    '''
    Adds product to cart
    '''
    if request.method == "POST":
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']

        if Product.objects.filter(id=product_id).exists():
            cart = request.session.get('cart', {})
            if product_id in cart:
                cart[product_id] += int(quantity)
            else:
                cart[product_id] = int(quantity)

            request.session['cart'] = cart
            return JsonResponse({'success': True})
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
