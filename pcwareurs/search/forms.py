
'''
Home forms
'''
from django import forms


class SearchForm(forms.Form):
    '''
    Search form
    '''
    query = forms.CharField(
        max_length=100,
        required=True
    )