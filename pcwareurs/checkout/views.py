from django.shortcuts import render, redirect

from user.models import Address

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
        address_list = Address.objects.filter(user=request.user)
        print(address_list)
        return render(request,
                      'checkout/address_step.html', {'address_list': address_list})

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




def confirm_cart(request):
    return redirect('next_step')


def confirm_address(request):
    '''
    Confirming the address
    '''
    if request.method == 'POST':

        # Check if step is created or updated

        if 'addresses' not in request.session:
            # Create
            request.session['addresses'] = ""



        else:
            # Update 
            addresses = request.session.get('addresses')

            # Check if address is selected
        

        #Create step
        #
    request.session['addresses']


def confirm_payment(request):

    

    # TODO Confirm payment
    return redirect('next_step')


def confirm_order(request):
    # TODO Create final order
    return redirect('next_step')



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

