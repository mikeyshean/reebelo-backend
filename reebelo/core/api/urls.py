from django.urls import include, path

from reebelo.orders.urls import router as order_router
from reebelo.products.urls import router as product_router
from reebelo.shipments.urls import router as shipment_router

urlpatterns = [
    path("", include(product_router.urls), name="products"),
    path("", include(order_router.urls), name="orders"),
    path("", include(shipment_router.urls), name="shipments"),
]
