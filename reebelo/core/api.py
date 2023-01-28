from django.urls import include, path

from reebelo.products.urls import router as product_router

urlpatterns = [
    path("", include(product_router.urls), name="products"),
]
