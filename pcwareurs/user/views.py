from django.shortcuts import render

# Create your views here.
def user_overview(request):
    '''
    User overview
    '''
    if request.user.is_authenticated:
        return render(request, 'user/user_overview.html')