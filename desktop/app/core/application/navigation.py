from typing import Protocol

from app.modules.sales.models.customer import Customer


class Navigation(Protocol):

    def show_login(self) -> None:
        ...

    def show_change_password(self) -> None:
        ...

    def show_password_recovery(self) -> None:
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

    def show_product_variants(self) -> None:
        ...

    def show_customers(self) -> None:
        ...

    def show_customer_detail(
        self,
        customer: Customer,
    ) -> None:
        ...

    def show_sales(self) -> None:
        ...

    def show_sales_returns(self) -> None:
        ...

    def show_reports(self) -> None:
        ...

    def show_users(self) -> None:
        ...

    def show_roles(self) -> None:
        ...

    def show_backup(self) -> None:
        ...

    def show_settings(self) -> None:
        ...