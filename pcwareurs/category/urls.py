'''
Urlpatterns
'''
from django.urls import path

from category import views

urlpatterns = [
    path(
        'categories/<str:handle>/',
        views.category_detail,
        name='category_detail'
    ),
]
