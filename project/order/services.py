import logging

from cart.services import Cart
from order.models import Order as OrderModel, OrderItem, PaymentMethod

# Logger
logger = logging.getLogger(__name__)


class Order:
    # Keys
    _pm_key = "session_payment_method_key"
    _si_key = "session_shipping_info_key"
    _bi_key = "session_billing_info_key"

    # Values
    _pm: PaymentMethod | None = None
    _si: dict | None = None
    _bi: dict | None = None

    def __init__(self, request) -> None:
        self._session = request.session
        self._request = request

        # Check current values of session keys
        pair_dict = {self._pm_key: "_pm", self._si_key: "_si", self._bi_key: "_bi"}

        for key, atr in pair_dict.items():
            # If key doesn't exist yet
            if key not in self._session:
                val = self._session[key] = None
            else:
                # Get the current session key if it exists
                val = self._session.get(key)

            self.__setattr__(atr, val)

    def get_pm(self) -> PaymentMethod | None:
        """Get the payment method of this order"""
        return self._pm

    def get_si(self) -> dict | None:
        """Set the shipping info of this order"""
        return self._si

    def get_bi(self) -> dict | None:
        """Set the billing info of this order"""
        return self._bi

    def set_pm(self, value: PaymentMethod) -> bool:
        """Set the payment method for this order"""
        if value in PaymentMethod.values:
            self._pm = self._session[self._pm_key] = value

            return True

        return False

    def set_si(self, value: dict) -> None:
        """Set the shipping info for this order"""
        self._si = self._session[self._si_key] = value

    def set_bi(self, value: dict) -> None:
        """Set the billing info for this order"""
        self._bi = self._session[self._bi_key] = value

    def clean(self, except_bi: bool = False) -> None:
        """Clean Order session data"""
        del self._session[self._pm_key]
        del self._session[self._si_key]

        self._pm = None
        self._si = None

        if not except_bi:
            del self._session[self._bi_key]

            self._bi = None

    def create(self) -> str | None:
        # Get Cart Session
        cart = Cart(self._request)

        # Get Cart Full Info
        cart_full_info = cart.get_full_info()

        # Get Payment Method
        pm = self.get_pm()

        # Get Shipping Info
        si = self.get_si()

        # Combine Shipping Info
        shipping_address = ""
        for key, value in si.items():
            if key not in [
                "shipping_full_name",
                "shipping_phone",
                "shipping_email",
            ]:
                shipping_address += f"{value}\n"

        # Order Data
        order_data = {
            "full_name": si["shipping_full_name"],
            "phone": si["shipping_phone"],
            "email": si["shipping_email"],
            "shipping_address": shipping_address,
            "amount_paid": cart_full_info["total_sale_price"],
            "payment_method": pm,
        }

        if self._request.user.is_authenticated:
            order_data["user_id"] = self._request.user.id

        try:
            # Create Order
            order = OrderModel.objects.create(**order_data)
        except Exception as e:
            logger.error(f"Failed to create Order: {e}")

            return None
        else:
            # Create Order Items
            order_items = [
                OrderItem(
                    **{
                        "order_id": order.id,
                        "product_id": c_i["product"].id,
                        "quantity": c_i["quantity"],
                        "price": c_i["total_sale_price"],
                    }
                )
                for c_i in cart_full_info["cart_items"]
            ]

            try:
                # Save Order Items
                OrderItem.objects.bulk_create(order_items)
            except Exception as e:
                logger.error(f"Failed to create Order Items: {e}")

                return None
            else:
                # Clean Order Session
                self.clean(except_bi=True)

                # Clean Cart Session
                cart.clean()

                # Return invoice
                return order.invoice
