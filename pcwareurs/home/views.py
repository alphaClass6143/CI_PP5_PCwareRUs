from django.shortcuts import render


# Create your views here.
def home(request):
    '''
    Loads the home page
    '''
    # request.session["cart"] = {}
    return render(
        request,
        'home/index.html'
    )