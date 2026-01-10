import logging

from subscribe.models import SubscribeProduct

# Logger
logger = logging.getLogger(__name__)


class Subscribe:
    def __init__(self, request):
        self._request = request

    def get_product_ids(self):
        """Get a list of subscribing product ids of current user"""
        if self._request.user.is_authenticated:
            product_ids = [
                s_p["product_id"]
                for s_p in SubscribeProduct.objects.filter(
                    user=self._request.user
                ).values("product_id")
            ]

            return product_ids

        return []

    def add_item(self, product_id: int) -> bool:
        """Add an item to the product subscription of current user"""
        if self._request.user.is_authenticated:
            try:
                subscribe_prod = SubscribeProduct.objects.create(
                    product_id=product_id,
                    user_id=self._request.user.id,
                )

                if subscribe_prod:
                    return True
                else:
                    raise Exception(
                        f"Failed creating Subscribe Product by product_id: {product_id}"
                    )
            except Exception as e:
                logger.error(e)

                return False

        return False

    def delete_item(self, product_id: int) -> bool:
        """Delete an item from the product subscription of current user"""
        if self._request.user.is_authenticated:
            try:
                subscribe_prod = SubscribeProduct.objects.get(
                    product_id=product_id,
                    user_id=self._request.user.id,
                )

                if subscribe_prod:
                    try:
                        unsubscribe_prod_id, *_ = subscribe_prod.delete()

                        return True
                    except Exception as e:
                        raise Exception(
                            f"Failed deleting Subscribe Product by product_id: {product_id}"
                        )
                else:
                    raise Exception(f"Failed to unsubscribe Product {product_id}")
            except Exception as e:
                logger.error(e)

                return False

        return False
