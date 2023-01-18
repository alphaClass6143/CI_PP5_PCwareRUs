'''
Urlpatterns
'''
from django.urls import path

from checkout import views


urlpatterns = [
    path('checkout/next_step', views.next_step, name='next_step'),
    path('checkout/previous_step', views.previous_step, name='previous_step'),
    path('checkout/load_step', views.load_step, name='load_step'),
    path('checkout/cancel_step', views.cancel_step, name='cancel_step'),
    path('checkout/confirm_address', views.confirm_address, name='confirm_address'),
    path('checkout/create-payment', views.CreatePaymentView.as_view(), name='create_payment'),
    path('checkout/confirm_payment', views.confirm_payment, name='confirm_payment')
]