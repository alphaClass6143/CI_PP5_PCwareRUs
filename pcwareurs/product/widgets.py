'''
Widgets
'''

from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomClearableFileInput(ClearableFileInput):
    '''
    Custom Image input
    '''
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'product/widget/custom_file_input.html'

    
