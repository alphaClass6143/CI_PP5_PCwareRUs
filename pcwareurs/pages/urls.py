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
        'conditions/',
        views.conditions,
        name='conditions'
    ),
    path(
        'newsletter/',
        views.newsletter,
        name='newsletter'
    )
]
