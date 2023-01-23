'''
Forms for the product app
'''
from django import forms

from product.models import Product, Manufacturer
from category.models import Category
from product.widgets import CustomClearableFileInput
from django.forms.widgets import ClearableFileInput


class ReviewForm(forms.Form):
    '''
    Review form
    '''
    rating_choices = [(i, f"{i} star") for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=rating_choices
    )

    content = forms.CharField(
        widget=forms.Textarea
    )


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
        category_choices = [(c.id, c.category_name) for c in Category.objects.all()]
        manufacturer_choices = [(m.id, m.manufacturer_name) for m in Manufacturer.objects.all()]

        self.fields['category'].choices = category_choices
        self.fields['manufacturer'].choices = manufacturer_choices
