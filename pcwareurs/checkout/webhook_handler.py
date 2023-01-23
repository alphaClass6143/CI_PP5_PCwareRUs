'''
Webhook handler
'''
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from checkout.models import Order


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email
        """
        customer_email = order.email
        subject = render_to_string(
            'checkout/email/order_confirmation_subject.txt',
            {
                'order': order
            }
        )
        body = render_to_string(
            'checkout/email/order_confirmation_body.txt',
            {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            }
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # Get order id
        order_id = event.data.object.metadata.get('order_number')

        # Set order with payment id true
        order = Order.objects.get(order_id=order_id)

        if not order.payment_successful:
            order.payment_successful = True
            order.save()

        # Send confirm email
        self._send_confirmation_email(order)

        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Order verified'),
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )