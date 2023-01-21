'''
Home views
'''
import boto3

from django.shortcuts import render


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

    # request.session["cart"] = {}
    return render(
        request,
        'home/index.html'
    )
