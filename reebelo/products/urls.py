from rest_framework.routers import SimpleRouter

from reebelo.products.views import ProductViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"products", ProductViewSet, basename="products")
