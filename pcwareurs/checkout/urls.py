'''
Urlpatterns
'''
from django.urls import path

from checkout import views
from checkout import webhooks


urlpatterns = [
    path(
        'checkout/next_step',
        views.next_step,
        name='next_step'
    ),
    path(
        'checkout/previous_step',
        views.previous_step,
        name='previous_step'
    ),
    path(
        'checkout/load_step',
        views.load_step,
        name='load_step'
    ),
    path(
        'checkout/cancel_step',
        views.cancel_step,
        name='cancel_step'
    ),
    path(
        'checkout/confirm_address',
        views.confirm_address,
        name='confirm_address'
    ),
    path(
        'checkout/confirm_order',
        views.confirm_order,
        name='confirm_order'
    ),
    path('webhook', views.stripe_webhook) # new
]