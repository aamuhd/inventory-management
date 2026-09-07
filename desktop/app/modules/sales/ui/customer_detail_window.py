from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, cast

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow

from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.models.customer import Customer
from app.modules.sales.services.payment_service import PaymentService
from app.modules.sales.services.sale_service import SaleService

from app.modules.settings.services.settings_service import (
    SettingsService,
)

from app.modules.sales.printing.customer_report_printer import (
    CustomerReportPrinter,
)


class CustomerDetailWindow(BaseWindow):

    def __init__(
        self,
        customer: Customer,
        sale_service: SaleService,
        payment_service: PaymentService,
        settings_service: SettingsService,
    ) -> None:

        super().__init__()

        self._customer = customer
        self._sale_service = sale_service
        self._payment_service = payment_service
        self._settings_service = settings_service

        self._customer_sales: list[Any] = []

        self._sale_paid: dict[Any, Decimal] = {}
        self._sale_balance: dict[Any, Decimal] = {}

        self._build_ui()
        self._connect_signals()

        self._load_customer_details()
        self._set_default_dates()
        self._generate_report()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Customer Details"
        )

        self.setObjectName(
            "customerDetailWindow"
        )

        self.setMinimumSize(
            900,
            600,
        )

        self.resize(
            1100,
            700,
        )

        # =====================================================
        # CUSTOMER INFORMATION
        # =====================================================

        customer_group = QGroupBox(
            "Customer Information"
        )

        customer_layout = QGridLayout()

        self.name_label = QLabel()
        self.phone_label = QLabel()
        self.email_label = QLabel()
        self.address_label = QLabel()

        customer_layout.addWidget(
            QLabel("Name:"),
            0,
            0,
        )

        customer_layout.addWidget(
            self.name_label,
            0,
            1,
        )

        customer_layout.addWidget(
            QLabel("Phone:"),
            0,
            2,
        )

        customer_layout.addWidget(
            self.phone_label,
            0,
            3,
        )

        customer_layout.addWidget(
            QLabel("Email:"),
            1,
            0,
        )

        customer_layout.addWidget(
            self.email_label,
            1,
            1,
        )

        customer_layout.addWidget(
            QLabel("Address:"),
            1,
            2,
        )

        customer_layout.addWidget(
            self.address_label,
            1,
            3,
        )

        customer_group.setLayout(
            customer_layout
        )

        # =====================================================
        # REPORT FILTER
        # =====================================================

        filter_group = QGroupBox(
            "Sales Report"
        )

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(
            QLabel("From:")
        )

        self.start_date_edit = QDateEdit()

        self.start_date_edit.setCalendarPopup(
            True
        )

        filter_layout.addWidget(
            self.start_date_edit
        )

        filter_layout.addWidget(
            QLabel("To:")
        )

        self.end_date_edit = QDateEdit()

        self.end_date_edit.setCalendarPopup(
            True
        )

        filter_layout.addWidget(
            self.end_date_edit
        )

        self.generate_button = QPushButton(
            "Generate Report"
        )

        self.generate_button.setObjectName(
            "customerDetailGenerateButton"
        )

        filter_layout.addWidget(
            self.generate_button
        )

        self.print_button = QPushButton(
            "Print Report"
        )

        self.print_button.setObjectName(
            "customerDetailPrintButton"
        )

        filter_layout.addWidget(
            self.print_button
        )

        self.save_pdf_button = QPushButton(
            "Save as PDF"
        )

        self.save_pdf_button.setObjectName(
            "customerDetailSavePdfButton"
        )

        filter_layout.addWidget(
            self.save_pdf_button
        )

        filter_layout.addStretch()

        filter_group.setLayout(
            filter_layout
        )

        # =====================================================
        # SUMMARY
        # =====================================================

        summary_group = QGroupBox(
            "Sales Summary"
        )

        summary_layout = QGridLayout()

        self.total_sales_label = QLabel()
        self.total_paid_label = QLabel()
        self.total_balance_label = QLabel()

        self.number_of_sales_label = QLabel()
        self.total_items_label = QLabel()
        self.average_sale_label = QLabel()

        summary_layout.addWidget(
            QLabel("Total Sales:"),
            0,
            0,
        )

        summary_layout.addWidget(
            self.total_sales_label,
            0,
            1,
        )

        summary_layout.addWidget(
            QLabel("Total Paid:"),
            0,
            2,
        )

        summary_layout.addWidget(
            self.total_paid_label,
            0,
            3,
        )

        summary_layout.addWidget(
            QLabel("Total Balance:"),
            0,
            4,
        )

        summary_layout.addWidget(
            self.total_balance_label,
            0,
            5,
        )

        summary_layout.addWidget(
            QLabel("Number of Sales:"),
            1,
            0,
        )

        summary_layout.addWidget(
            self.number_of_sales_label,
            1,
            1,
        )

        summary_layout.addWidget(
            QLabel("Items Purchased:"),
            1,
            2,
        )

        summary_layout.addWidget(
            self.total_items_label,
            1,
            3,
        )

        summary_layout.addWidget(
            QLabel("Average Sale:"),
            1,
            4,
        )

        summary_layout.addWidget(
            self.average_sale_label,
            1,
            5,
        )

        summary_group.setLayout(
            summary_layout
        )

        # =====================================================
        # SALES TABLE
        # =====================================================

        self.sales_table = QTableWidget()

        self.sales_table.setObjectName(
            "customerDetailSalesTable"
        )

        self.sales_table.setColumnCount(
            7
        )

        self.sales_table.setHorizontalHeaderLabels(
            [
                "Invoice",
                "Date",
                "Items",
                "Total",
                "Paid",
                "Balance",
                "Status",
            ]
        )

        self.sales_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.sales_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.sales_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.sales_table.setAlternatingRowColors(
            True
        )

        self.sales_table.setWordWrap(
            False
        )

        self.sales_table.horizontalHeader().setStretchLastSection(
            True
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(
            10
        )

        layout.addWidget(
            customer_group
        )

        layout.addWidget(
            filter_group
        )

        layout.addWidget(
            summary_group
        )

        layout.addWidget(
            self.sales_table
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.generate_button.clicked.connect(
            self._generate_report
        )

        self.print_button.clicked.connect(
            self._print_report
        )

        self.save_pdf_button.clicked.connect(
            self._save_pdf
        )

    # =========================================================
    # CUSTOMER DETAILS
    # =========================================================

    def _load_customer_details(self) -> None:

        self.name_label.setText(
            self._customer.name
        )

        self.phone_label.setText(
            self._customer.phone
            or "-"
        )

        self.email_label.setText(
            self._customer.email
            or "-"
        )

        self.address_label.setText(
            self._customer.address
            or "-"
        )

    # =========================================================
    # DEFAULT DATES
    # =========================================================

    def _set_default_dates(self) -> None:

        today = QDate.currentDate()

        start_date = today.addMonths(
            -1
        )

        self.start_date_edit.setDate(
            start_date
        )

        self.end_date_edit.setDate(
            today
        )

    # =========================================================
    # GET REPORT DATES
    # =========================================================

    def _get_report_dates(
        self,
    ) -> tuple[date, date] | None:

        start_date = cast(
            date,
            self.start_date_edit.date().toPython(),
        )

        end_date = cast(
            date,
            self.end_date_edit.date().toPython(),
        )

        if start_date > end_date:

            self.show_error(
                "Start date cannot be after end date."
            )

            return None

        return (
            start_date,
            end_date,
        )

    # =========================================================
    # NORMALIZE SALE DATE
    # =========================================================

    @staticmethod
    def _sale_date_as_date(
        sale_date: object,
    ) -> date | None:

        if isinstance(
            sale_date,
            datetime,
        ):
            return sale_date.date()

        if isinstance(
            sale_date,
            date,
        ):
            return sale_date

        return None

    # =========================================================
    # GET CUSTOMER SALES
    # =========================================================

    def _get_customer_sales(
        self,
        start_date: date,
        end_date: date,
    ) -> list[Any]:

        customer_id = self._customer.id

        if customer_id is None:
            return []

        sales = self._sale_service.get_all()

        customer_sales: list[Any] = []

        for sale in sales:

            if sale.customer_id != customer_id:
                continue

            if sale.status != SaleStatus.COMPLETED:
                continue

            sale_date = (
                self._sale_date_as_date(
                    sale.sale_date
                )
            )

            if sale_date is None:
                continue

            if sale_date < start_date:
                continue

            if sale_date > end_date:
                continue

            customer_sales.append(
                sale
            )

        customer_sales.sort(
            key=lambda sale: (
                self._sale_date_as_date(
                    sale.sale_date
                )
                or date.min
            ),
            reverse=True,
        )

        return customer_sales

    # =========================================================
    # GET SALE PAYMENT VALUES
    # =========================================================

    def _get_sale_paid(
        self,
        sale,
    ) -> Decimal:

        if sale.id is None:
            return Decimal("0.00")

        paid = self._payment_service.get_total_paid(
            sale.id
        )

        return Decimal(
            paid
        )

    # =========================================================
    # GET SALE BALANCE
    # =========================================================

    def _get_sale_balance(
        self,
        sale,
        paid: Decimal,
    ) -> Decimal:

        balance = (
            Decimal(sale.total_amount)
            - paid
        )

        if balance < Decimal("0.00"):
            return Decimal("0.00")

        return balance

    # =========================================================
    # CACHE PAYMENT VALUES
    # =========================================================

    def _load_payment_values(
        self,
        sales,
    ) -> None:

        self._sale_paid.clear()
        self._sale_balance.clear()

        for sale in sales:

            paid = self._get_sale_paid(
                sale
            )

            balance = self._get_sale_balance(
                sale,
                paid,
            )

            sale_key = sale.id

            self._sale_paid[
                sale_key
            ] = paid

            self._sale_balance[
                sale_key
            ] = balance

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    def _generate_report(self) -> None:

        dates = self._get_report_dates()

        if dates is None:
            return

        start_date, end_date = dates

        self._customer_sales = (
            self._get_customer_sales(
                start_date,
                end_date,
            )
        )

        self._load_payment_values(
            self._customer_sales
        )

        self._load_summary(
            self._customer_sales
        )

        self._load_sales_table(
            self._customer_sales
        )

    # =========================================================
    # PRINT REPORT
    # =========================================================

    def _print_report(self) -> None:

        dates = self._get_report_dates()

        if dates is None:
            return

        start_date, end_date = dates

        self._customer_sales = (
            self._get_customer_sales(
                start_date,
                end_date,
            )
        )

        self._load_payment_values(
            self._customer_sales
        )

        self._load_summary(
            self._customer_sales
        )

        self._load_sales_table(
            self._customer_sales
        )

        printer = CustomerReportPrinter(
            parent=self
        )

        settings = (
            self._settings_service.get()
        )

        total_sales = sum(
            (
                Decimal(sale.total_amount)
                for sale in self._customer_sales
            ),
            Decimal("0.00"),
        )

        total_paid = sum(
            self._sale_paid.get(
                sale.id,
                Decimal("0.00"),
            )
            for sale in self._customer_sales
        )

        total_balance = sum(
            self._sale_balance.get(
                sale.id,
                Decimal("0.00"),
            )
            for sale in self._customer_sales
        )

        printer.print_report(
            customer=self._customer,
            sales=self._customer_sales,
            start_date=start_date,
            end_date=end_date,
            settings=settings,
            total_sales=total_sales,
            total_paid=total_paid,
            total_balance=total_balance,
            sale_paid=self._sale_paid,
            sale_balance=self._sale_balance,
        )

    # =========================================================
    # SAVE AS PDF
    # =========================================================

    def _save_pdf(self) -> None:

        dates = self._get_report_dates()

        if dates is None:
            return

        start_date, end_date = dates

        self._customer_sales = (
            self._get_customer_sales(
                start_date,
                end_date,
            )
        )

        self._load_payment_values(
            self._customer_sales
        )

        self._load_summary(
            self._customer_sales
        )

        self._load_sales_table(
            self._customer_sales
        )

        printer = CustomerReportPrinter(
            parent=self
        )

        settings = (
            self._settings_service.get()
        )

        total_sales = sum(
            (
                Decimal(sale.total_amount)
                for sale in self._customer_sales
            ),
            Decimal("0.00"),
        )

        total_paid = sum(
            self._sale_paid.get(
                sale.id,
                Decimal("0.00"),
            )
            for sale in self._customer_sales
        )

        total_balance = sum(
            self._sale_balance.get(
                sale.id,
                Decimal("0.00"),
            )
            for sale in self._customer_sales
        )

        printer.save_pdf(
            customer=self._customer,
            sales=self._customer_sales,
            start_date=start_date,
            end_date=end_date,
            settings=settings,
            total_sales=total_sales,
            total_paid=total_paid,
            total_balance=total_balance,
            sale_paid=self._sale_paid,
            sale_balance=self._sale_balance,
        )

    # =========================================================
    # SUMMARY
    # =========================================================

    def _load_summary(
        self,
        sales,
    ) -> None:

        total_sales = Decimal(
            "0.00"
        )

        total_paid = Decimal(
            "0.00"
        )

        total_balance = Decimal(
            "0.00"
        )

        total_items = 0

        for sale in sales:

            total_sales += Decimal(
                sale.total_amount
            )

            total_paid += (
                self._sale_paid.get(
                    sale.id,
                    Decimal("0.00"),
                )
            )

            total_balance += (
                self._sale_balance.get(
                    sale.id,
                    Decimal("0.00"),
                )
            )

            for item in sale.items:
                total_items += item.quantity

        number_of_sales = len(
            sales
        )

        if number_of_sales:

            average_sale = (
                total_sales
                / number_of_sales
            )

        else:

            average_sale = Decimal(
                "0.00"
            )

        self.total_sales_label.setText(
            self._format_money(
                total_sales
            )
        )

        self.total_paid_label.setText(
            self._format_money(
                total_paid
            )
        )

        self.total_balance_label.setText(
            self._format_money(
                total_balance
            )
        )

        self.number_of_sales_label.setText(
            str(number_of_sales)
        )

        self.total_items_label.setText(
            str(total_items)
        )

        self.average_sale_label.setText(
            self._format_money(
                average_sale
            )
        )

    # =========================================================
    # SALES TABLE
    # =========================================================

    def _load_sales_table(
        self,
        sales,
    ) -> None:

        self.sales_table.setRowCount(
            len(sales)
        )

        for row, sale in enumerate(
            sales
        ):

            total_items = sum(
                item.quantity
                for item in sale.items
            )

            sale_date = (
                self._sale_date_as_date(
                    sale.sale_date
                )
            )

            date_text = (
                sale_date.strftime(
                    "%Y-%m-%d"
                )
                if sale_date is not None
                else "-"
            )

            paid = self._sale_paid.get(
                sale.id,
                Decimal("0.00"),
            )

            balance = self._sale_balance.get(
                sale.id,
                Decimal("0.00"),
            )

            if balance == Decimal("0.00"):

                status_text = "PAID"

            elif paid > Decimal("0.00"):

                status_text = "PARTIAL"

            else:

                status_text = "UNPAID"

            values = (
                sale.invoice_number,
                date_text,
                str(total_items),
                self._format_money(
                    sale.total_amount
                ),
                self._format_money(
                    paid
                ),
                self._format_money(
                    balance
                ),
                status_text,
            )

            for column, value in enumerate(
                values
            ):

                self.sales_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        value
                    ),
                )

    # =========================================================
    # FORMAT MONEY
    # =========================================================

    @staticmethod
    def _format_money(
        amount: Decimal,
    ) -> str:

        return f"{amount:,.2f}"
