'''
Urlpatterns
'''

from django.urls import path
from . import views

urlpatterns = [
    path('user/user_overview', views.user_overview, name='user_overview'),
]