'''
Category views
'''
from django.shortcuts import render, get_object_or_404

from category.models import Category
from product.models import Product


# Create your views here.
def category_detail(request, handle):
    '''
    List category
    '''
    category = get_object_or_404(Category, category_handle=handle)
    products = Product.objects.filter(category=category)

    return render(
        request,
        'category/category_detail.html',
        {'category': category, 'products': products}
    )
