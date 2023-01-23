'''
Search views
'''
from django.shortcuts import render, redirect
from django.contrib import messages

from search.forms import SearchForm

from product.models import Product

# Create your views here.
def search(request):
    '''
    Search for products
    '''
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']

        product_list = (Product.objects.all().filter(product_name__icontains=query)[:20])

        return render(
            request,
            'search/result.html',
            {
                'product_list': product_list,
                'query': query
            }
        )
    else:
        messages.error(request, "Something went wrong during your search")
    return redirect('home')