from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Product

def product_detail(request, category_handle, product_handle):
    product = Product.objects.get(product_handle=product_handle)
    return render(request, 'product/product_detail.html', {'product': product})