'''
Home views
'''
import boto3

from django.shortcuts import render

from product.models import Product


# Create your views here.
def home(request):
    '''
    Loads the home page
    '''
    # create an S3 client
    s3 = boto3.client('s3')

    try:
        # try to list all the buckets
        response = s3.list_buckets()
        # if the request is successful, check if the buckets are returned
        if 'Buckets' in response:
            print("Connection to S3 successful!")
        else:
            raise Exception("No buckets found.")
    except Exception as e:
        print("Error connecting to S3: ", e)

    product_newest_list = Product.objects.filter(is_active=True).order_by('-product_created_at')[:10]
    product_best_price = Product.objects.filter(is_active=True).order_by('price')[:10]

    context = {
        'product_newest_list': product_newest_list,
        'product_best_price': product_best_price,
    }

    # request.session["cart"] = {}
    return render(
        request,
        'home/index.html',
        context
    )



# HTTP Error 400
def custom_not_found(request, exception):
    '''
    Render error 404 page
    '''
    return render(request, '404.html', status=404)

