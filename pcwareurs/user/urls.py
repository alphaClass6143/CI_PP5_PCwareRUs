'''
Urlpatterns
'''

from django.urls import path
from . import views

urlpatterns = [
    path('user/user_overview', views.user_overview, name='user_overview'),
    path('user/add_address', views.add_address, name='add_address'),
]