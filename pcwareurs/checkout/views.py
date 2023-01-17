from django.shortcuts import render, redirect

from user.models import Address
from checkout.forms import AddressForm

import stripe

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

        delivery_address = request.session.get('delivery_address')
        billing_address = request.session.get('billing_address')

        return render(request,
                      'checkout/address_step.html', {'address_list': address_list, 'delivery_address': delivery_address, 'billing_address': billing_address})

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
        print("confirming address")
        form = AddressForm(request.POST, user=request.user)
        if form.is_valid():
            print("is valid")
            if request.POST['delivery_address'] == 'custom':
                delivery_address = {
                    'street': request.POST['custom_delivery_street'],
                    'city': request.POST['custom_delivery_city'],
                    'zip': request.POST['custom_delivery_zip'],
                    'state': request.POST['custom_delivery_state'],
                    'country': request.POST['custom_delivery_country']
                }
                request.session['delivery_address'] = delivery_address
            
            if request.POST['same_address'] == '1':
                if request.POST['delivery_address'] == 'custom':
                    request.session['billing_address'] = delivery_address

                else:
                    request.session['delivery_address'] = request.POST['delivery_address']
                    request.session['billing_address'] = request.POST['delivery_address']

            else:
                if not request.POST['delivery_address'] == 'custom':
                    request.session['delivery_address'] = request.POST['delivery_address']

                if request.POST['billing_address'] == 'custom':
                    request.session['billing_address'] = {
                        'street': request.POST['custom_billing_street'],
                        'city': request.POST['custom_billing_city'],
                        'zip': request.POST['custom_billing_zip'],
                        'state': request.POST['custom_billing_state'],
                        'country': request.POST['custom_billing_country']
                    }
                else:
                    request.session['billing_address'] = request.POST['billing_address']
            
            print("advance")
            step = request.session.get('step')
            request.session['step'] = step + 1
            return redirect('load_step')
        else:
            print(form.errors)
    else:

        print("not post")


def confirm_payment(request):

    if request.method == 'POST':
        stripe_token = request.POST['stripeToken']
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            charge = stripe.Charge.create(
                amount=1000,
                currency='usd',
                source=stripe_token,
                description='Example charge'
            )
            # Handle successful payment
            return redirect('order_confirmation')
        except stripe.error.CardError as e:
            # Handle errors
            pass
    return render(request, 'payment_error.html')
    

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

