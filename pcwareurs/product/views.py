'''
Product views
'''
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from product.forms import ReviewAddForm, ReviewEditForm, ProductForm

from product.models import Product, Review, Manufacturer
from category.models import Category


def product_detail(request, category_handle, product_handle):
    '''
    Shows product page
    '''
    product = Product.objects.get(product_handle=product_handle)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product/product_detail.html', {'product': product, 'reviews': reviews})



def add_product(request):
    '''
    Adds product
    '''
    # Query for the post
    if request.user.is_staff:
        # Add a new post
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                
                # Get category and manufacturer
                category = Category.objects.get(id=form.cleaned_data['category_id'])
                manufacturer = Manufacturer.objects.get(id=form.cleaned_data['manufacturer_id'])

                Product.objects.create(
                    product_name=form.cleaned_data['name'],
                    handle=form.cleaned_data['handle'],
                    product_description=form.cleaned_data['description'],
                    manufacturer=manufacturer,
                    category=category,
                    product_created_at=datetime.now()
                )
                return redirect('product_detail', category_handle=category.category_handle, product_handle=form.cleaned_data['handle'],)

            return render(request,
                'product/add_product.html',
                {'error_message': 'Invalid request'})

        return render(request,
                    'product/add_product.html')

    return render(request,
                    'home/index.html',
                    {'error_message': 'No editing'})


def edit_product(request, product_id):
    '''
    Edit product
    '''
    pass


def delete_product(request, product_id):
    '''
    Delete product
    '''
    # Query for the post
    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id)
        category_handle = product.category.category_handle

        product.delete()

        return redirect('category_detail', category_handle=category_handle)

    return render(request,
                    'home/index.html',
                    {'error_message': 'No editing'})


def add_review(request, product_id):
    '''
    Adds review to product
    '''
    # Query for the product
    product = get_object_or_404(Product, pk=product_id)

    # Check if review exists
    # Add a new comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not Review.objects.filter(user=request):

                form = ReviewAddForm(request.POST)
                if form.is_valid():
                    Review.objects.create(
                        user=request.user,
                        product=product,
                        content=form.cleaned_data['content'],
                        rating=form.cleaned_data['rating'],
                        created_at=datetime.now()
                    )
                    return redirect('product_detail', product_id=product.id)

            # Invalid request for review add -> exists
            return render(request,
                  'home/index.html',
                  {'error_message': 'This review does not exist'})

    return render(request,
                  'home/index.html',
                  {'error_message': 'Invalid request'})


def edit_review(request, review_id):
    '''
    Edit review route
    '''
    review = Review.objects.get(id=review_id)

    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewEditForm(request.POST)
            if form.is_valid():

                review.content = form.cleaned_data['content']
                review.modified_at = datetime.now()
                review.save()
                return redirect('product_detail', review_id=review.product.id)

            return render(request,
                          'product/edit_review.html',
                          {'error_message': 'Invalid input'})

        return render(request,
                      'product/edit_review.html',
                      {'review': review})

    return render(request,
                  'product/product_detail.html',
                  {'product_detail': review.product,
                   'error_message': 'Really? No you cannot edit this review, this is not your review!'})