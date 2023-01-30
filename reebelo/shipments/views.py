import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ShipmentSerializer,
    TrackingCompanySerializer,
    UpsertShipmentSerializer,
)
from .service import ShipmentService, TrackingCompanyService

logger = logging.getLogger(__name__)


class TrackingCompanyViewSet(ViewSet):
    def list(self, request):
        tracking_companies = TrackingCompanyService.list()
        serializer = TrackingCompanySerializer(tracking_companies, many=True)
        return Response(serializer.data)


class ShipmentViewSet(ViewSet):
    def retrieve(self, request, pk):
        shipment = ShipmentService.get_by_order_id(order_id=pk)
        if not shipment:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """
        Creates or replaces order's shipment details
        """

        try:
            serializer = UpsertShipmentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            shipment, _created = ShipmentService.upsert(order_id=pk, **data)
            serializer = ShipmentSerializer(shipment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
