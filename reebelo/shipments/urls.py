from rest_framework.routers import SimpleRouter

from reebelo.shipments.views import TrackingCompanyViewSet

router = SimpleRouter(trailing_slash=False)
router.register(
    r"shipments/tracking-companies",
    TrackingCompanyViewSet,
    basename="tracking-companies",
)
