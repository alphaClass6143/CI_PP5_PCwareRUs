from django.shortcuts import render, redirect

from user.models import Address
from checkout.forms import AddressForm

import stripe
import json
from django.contrib import messages

from django.conf import settings


from django.http import JsonResponse
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY

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
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request,
                           "There's nothing in your bag at the moment")
            return redirect('home')

        #TODO Update with real total
        total = 100
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )


        if not stripe_public_key:
            messages.warning(request, ('Stripe public key is missing. '
                                    'Did you forget to set it in '
                                    'your environment?'))

        template = 'checkout/payment_step.html'
        context = {
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)
    
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
                    'full_name': request.POST['custom_delivery_full_name'],
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


class CreatePaymentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=200,
                currency='eur',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)
    

def confirm_payment(request):

    if request.method == 'POST':
        stripe_token = request.POST['stripeToken']
        try:
            
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

