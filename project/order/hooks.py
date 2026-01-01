from django.conf import settings
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from order.models import Order, Status


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    # Grab info
    ipn_obj = sender

    # WARNING !
    # Check that the receiver email is the same we previously
    # set on the `business` field. (The user could tamper with
    # that fields on the payment form before it goes to PayPal)
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        # Not a valid payment
        return

    if ipn_obj.invoice:
        # Get OrderModel
        print(ipn_obj.invoice)

        order_m = Order.objects.get(invoice=ipn_obj.invoice)

        if order_m:
            print(ipn_obj.payment_status)

            if ipn_obj.payment_status == ST_PP_COMPLETED:
                # Set PAID Status
                order_m.status = Status.PAID
                order_m.save()
