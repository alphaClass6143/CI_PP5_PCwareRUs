


def cart(request):
    pass

def cart_list(request):
    '''
    Provide cart
    '''
    return {'cart': request.session.get('cart', {})}