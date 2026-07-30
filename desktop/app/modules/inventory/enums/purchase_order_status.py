from enum import Enum


class PurchaseOrderStatus(str, Enum):
    DRAFT = "Draft"
    ORDERED = "Ordered"
    PARTIALLY_RECEIVED = "Partially Received"
    RECEIVED = "Received"
    CANCELLED = "Cancelled"