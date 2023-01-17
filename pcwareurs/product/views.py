'''
Product views
'''
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from product.forms import ReviewAddForm, ReviewEditForm

from product.models import Product, Review

def product_detail(request, category_handle, product_handle):
    product = Product.objects.get(product_handle=product_handle)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product/product_detail.html', {'product': product, 'reviews': reviews})



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
                  {'error_message': 'Invalid request'})

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