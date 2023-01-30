from reebelo.core.api.result import Result
from reebelo.products.exceptions import InsufficientQuantity

from .service import ProductService


class ProductApi:
    @staticmethod
    def decrease_quantity(id: str, quantity: int):
        try:
            ProductService.update(id=id, decrease_quantity=quantity)
            return Result(success=True)
        except InsufficientQuantity as e:
            return Result(success=False, error=e.error)
