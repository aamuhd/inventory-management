from enum import Enum
from enum import StrEnum

"""
class MovementType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    ADJUSTMENT = "ADJUSTMENT"
    RETURN_IN = "RETURN_IN"
    RETURN_OUT = "RETURN_OUT"
    DAMAGED = "DAMAGED"
    TRANSFER = "TRANSFER"

"""

class MovementType(StrEnum):
    PURCHASE = "Purchase"
    SALE = "Sale"
    ADJUSTMENT = "Adjustment"
    RETURN_IN = "Return In"
    DAMAGED = "Damaged"
    SALES_RETURN = "Sales Return"

    RETURN_TO_SUPPLIER = "Return To Supplier"