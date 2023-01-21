'''
Context processors
'''
from category.models import Category


def category_list(request):
    '''
    Creates a list of categories available in the whole app
    '''
    category = Category.objects.all()
    return {
        'category_list': category
    }
