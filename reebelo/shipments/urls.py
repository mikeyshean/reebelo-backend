from rest_framework.routers import SimpleRouter

from reebelo.shipments.views import ShipmentViewSet, TrackingCompanyViewSet

router = SimpleRouter(trailing_slash=False)
router.register(
    r"shipments/tracking-companies",
    TrackingCompanyViewSet,
    basename="tracking-companies",
)
router.register(r"shipments", ShipmentViewSet, basename="shipments")
