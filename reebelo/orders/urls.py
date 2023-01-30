from rest_framework.routers import SimpleRouter

from reebelo.orders.views import OrderViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"orders", OrderViewSet, basename="orders")
