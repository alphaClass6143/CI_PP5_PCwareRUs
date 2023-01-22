'''
Views for different pages
'''
from django.shortcuts import render


# Create your views here.
def privacy_policy(request):
    '''
    Loads the privacy policy page
    '''
    return render(
        request,
        'pages/privacy-policy.html'
    )


def conditions(request):
    '''
    Loads the conditions page
    '''
    return render(
        request,
        'pages/privacy-policy.html'
    )


def newsletter(request):
    '''
    Loads the newsletter page
    '''
    return render(
        request,
        'pages/newsletter.html'
    )
