from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from cart.services import Cart

UserModel = get_user_model()


# Sync local Cart with Profile Cart when User is logging in
def sync_cart(sender, request, user, **kwargs):
    # Get Cart
    cart = Cart(request)

    # Sync local Cart and Profile Cart
    cart.sync()


user_logged_in.connect(sync_cart, sender=UserModel)
