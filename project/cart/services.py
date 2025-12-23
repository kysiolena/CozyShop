import json
import logging
from typing import TypedDict

# Logger
logger = logging.getLogger(__name__)


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

    def get_items(self) -> list[TCartItem]:
        return self._cart

    def get_ids(self) -> list[int]:
        return [item["product_id"] for item in self._cart]

    def get_item(self, product_id: int) -> TCartItem | None:
        try:
            return [item for item in self._cart if item["product_id"] == product_id][0]
        except Exception as e:
            logger.error(f"Failed to get Product #{product_id} from the Cart: {e}")

            return None

    def get_item_index(self, product_id: int) -> int:
        try:
            item = self.get_item(product_id)

            return self._cart.index(item)
        except Exception as e:
            logger.error(f"Failed to get Product #{product_id} index in the Cart: {e}")

            return -1

    def add_item(self, product_id: int, quantity: int) -> bool:
        try:
            # Product already in the cart
            if product_id in self.get_ids():
                return False

            new_item: TCartItem = {"product_id": product_id, "quantity": quantity}

            # Update Cart
            self._cart.append(new_item)

            self._session.modified = True

            return True
        except Exception as e:
            logger.error(f"Failed to add Product #{product_id} to the Cart: {e}")

            return False

    def delete_item(self, product_id: int) -> bool:
        try:
            # Update cart
            item_index = self.get_item_index(product_id)

            del self._cart[item_index]

            self._session.modified = True

            return True
        except Exception as e:
            logger.error(f"Failed to delete Product #{product_id} from the Cart: {e}")

            return False

    def update(self, data: list[TCartItem]) -> bool:
        try:
            # Update cart
            self._cart = self._session[self._key] = data

            return True
        except Exception as e:
            logger.error(f"Failed to update Cart: {e}")

            return False

    def clean(self) -> bool:
        try:
            self._cart = self._session[self._key] = []

            return True
        except Exception as e:
            logger.error(f"Failed to clean the Cart: {e}")

            return False

    def __len__(self):
        return len(self._cart)

    def __str__(self):
        return json.dumps(self._cart)
