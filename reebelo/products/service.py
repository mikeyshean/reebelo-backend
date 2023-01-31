import logging

from django.db import transaction

from reebelo.core.exceptions import NotFoundError
from reebelo.products.exceptions import InsufficientQuantity

from .models import Product

logger = logging.getLogger(__name__)


class ProductService:
    UPDATABLE_FIELDS = {"name", "price"}
    QUANTITY_FIELDS = {"increase_quantity", "decrease_quantity"}

    @staticmethod
    def create(name: str, price: float, quantity: int):
        return Product.objects.create(name=name, price=price, quantity=quantity)

    @staticmethod
    def list(search: str):
        return Product.objects.filter(name__search=search).order_by("name")

    @staticmethod
    @transaction.atomic
    def update(id: str, **kwargs) -> Product:
        product = ProductService._get_product_for_update(id, **kwargs)

        update_fields = []
        ProductService._update_fields(product, update_fields, **kwargs)

        product.save(update_fields=update_fields)
        return product

    @staticmethod
    def delete(id: str):
        try:
            Product.objects.get(id=id).delete()
        except Product.DoesNotExist:
            raise NotFoundError()

    @staticmethod
    def _update_fields(product: Product, update_fields, **kwargs):
        """
        Updates fields directly by requested field name strs
        in kwargs or handles custom increase_quantity/decrease_quantity
        param in kwargs

        Args:
            kwargs (_type_): key, value fields to update
            product (Product): Instance of Product
            update_fields (_type_): _description_
        """
        for key, value in kwargs.items():
            if key in ProductService.UPDATABLE_FIELDS:
                setattr(product, key, value)
                update_fields.append(key)
            elif key in ProductService.QUANTITY_FIELDS:
                new_value = ProductService._get_adjusted_quantity(product, key, value)
                setattr(product, "quantity", new_value)
                update_fields.append("quantity")

    @staticmethod
    def _get_product_for_update(id: str, **kwargs) -> Product:
        """
        Checks params to see if we need to lock
        row for update of quantity before fetching

        Args:
            id (str): UUID of Product

        Raises:
            NotFoundError: Not found by id

        Returns:
            Product: Instance of Product
        """
        try:
            if ProductService._is_locking_update(**kwargs):
                return Product.objects.select_for_update().get(id=id)
            else:
                return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise NotFoundError("Product not found")

    @staticmethod
    def _get_adjusted_quantity(product: Product, action: str, value: int):
        if action == "increase_quantity":
            return product.quantity + value

        if action == "decrease_quantity":
            if product.quantity - value < 0:
                raise InsufficientQuantity()
            return max(product.quantity - value, 0)

    @staticmethod
    def _is_locking_update(**kwargs):
        for key in kwargs.keys():
            if key in ProductService.QUANTITY_FIELDS:
                return True
        return False
