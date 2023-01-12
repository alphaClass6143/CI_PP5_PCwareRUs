from django.shortcuts import render, redirect

# Create your views here.
def load_step(request):
    '''
    Load step
    '''
    step = request.session.get('step')
    print(step)

    if step == 1:
        return render(request,
                      'checkout/cart_step.html')

    elif step == 2:
        return render(request,
                      'checkout/address_step.html')

    elif step == 3:
        return render(request,
                      'checkout/payment_step.html')

    elif step == 4:
        return render(request,
                      'checkout/confirm_step.html')
    
    else:
        # Step does not exist
        request.session['step'] = 1
        return render(request,
                      'checkout/cart_step.html')


def previous_step(request):
    '''
    Previous step
    '''
    step = request.session.get('step')
    if not step <= 1 and not step > 4:
        request.session['step'] = step - 1
        print("redirecting")
        return redirect('load_step')

    return render(request,
                  'home/index.html')


def next_step(request):
    '''
    Next step
    '''
    step = request.session.get('step')
    if not step < 1 and not step >= 4:
        request.session['step'] = step + 1
        return redirect('load_step')
        
    return render(request,
                  'home/index.html')


def cancel_step(request):
    '''
    Cancel step
    '''
    del request.session['step']
        
    return render(request,
                  'home/index.html')

