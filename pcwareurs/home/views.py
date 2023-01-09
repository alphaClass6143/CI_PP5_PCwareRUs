from django.shortcuts import render


# Create your views here.
def home(request):
    '''
    Loads the home page
    '''

    return render(request,
                  'home/index.html')