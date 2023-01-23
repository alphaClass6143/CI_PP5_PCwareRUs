'''
Pages forms
'''
from django import forms


class NewsletterForm(forms.Form):
    '''
    Newsletter form
    '''
    name = forms.CharField(
        max_length=255
    )

    email = forms.EmailField()
