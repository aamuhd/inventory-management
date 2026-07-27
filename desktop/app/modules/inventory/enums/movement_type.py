from enum import Enum


class MovementType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    ADJUSTMENT = "ADJUSTMENT"
    RETURN_IN = "RETURN_IN"
    RETURN_OUT = "RETURN_OUT"
    DAMAGED = "DAMAGED"
    TRANSFER = "TRANSFER"