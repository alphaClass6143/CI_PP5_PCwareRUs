'''
Forms for the user app
'''
from django import forms


class AddressForm(forms.Form):
    '''
    Address form
    '''
    street = forms.CharField(
        label='street',
        max_length=255,
        required=True
    )

    city = forms.CharField(
        label='city',
        max_length=32,
        required=True
    )

    zip = forms.CharField(
        label='zip',
        max_length=255,
        required=True
    )

    state = forms.CharField(
        label='state',
        max_length=255,
        required=True
    )

    country = forms.CharField(
        label='country',
        max_length=255,
        required=True
    )
