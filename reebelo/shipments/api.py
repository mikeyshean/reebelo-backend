from reebelo.core.exceptions import NotFoundError
from reebelo.shipments.dtos import ShipmentDto, TrackingCompanyDto
from reebelo.shipments.service import ShipmentService


class ShipmentApi:
    @staticmethod
    def upsert(orderId: str, **kwargs):
        shipment, _created = ShipmentService.upsert(order_id=orderId, **kwargs)
        tracking_company = shipment.tracking_company
        trackingCompanyDto = None
        if tracking_company:
            trackingCompanyDto = TrackingCompanyDto(
                id=tracking_company.id, name=tracking_company.name
            )

        return ShipmentDto(
            order_id=shipment.order_id,
            recipient_name=shipment.recipient_name or "",
            tracking_company=trackingCompanyDto,
            tracking_number=shipment.tracking_number or "",
        )

    @staticmethod
    def get_by_order_id(orderId: str):
        shipment = ShipmentService.get_by_order_id(order_id=orderId)
        if not shipment:
            raise NotFoundError()

        tracking_company = shipment.tracking_company
        trackingCompanyDto = None
        if tracking_company:
            trackingCompanyDto = TrackingCompanyDto(
                id=tracking_company.id, name=tracking_company.name
            )

        return ShipmentDto(
            order_id=shipment.order_id,
            recipient_name=shipment.recipient_name or "",
            tracking_company=trackingCompanyDto,
            tracking_number=shipment.tracking_number or "",
        )
