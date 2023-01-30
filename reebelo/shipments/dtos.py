from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TrackingCompanyDto:
    id: str
    name: str


@dataclass(frozen=True)
class ShipmentDto:
    order_id: str
    recipient_name: Optional[str]
    tracking_number: Optional[str]
    tracking_company: Optional[TrackingCompanyDto]
