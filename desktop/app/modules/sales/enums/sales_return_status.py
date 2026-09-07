from enum import Enum


class SalesReturnStatus(str, Enum):
    DRAFT = "Draft"
    COMPLETED = "Completed"