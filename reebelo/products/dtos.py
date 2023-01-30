from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDto:
    id: str
    name: str
    price: float
    quantity: int
