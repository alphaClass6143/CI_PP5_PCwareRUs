'''
Checkout forms
'''
from django import forms

from user.models import Address


class AddressForm(forms.Form):
    '''
    AddressForm to confirm the address
    '''
    email = forms.EmailField()

    delivery_address = forms.ChoiceField(
        choices=[('custom', 'Custom Address')]
    )

    custom_delivery_full_name = forms.CharField(
        required=False
    )

    custom_delivery_street = forms.CharField(
        required=False
    )

    custom_delivery_city = forms.CharField(
        required=False
    )

    custom_delivery_zip = forms.CharField(
        required=False
    )

    custom_delivery_state = forms.CharField(
        required=False
    )

    custom_delivery_country = forms.CharField(
        required=False
    )

    billing_address = forms.ChoiceField(
        choices=[('custom', 'Custom Address')],
        required=False
    )

    custom_billing_street = forms.CharField(
        required=False
    )

    custom_billing_street = forms.CharField(
        required=False
    )

    custom_billing_city = forms.CharField(
        required=False
    )

    custom_billing_zip = forms.CharField(
        required=False
    )

    custom_billing_state = forms.CharField(
        required=False
    )

    custom_billing_country = forms.CharField(
        required=False
    )

    same_address = forms.BooleanField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        '''
        __init__
        '''
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['delivery_address'].choices += [
            (address.id, address) for address in Address.objects.filter(user=user)
        ]
        self.fields['billing_address'].choices += [
            (address.id, address) for address in Address.objects.filter(user=user)
        ]

    def clean(self):
        '''
        clean
        '''
        cleaned_data = super().clean()

        delivery_address = cleaned_data.get("delivery_address")
        billing_address = cleaned_data.get("billing_address")
        same_address = cleaned_data.get("same_address")

        # Check if form is valid:
        # If the address is same check just for custom delivery address
        if same_address:
            if delivery_address == 'custom':
                if not all([
                    cleaned_data.get("custom_delivery_full_name"),
                    cleaned_data.get("custom_delivery_street"),
                    cleaned_data.get("custom_delivery_city"),
                    cleaned_data.get("custom_delivery_zip"),
                    cleaned_data.get("custom_delivery_state"),
                    cleaned_data.get("custom_delivery_country")]):

                    raise forms.ValidationError("Please fill in all the required fields for the custom delivery address.")
        # If the address is NOT the same then check for both
        else:
            if delivery_address == 'custom':
                if not all([
                    cleaned_data.get("custom_delivery_full_name"),
                    cleaned_data.get("custom_delivery_street"),
                    cleaned_data.get("custom_delivery_city"),
                    cleaned_data.get("custom_delivery_zip"),
                    cleaned_data.get("custom_delivery_state"),
                    cleaned_data.get("custom_delivery_country")]):

                    raise forms.ValidationError("Please fill in all the required fields for the custom delivery address.")
            if billing_address == 'custom':
                if not all([
                    cleaned_data.get("custom_billing_full_name"),
                    cleaned_data.get("custom_billing_street"),
                    cleaned_data.get("custom_billing_city"),
                    cleaned_data.get("custom_billing_zip"),
                    cleaned_data.get("custom_billing_state"),
                    cleaned_data.get("custom_billing_country")]):

                    raise forms.ValidationError("Please fill in all the required fields for the custom billing address.")
