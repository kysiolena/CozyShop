# Create context processor so our Subscribe can work on all pages
from subscribe.services import Subscribe


def subscribe(request):
    # Return the default data from our Subscribe
    return {"subscribe": Subscribe(request)}
