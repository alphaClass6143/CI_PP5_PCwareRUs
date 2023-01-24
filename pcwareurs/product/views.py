'''
Product views
'''
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

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
    rating = Review.objects.filter(product=product).aggregate(Avg('rating'))

    template = 'product/product_detail.html'
    context = {
        'product': product,
        'reviews': reviews,
        'rating': rating['rating__avg'],
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """
    Add a product
    """
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to do that')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has been added')
            return redirect(reverse(
                'product_detail',
                kwargs={
                    'category_handle': product.category.category_handle,
                    'product_handle': product.product_handle
                }))

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
    """
    Edit a product
    """
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to do that')
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Product has been updated'
            )
            return redirect(reverse(
                'product_detail',
                kwargs={
                    'category_handle': product.category.category_handle,
                    'product_handle': product.product_handle
                }))

        messages.error(
            request,
            'Invalid product information'
        )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.product_name}')

    template = 'product/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


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

        messages.success(request, 'Product has been deleted')
        return redirect(
            'category_detail',
            handle=category_handle
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

    # Add a new review
    if not Review.objects.filter(user=request.user, product=product).exists():
        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():

                Review.objects.create(
                    user=request.user,
                    product=product,
                    content=form.cleaned_data['content'],
                    rating=form.cleaned_data['rating'],
                )
                messages.success(request, 'Thank you for your review')
                return redirect(reverse(
                    'product_detail',
                    kwargs={
                        'category_handle': product.category.category_handle,
                        'product_handle': product.product_handle
                    })
                )

            messages.error(request, 'Invalid form')
        form = ReviewForm()
        return render(
                request,
                'product/add_review.html',
                {
                    'product': product,
                    'form': form
                }
            )

    messages.error(request, 'You already reviewed this product')
    return redirect(
        'product_detail',
        category_handle=product.category.category_handle,
        product_handle=product.product_handle
    )


@login_required
def edit_review(request, review_id):
    '''
    Edit review route
    '''
    # Get review
    review = get_object_or_404(Review, pk=review_id)

    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():

                review.rating = form.cleaned_data['rating']
                review.content = form.cleaned_data['content']
                review.modified_at = datetime.now()
                review.save()
                messages.success(request, "Edit successful")
                return redirect(
                    'product_detail',
                    category_handle=review.product.category.category_handle,
                    product_handle=review.product.product_handle
                )

            messages.error(request, "Invalid input")

        else:
            form = ReviewForm(instance=review)
            messages.info(
                request,
                f'You are editing your review for {review.product.product_name}'
            )

        return render(
            request,
            'product/edit_review.html',
            {
                'review': review,
                'form': form
            }
        )

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
    Delete review
    '''
    # Get review
    review = get_object_or_404(Review, pk=review_id)

    if request.user == review.user:

        # Product for redirect later
        product = review.product

        review.delete()

        messages.success(request, 'Review has been deleted')
        return redirect(
            'product_detail',
            category_handle=product.category.category_handle,
            product_handle=product.product_handle
        )

    messages.error(request, 'This is not your product')
    return redirect('home')
