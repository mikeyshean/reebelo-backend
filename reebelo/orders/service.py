import logging
from typing import Optional

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

        productDto = result.data
        order = Order.objects.create(
            product_id=productDto.id,
            quantity=quantity,
            status=Order.PROCESSING,
            amount_per_unit=productDto.price,
            amount_total=(productDto.price * quantity),
        )
        result.data = order
        return result

    @staticmethod
    def list():
        return (
            Order.objects.all()
            .select_related("product")
            .select_related("shipment")
            .select_related("shipment__tracking_company")
            .order_by("-created")
        )

    @staticmethod
    def get_by_id(id: str) -> Optional[Order]:
        return Order.objects.filter(id=id).first()

    @staticmethod
    def delete(id: str):
        try:
            Order.objects.get(id=id).delete()
        except Order.DoesNotExist:
            raise NotFoundError()
