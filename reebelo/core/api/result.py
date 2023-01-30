from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ErrorCode(str, Enum):
    INSUFFICIENT_QUANTITY = "insufficient_quantity"
    UNIQUE_OR_REQUIRED_FIELD = "unique_or_required"


@dataclass
class Error:
    code: ErrorCode
    message: str


@dataclass
class Result:
    success: bool
    error: Optional[Error] = None
    data: Any = None
