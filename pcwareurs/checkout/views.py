from django.shortcuts import render, redirect

from user.models import Address
from checkout.forms import AddressForm

import stripe
import json
from django.contrib import messages

from django.conf import settings

from checkout.models import Order, OrderPosition

from product.models import Product


from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def load_step(request):
    '''
    Load step
    '''
    step = request.session.get('step')

    cart_info = request.session.get('cart_info', {})
    cart = request.session.get('cart', {})


    if not cart:
        messages.error(request,
                        "There's nothing in your bag at the moment")
        return redirect('home')

    # Load cart overview
    if step == 1:
        return render(
            request,
            'checkout/cart_step.html'
        )

    # Load address_step
    elif step == 2:
        address_list = Address.objects.filter(user=request.user)

        delivery_address = request.session.get('delivery_address')
        billing_address = request.session.get('billing_address')

        return render(
            request,
            'checkout/address_step.html',
            {
                'address_list': address_list,
                'delivery_address': delivery_address,
                'billing_address': billing_address
            }
        )

    # Load payment step
    elif step == 3:
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        delivery_address = request.session.get('delivery_address')
        billing_address = request.session.get('billing_address')

        total = float(cart_info["total"]) + float(cart_info["delivery_fee"])

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=round(total * 100),
            currency=settings.STRIPE_CURRENCY,
        )
        
        if 'delivery' in cart_info and cart_info['delivery'] == 'custom':
            delivery = Address.objects.create(
                full_name=delivery_address["full_name"],
                street=delivery_address["full_name"],
                city=delivery_address["city"],
                zip=delivery_address["zip"],
                state=delivery_address["state"],
                country=delivery_address["country"],
                is_used=True,
                is_active=False
            )
        else:
            delivery = Address.objects.get(id=delivery_address)

        if 'billing' in cart_info and cart_info['billing'] == 'custom':
            billing = Address.objects.create(
                full_name=billing_address["full_name"],
                street=billing_address["full_name"],
                city=billing_address["city"],
                zip=billing_address["zip"],
                state=billing_address["state"],
                country=billing_address["country"],
                is_used=True,
                is_active=False
            )
        else:
            billing = Address.objects.get(id=billing_address)

        # Create Order 
        if request.user.is_authenticated:
            order = Order.objects.create(
                total=total,
                payment_id=intent.id,
                user=request.user,
                delivery_address=delivery,
                billing_address=billing
            )
        else:
            order = Order.objects.create(
                total=total,
                payment_id=intent.id,
                delivery_address=delivery,
                billing_address=billing
            )

        # Create Order Positions
        counter = 1
        for item_id, item_data in cart.items():
            product = Product.objects.get(id=item_id)

            OrderPosition.objects.create(
                position=counter,
                product=product,
                order=order,
                quantity=item_data["quantity"]
            )
            counter += 1
        
        

        if not stripe_public_key:
            messages.warning(
                request,
                ('Stripe public key is missing. '
                 'Did you forget to set it in '
                 'your environment?'))

        template = 'checkout/payment_step.html'
        context = {
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'order_id': order.id,
            'payment_id': intent.id,
            'total': cart_info["total"],
            'delivery_fee': cart_info["delivery_fee"]
        }

        return render(request, template, context)
    
    else:
        # Step does not exist
        request.session['step'] = 1
        return render(
            request,
            'checkout/cart_step.html'
        )


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




def confirm_order(request):
    order_id = request.POST['order_id']
    payment_id = request.POST['payment_id']

    print(order_id)
    print(payment_id)

    return render(
        request,
        'checkout/success.html'
    )


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
                request.session['cart_info']['delivery'] = 'custom'
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
                    request.session['cart_info']['billing'] = 'custom'
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



@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = "whsec_8aed239c419596300cd5b87147604ca4465ca01b3f4ef647f7043028c9cd06b9"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("Received stripe")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)