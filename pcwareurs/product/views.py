'''
Product views
'''
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from product.forms import ReviewForm, ProductForm

from product.models import Product, Review
from category.models import Category


# Views
def product_detail(request, category_handle, product_handle):
    '''
    Shows product page
    '''
    get_object_or_404(Category, category_handle=category_handle)
    product = get_object_or_404(Product, product_handle=product_handle)
    reviews = Review.objects.filter(product=product)

    template = 'product/product_detail.html'
    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, template, context)



@login_required
def add_product(request):
    """ 
    Add a product
    """
    print("add product")
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to do that')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has been added')
            print("product added?")
            return redirect(reverse(
                'product_detail',
                kwargs={
                    'category_handle': product.category.category_handle,
                    'product_handle': product.product_handle
                }))
        else:
            messages.error(
                request,
                'Invalid form data'
            )
    else:
        form = ProductForm()

    template = 'product/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    '''
    Edit product
    '''
    pass


@login_required
def delete_product(request, product_id):
    '''
    Delete product
    '''
    # Query for the post
    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id)
        category_handle = product.category.category_handle

        product.delete()

        return redirect(
            'category_detail',
            category_handle=category_handle
        )

    messages.error(request, 'You are not allowed to do that')
    return redirect('home')


@login_required
def add_review(request, product_id):
    '''
    Adds review to product
    '''
    # Query for the product
    product = get_object_or_404(Product, pk=product_id)

    # Get form
    form = ReviewForm()

    # Check if review exists
    # Add a new comment
    if request.method == 'POST':
        if not Review.objects.filter(user=request.user).exists():
  
            if form.is_valid():
                Review.objects.create(
                    user=request.user,
                    product=product,
                    content=form.cleaned_data['content'],
                    rating=form.cleaned_data['rating'],
                    created_at=datetime.now()
                )

                return redirect(reverse(
                    'product_detail',
                    kwargs={
                        'category_handle': product.category.category_handle,
                        'product_handle': product.product_handle
                    })
                )

            messages.error(request, 'Invalid form')   

        # Invalid request for review add -> exists
        messages.error(request, 'This review does not exist')
        return render(
            request,
            'home/index.html',
        )

    if Review.objects.filter(user=request.user).exists():
        messages.error(request, 'You already reviewed this product')
        return redirect('product_detail', product_id=product.id)


    return render(
        request,
        'product/add_review.html',
        {
            'product':product,
            'form': form
        }
    )


@login_required
def edit_review(request, review_id):
    '''
    Edit review route
    '''
    review = Review.objects.get(id=review_id)

    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
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

    # User is not logged in and not allowed to edit it
    messages.error(
        request,
        'Really? No you cannot edit this review, this is not your review!'
    )
    return render(
        request,
        'product/product_detail.html',
        {'product_detail': review.product}
    )


@login_required
def delete_review(request, review_id):
    '''
    Delete review route
    '''