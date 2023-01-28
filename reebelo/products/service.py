from reebelo.core.exceptions import NotFoundError

from .models import Product


class ProductService:
    UPDATABLE_FIELDS = {"name", "price"}

    @staticmethod
    def create(name: str, price: float, quanitity: int):
        return Product.objects.create(name=name, price=price, quanitity=quanitity)

    @staticmethod
    def list():
        return Product.objects.all().order_by("name")

    @staticmethod
    def update(id: int, **kwargs):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise NotFoundError("Product not found")

        update_fields = []
        for field, value in kwargs.items():
            if field in ProductService.UPDATABLE_FIELDS:
                setattr(product, field, value)
                update_fields.append(field)

        product.save(update_fields=update_fields)
