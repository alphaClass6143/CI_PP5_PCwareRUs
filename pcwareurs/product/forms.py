'''
Forms for the product app
'''
from django import forms


class ReviewAddForm(forms.Form):
    '''
    Review add form
    '''
    rating = forms.IntegerField()

    content = forms.CharField(
        widget=forms.Textarea
    )


class ReviewEditForm(forms.Form):
    '''
    Review edit form
    '''
    content = forms.CharField(
        widget=forms.Textarea
    )


class ManufacturerForm(forms.Form):
    '''
    Manufacturer form
    '''
    manufacturer_name = forms.CharField(
        max_length=255
    )


class ProductForm(forms.Form):
    '''
    Product form
    '''
    product_name = forms.CharField(
        max_length=255
    )

    product_description = forms.CharField(
        widget=forms.Textarea
    )

    manufacturer_id = forms.IntegerField()

    category_id = forms.IntegerField()
