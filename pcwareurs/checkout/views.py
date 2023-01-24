'''
Checkout views
'''
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from user.models import Address
from checkout.models import Order, OrderPosition
from product.models import Product

from checkout.forms import AddressForm

import stripe


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
        messages.error(
            request,
            "There's nothing in your cart at the moment"
        )
        return redirect('home')

    # Load cart overview
    if step == 1:
        return render(
            request,
            'checkout/cart_step.html'
        )

    # Load address_step
    elif step == 2:
        delivery_address = request.session.get('delivery_address')
        billing_address = request.session.get('billing_address')

        if request.user.is_authenticated:
            address_list = Address.objects.filter(user=request.user, is_active=True)

            context = {
                'address_list': address_list,
                'delivery_address': delivery_address,
                'billing_address': billing_address
            }

        else:
            context = {
                'delivery_address': delivery_address,
                'billing_address': billing_address
            }

        return render(
            request,
            'checkout/address_step.html',
            context
        )

    # Load payment step
    elif step == 3:
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        delivery_address = request.session.get('delivery_address')
        billing_address = request.session.get('billing_address')

        total = float(cart_info["total"])

        order_id = str(uuid.uuid4().hex.upper())

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=round(total * 100),
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'order_number': order_id,
            },
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
            delivery.is_used = True
            delivery.save()

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
            billing.is_used = True
            billing.save()

        # Create Order
        if request.user.is_authenticated:
            order = Order.objects.create(
                order_id=order_id,
                email=request.session.get('order_email'),
                total=total,
                payment_id=intent.id,
                user=request.user,
                delivery_address=delivery,
                billing_address=billing
            )
        else:
            order = Order.objects.create(
                order_id=order_id,
                total=total,
                email=request.session.get('order_email'),
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
        }

        return render(request, template, context)
    # Confirmation screen
    elif step == 4:
        del request.session['cart']
        del request.session['cart_info']
        del request.session['billing_address']
        del request.session['order_email']
        del request.session['delivery_address']
        del request.session['step']

        return render(
            request,
            'checkout/checkout_success.html'
        )

    else:
        # Step does not exist
        request.session['step'] = 1
        return render(
            request,
            'checkout/cart_step.html'
        )

def confirm_address(request):
    '''
    Confirming the address
    '''
    if request.method == 'POST':
        form = AddressForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['order_email'] = request.POST['email']

            # Same address
            if request.POST['same_address'] == '1':

                # Set custom address with same address
                if request.POST['delivery_address'] == 'custom':
                    request.session['cart_info']['delivery'] = 'custom'
                    request.session['cart_info']['billing'] = 'custom'
                    delivery_address = {
                        'full_name': request.POST['custom_delivery_full_name'],
                        'street': request.POST['custom_delivery_street'],
                        'city': request.POST['custom_delivery_city'],
                        'zip': request.POST['custom_delivery_zip'],
                        'state': request.POST['custom_delivery_state'],
                        'country': request.POST['custom_delivery_country']
                    }
                    request.session['delivery_address'] = delivery_address
                    request.session['billing_address'] = delivery_address

                # Set selected address
                else:
                    request.session['delivery_address'] = request.POST['delivery_address']
                    request.session['billing_address'] = request.POST['delivery_address']

            # Two different addresses
            else:
                # Check if delivery is custom
                if request.POST['delivery_address'] == 'custom':
                    request.session['cart_info']['delivery'] = 'custom'
                    request.session['delivery_address'] = {
                        'full_name': request.POST['custom_delivery_full_name'],
                        'street': request.POST['custom_delivery_street'],
                        'city': request.POST['custom_delivery_city'],
                        'zip': request.POST['custom_delivery_zip'],
                        'state': request.POST['custom_delivery_state'],
                        'country': request.POST['custom_delivery_country']
                    }
                else:
                    request.session['delivery_address'] = request.POST['delivery_address']

                # Check if billing is custom
                if request.POST['billing_address'] == 'custom':
                    request.session['cart_info']['billing'] = 'custom'
                    request.session['billing_address'] = {
                        'full_name': request.POST['custom_billing_full_name'],
                        'street': request.POST['custom_billing_street'],
                        'city': request.POST['custom_billing_city'],
                        'zip': request.POST['custom_billing_zip'],
                        'state': request.POST['custom_billing_state'],
                        'country': request.POST['custom_billing_country']
                    }
                else:
                    request.session['billing_address'] = request.POST['billing_address']

            step = request.session.get('step')
            request.session['step'] = step + 1
        else:
            print(form.errors)
            messages.error(request, "Invalid address")
    return redirect('load_step')


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
    Cancel cancels checkout
    '''
    del request.session['step']
    del request.session['billing_address']
    del request.session['order_email']
    del request.session['delivery_address']
        
    return redirect('home')
