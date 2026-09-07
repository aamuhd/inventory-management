from dataclasses import dataclass

from app.modules.sales.models.sale_item import SaleItem


@dataclass
class ReturnableSaleItem:
    sale_item: SaleItem
    sold_quantity: int
    returned_quantity: int
    available_quantity: int