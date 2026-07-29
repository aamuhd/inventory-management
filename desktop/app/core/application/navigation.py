from typing import Protocol


class Navigation(Protocol):

    def show_login(self) -> None:
        ...

    def show_dashboard(self) -> None:
        ...

    def show_categories(self) -> None:
        ...

    def show_products(self) -> None:
        ...

    def show_suppliers(self) -> None:
        ...

    def show_purchase_orders(self) -> None:
        ...

    def show_supplier_returns(self) -> None:
        ...