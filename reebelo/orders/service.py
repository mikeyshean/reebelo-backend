import logging

from django.db import transaction

from reebelo.core.api.result import Result
from reebelo.core.exceptions import NotFoundError
from reebelo.products.api import ProductApi

from .models import Order

logger = logging.getLogger(__name__)


class OrderService:
    UPDATABLE_FIELDS = {"status", "product"}

    @staticmethod
    @transaction.atomic
    def create(product_id: str, quantity: int) -> Result:
        result = ProductApi.decrease_quantity(id=product_id, quantity=quantity)
        if not result.success:
            return result

        order = Order.objects.create(
            product_id=product_id, quantity=quantity, status=Order.PROCESSING
        )
        result.data = order
        return result

    @staticmethod
    def list():
        return Order.objects.all().order_by("name")

    @staticmethod
    def delete(id: str):
        try:
            Order.objects.get(id=id).delete()
        except Order.DoesNotExist:
            raise NotFoundError()
