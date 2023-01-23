'''
Forms for the product app
'''
from django import forms
from django.forms.widgets import ClearableFileInput

from product.models import Product, Review, Manufacturer
from category.models import Category


class ReviewForm(forms.ModelForm):
    '''
    Review form
    '''
    class Meta:
        '''
        Meta
        '''
        model = Review
        fields = [
            'rating',
            'content'
        ]

    def __init__(self, *args, **kwargs):
        '''
        Init
        '''
        super().__init__(*args, **kwargs)
        rating_choices = [(i, f"{i} star") for i in range(1, 6)]

        self.fields['rating'].choices = rating_choices
        self.fields['rating'].widget = forms.Select(choices=rating_choices)


class ProductForm(forms.ModelForm):
    '''
    Product form
    '''

    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_handle',
            'product_description',
            'category',
            'manufacturer',
            'image',
            'price',
            'is_active'
        ]

    image = forms.ImageField(label='Image',
                             required=False,
                             widget=ClearableFileInput
                             )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_choices = [
            (c.id, c.category_name) for c in Category.objects.all()
        ]
        manufacturer_choices = [
            (m.id, m.manufacturer_name) for m in Manufacturer.objects.all()
        ]

        self.fields['category'].choices = category_choices
        self.fields['manufacturer'].choices = manufacturer_choices
