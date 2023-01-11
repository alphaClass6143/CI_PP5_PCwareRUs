from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Category
from product.models import Product

def category_detail(request, handle):
    category = Category.objects.get(handle=handle)
    products = Product.objects.filter(category=category)
    return render(request, 'category/category_detail.html', {'category': category, 'products': products})
