# Create context processor so our Cart can work on all pages
from cart.services import Cart


def cart(request):
    # Return the default data from our Cart
    return {"cart": Cart(request)}
