from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Category

def category_detail(request, handle):
    category = Category.objects.get(handle=handle)
    return render(request, 'category/category_detail.html', {'category': category})
