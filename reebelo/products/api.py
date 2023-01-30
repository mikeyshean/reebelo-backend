from reebelo.core.api.result import Result
from reebelo.products.dtos import ProductDto
from reebelo.products.exceptions import InsufficientQuantity

from .service import ProductService


class ProductApi:
    @staticmethod
    def decrease_quantity(id: str, quantity: int) -> ProductDto:
        try:
            product = ProductService.update(id=id, decrease_quantity=quantity)
            return Result(
                success=True,
                data=ProductDto(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=product.quantity,
                ),
            )
        except InsufficientQuantity as e:
            return Result(success=False, error=e.error)
