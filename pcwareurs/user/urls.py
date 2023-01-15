'''
Urlpatterns
'''

from django.urls import path
from . import views
# from .views import (
#     AddressUpdateView,
# )


urlpatterns = [
    path('user/user_overview', views.user_overview, name='user_overview'),
    path('user/add_address', views.add_address, name='add_address'),
    path('user/edit_address/<int:address_id>', views.edit_address, name='edit_address'),
    # path('user/edit_address/<int:pk>', AddressUpdateView.as_view(), name='edit_address'),
    path('user/delete_address/<int:address_id>', views.delete_address, name='delete_address'),
]