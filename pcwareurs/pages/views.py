'''
Views for different pages
'''
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from pages.forms import NewsletterForm


# Create your views here.
def privacy_policy(request):
    '''
    Loads the privacy policy page
    '''
    return render(
        request,
        'pages/privacy_policy.html'
    )


def conditions(request):
    '''
    Loads the conditions page
    '''
    return render(
        request,
        'pages/terms_and_conditions.html'
    )


# Deactivated code for a newsletter signup on own site without mailchimp

# def newsletter(request):
#     '''
#     Loads the newsletter page
#     '''

#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)
#         if form.is_valid():

#             # Prepare mail
#             customer_email = request.POST["email"]
#             subject = render_to_string(
#                 'pages/email/newsletter_subject.txt',
#                 {
#                     'name': request.POST["name"]
#                 }
#             )
#             body = render_to_string(
#                 'pages/email/newsletter_body.txt',
#                 {
#                     'name': request.POST["name"],
#                     'contact_email': settings.DEFAULT_FROM_EMAIL
#                 }
#             )

#             # Send mail
#             send_mail(
#                 subject,
#                 body,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [customer_email]
#             )

#             messages.success(
#                 request,
#                 'You have been signed up to the newsletter. Check your emails'
#             )
#         else:
#             messages.error(
#                 request,
#                 'Invalid form data'
#             )

#     return render(
#         request,
#         'pages/newsletter.html'
#     )
