'''
Urlpatterns
'''
from django.urls import path

from pages import views


urlpatterns = [
    path(
        'privacy-policy/',
        views.privacy_policy,
        name='privacy_policy'
    ),
    path(
        'terms-and-conditions/',
        views.conditions,
        name='conditions'
    ),

    # Deactivated path for a newsletter signup on own site without mailchimp
    # path(
    #     'newsletter/',
    #     views.newsletter,
    #     name='newsletter'
    # )
]
