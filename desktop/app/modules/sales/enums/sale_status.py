from enum import Enum


class SaleStatus(str, Enum):
    DRAFT = "Draft"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"