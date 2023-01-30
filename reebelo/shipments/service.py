import logging
from typing import Optional

from .models import Shipment, TrackingCompany

logger = logging.getLogger(__name__)


class ShipmentService:
    UPDATABLE_FIELDS = {
        "recipient_name",
        "tracking_number",
        "tracking_company_id",
        "order_id",
    }

    @staticmethod
    def get_by_order_id(order_id: str) -> Optional[Shipment]:
        return Shipment.objects.filter(order_id=order_id).first()

    @staticmethod
    def upsert(order_id: str, **kwargs):
        update_fields = []
        data = {}
        for field, value in kwargs.items():
            if field in ShipmentService.UPDATABLE_FIELDS:
                data[field] = value
                update_fields.append(field)

        return Shipment.objects.update_or_create(order_id=order_id, defaults=data)


class TrackingCompanyService:
    @staticmethod
    def list():
        return TrackingCompany.objects.all()
