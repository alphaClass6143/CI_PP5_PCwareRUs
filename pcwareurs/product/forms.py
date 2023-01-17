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
    Review editform
    '''
    content = forms.CharField(
        widget=forms.Textarea
    )