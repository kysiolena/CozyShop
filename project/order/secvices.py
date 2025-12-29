from typing import Literal

TPaymentMethod = Literal["paypal", "card"]


class Order:
    # Keys
    _pm_key = "session_payment_method_key"
    _si_key = "session_shipping_info_key"
    _bi_key = "session_billing_info_key"

    # Values
    _pm: TPaymentMethod | None = None
    _si: dict | None = None
    _bi: dict | None = None

    # Available payment methods
    _available_pms: list[TPaymentMethod] = ["paypal", "card"]

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

    def get_pm(self) -> TPaymentMethod | None:
        """Get the payment method of this order"""
        return self._pm

    def get_si(self) -> dict | None:
        """Set the shipping info of this order"""
        return self._si

    def get_bi(self) -> dict | None:
        """Set the billing info of this order"""
        return self._bi

    def set_pm(self, value: TPaymentMethod) -> None:
        """Set the payment method for this order"""
        if value in self._available_pms:
            self._pm = self._session[self._pm_key] = value

    def set_si(self, value: dict) -> None:
        """Set the shipping info for this order"""
        self._si = self._session[self._si_key] = value

    def set_bi(self, value: dict) -> None:
        """Set the billing info for this order"""
        self._bi = self._session[self._bi_key] = value

    def clean(self):
        """Clean Order session data"""
        del self._session[self._pm_key]
        del self._session[self._si_key]
        del self._session[self._bi_key]

        self._pm = None
        self._si = None
        self._bi = None

    def create(self) -> str | None:
        # Clean session: cart, shipping/billing address, payment_method (TO DO)
        # Return invoice
        return "ksdlfjsd-jfksdjf-kjfjdk"
