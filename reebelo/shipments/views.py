import logging

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import TrackingCompanySerializer
from .service import TrackingCompanyService

logger = logging.getLogger(__name__)


class TrackingCompanyViewSet(ViewSet):
    def list(self, request):
        tracking_companies = TrackingCompanyService.list()
        serializer = TrackingCompanySerializer(tracking_companies, many=True)
        return Response(serializer.data)
