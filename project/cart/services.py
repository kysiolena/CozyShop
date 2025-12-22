from typing import TypedDict


class TCartItem(TypedDict):
    product_id: int
    quantity: int


class Cart:
    _key = "session_cart_key"

    def __init__(self, request) -> None:
        self._session = request.session

        # If cart doesn't exist yet
        if self._key not in self._session:
            cart = self._session[self._key] = []
        else:
            # Get the current session key if it exists
            cart = self._session.get(self._key)

        # Make sure cart is available on all pages of site
        self._cart = cart

    def get_items(self, request, ids_only=True) -> list[TCartItem]:
        # Default Cart
        cart_items = []

        # Some logic...

        return cart_items

    def add_item(self, request, product_id: int, quantity: int) -> bool:
        new_item: TCartItem = {"product_id": product_id, "quantity": quantity}

        # Current Cart
        cart_items = self.get_items(request, False)

        # Update Cart
        cart_items.append(new_item)

        # Some logic...

        return True

    def update_item(self, request, product_id: int, quantity: int) -> bool:
        # Current Cart
        cart_items = self.get_items(request, False)

        def check_and_update_item_quantity(item: TCartItem):
            """Update cart item quantity"""
            if item["product_id"] == product_id:
                item["quantity"] = quantity

            return item

        # New cart
        new_cart_items = [check_and_update_item_quantity(c_i) for c_i in cart_items]

        # Some logic...

        return True

    def delete_item(self, request, product_id: int) -> bool:
        # Current Cart
        cart_items = self.get_items(request, False)

        # New cart
        new_cart_items = [c_i for c_i in cart_items if c_i != product_id]

        # Some logic...

        return True

    def clear(self) -> bool:
        # Some logic...

        return True
