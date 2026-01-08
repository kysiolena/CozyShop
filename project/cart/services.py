import json
import logging
from typing import TypedDict

from catalog.models import Product

# Logger
logger = logging.getLogger(__name__)


class TCartItem(TypedDict):
    product_id: int
    quantity: int


class TCartItemFull(TypedDict):
    product: Product
    quantity: int
    total_price: float
    total_sale_price: float


class TCartInfo(TypedDict):
    cart_items: list[TCartItemFull]
    total_price: float
    total_sale_price: float


class Cart:
    _key = "session_cart_key"

    def __init__(self, request) -> None:
        self._session = request.session
        self._request = request

        # If cart doesn't exist yet
        if self._key not in self._session:
            cart = self._session[self._key] = []
        else:
            # Get the current session key if it exists
            cart = self._session.get(self._key)

        # Make sure cart is available on all pages of site
        self._cart = cart

    def get_items(self) -> list[TCartItem]:
        """Get items Cart from session."""
        return self._cart

    def get_ids(self) -> list[int]:
        """Get products ids from the Cart"""
        return [item["product_id"] for item in self._cart]

    def get_item(self, product_id: int) -> TCartItem | None:
        """Get item by product id from the Cart"""
        try:
            filtered_items = [
                item for item in self._cart if item["product_id"] == product_id
            ]

            if len(filtered_items):
                return filtered_items[0]
            else:
                raise IndexError
        except Exception as e:
            logger.error(f"Failed to get Product #{product_id} from the Cart: {e}")

            return None

    def get_item_index(self, product_id: int) -> int:
        """Get item index by product id from the Cart"""
        try:
            item = self.get_item(product_id)

            if item is not None:
                return self._cart.index(item)
            else:
                raise IndexError
        except Exception as e:
            logger.error(f"Failed to get Product #{product_id} index in the Cart: {e}")

            return -1

    def add_item(self, product_id: int, quantity: int) -> bool:
        """
        Add an item to the cart.
        :param product_id:
        :param quantity:
        :return:
        """
        try:
            # Product already in the cart
            if product_id in self.get_ids():
                return False

            new_item: TCartItem = {"product_id": product_id, "quantity": quantity}

            # Update Cart
            self._cart.append(new_item)

            # Sync local Cart and Profile Cart
            success = self.sync()

            if success:
                return True
            else:
                raise Exception("Failed update Profile cart")
        except Exception as e:
            logger.error(f"Failed to add Product #{product_id} to the Cart: {e}")

            return False

    def delete_item(self, product_id: int) -> bool:
        """
        Delete an item from the cart.
        :param product_id:
        :return:
        """
        try:
            # Update cart
            item_index = self.get_item_index(product_id)

            del self._cart[item_index]

            # Sync local Cart and Profile Cart
            success = self.sync([product_id])

            if success:
                return True
            else:
                raise Exception("Failed update Profile cart")
        except Exception as e:
            logger.error(f"Failed to delete Product #{product_id} from the Cart: {e}")

            return False

    def update(self, data: list[TCartItem]) -> bool:
        """
        Update the cart.
        :param data:
        :return:
        """
        try:
            # Set key of Session Cart with new value
            self._cart = data

            # Sync local Cart and Profile Cart
            success = self.sync()

            if success:
                return True
            else:
                raise Exception("Failed update Profile cart")
        except Exception as e:
            logger.error(f"Failed to update Cart: {e}")

            return False

    def clean(self) -> bool:
        """
        Clean the cart.
        :return:
        """
        try:
            # Get ids products of Cart
            ids = self.get_ids()

            # Clean Cart
            self._cart = []

            # Sync local Cart and Profile Cart
            success = self.sync(ids_for_delete=ids)

            if success:
                return True
            else:
                raise Exception("Failed update Profile cart")
        except Exception as e:
            logger.error(f"Failed to clean the Cart: {e}")

            return False

    def get_items_from_profile(self) -> list[TCartItem]:
        """Get Cart value from profile model"""
        try:
            # Get User
            user = self._request.user

            if user.is_authenticated:
                # Get Profile
                profile = user.profile

                profile_cart_json = profile.cart_temporary

                if profile_cart_json:
                    return json.loads(profile_cart_json)
                else:
                    raise Exception("Field cart_temporary is blank or NULL")
            else:
                # If the user is not logged in, the profile cart is empty
                return []
        except Exception as e:
            logger.error(f"Failed to get Cart from Profile: {e}")

            return []

    def set_items_to_profile(self, data: list[TCartItem]) -> bool:
        """Set Cart value to profile model"""
        try:
            # Get User
            user = self._request.user

            if user.is_authenticated:
                # Get Profile
                profile = user.profile

                data_json = json.dumps(data)

                # Save new value
                profile.cart_temporary = data_json
                profile.save()

                return True
            else:
                # If the user is not logged in, we do not need to update the profile cart
                return True
        except Exception as e:
            logger.error(f"Failed to set items to profile from the Cart: {e}")

            return False

    def sync(self, ids_for_delete: list[int] | None = None) -> bool:
        """
        Compare the local version and the profile version of the Cart, then save the final version to the profile.
        :param ids_for_delete:
        :return:
        """
        try:
            # Get cart from Profile
            profile_cart = self.get_items_from_profile()

            # Local cart
            local_cart = self.get_items()

            # Compare two carts
            for p_c_i in profile_cart:
                l_c_i = self.get_item(p_c_i["product_id"])

                if not l_c_i and p_c_i["product_id"] not in (ids_for_delete or []):
                    local_cart.append(p_c_i)

            # Update Profile cart
            success = self.set_items_to_profile(local_cart)

            if success:
                # Set new value for key of Session Cart
                self._cart = self._session[self._key] = local_cart

                return True
            else:
                raise Exception("Failed update Profile cart")
        except Exception as e:
            logger.error(f"Failed to sync local Cart with Profile Cart: {e}")

            return False

    def get_full_info(self) -> TCartInfo:
        # Get Cart ids
        cart_ids = self.get_ids()

        # Get Products info related to Cart items
        products = Product.objects.filter(id__in=cart_ids)

        # Total Cart
        total_price = 0
        total_sale_price = 0

        # Create full Cart items
        cart_item_full = []
        for product in products:
            item = self.get_item(product.id)

            if item:
                if product.in_stock:
                    # Calculate total item price
                    total_item_price = product.price * item["quantity"]
                    # Without sale total item price and total item sale price are equal
                    total_item_sale_price = total_item_price

                    if product.sale_price:
                        total_item_sale_price = product.sale_price * item["quantity"]

                    # Add total item price to total cart price
                    total_price += total_item_price
                    # Add total item sale price to total cart sale price
                    total_sale_price += total_item_sale_price

                    # Combine full cart item dict
                    cart_item_full.append(
                        {
                            "product": product,
                            "quantity": item["quantity"],
                            "total_price": round(total_item_price, 2),
                            "total_sale_price": round(total_item_sale_price, 2),
                        }
                    )
                else:
                    # If Product is out of stock - remove it from the Cart
                    self.delete_item(product.id)

        return {
            "cart_items": cart_item_full,
            "total_price": round(total_price, 2),
            "total_sale_price": round(total_sale_price, 2),
        }

    def __len__(self):
        return len(self._cart)

    def __str__(self):
        return json.dumps(self._cart)
