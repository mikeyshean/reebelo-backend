from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDto:
    name: str
    price: float
    quantity: int
