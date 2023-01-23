'''
Home views
'''
from django.shortcuts import render

from product.models import Product


# Create your views here.
def home(request):
    '''
    Loads the home page
    '''
    product_newest_list = Product.objects.filter(is_active=True).order_by('-product_created_at')[:10]
    product_best_price = Product.objects.filter(is_active=True).order_by('price')[:10]

    # del request.session["cart"]
    
    # cart_info = request.session.get('cart_info')
    # print(cart_info)
    # request.session["cart_info"] = {}
    # print(cart_info)

    context = {
        'product_newest_list': product_newest_list,
        'product_best_price': product_best_price,
    }

    return render(
        request,
        'home/index.html',
        context
    )



# HTTP Error 400
def custom_not_found(request, exception):
    '''
    Render custom error 404 page
    '''
    return render(request, '404.html', status=404)

