from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = "order"

    # Set up PayPal IPN Signal
    def ready(self):
        # noinspection PyUnusedImports
        import order.hooks
