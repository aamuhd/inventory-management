from __future__ import annotations

from collections.abc import Callable
from datetime import date
from decimal import Decimal
from typing import Any, cast

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow

from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)

from app.modules.sales.enums.sale_status import (
    SaleStatus,
)

from app.modules.sales.services.customer_service import (
    CustomerService,
)

from app.modules.sales.services.sale_service import (
    SaleService,
)

from app.modules.sales.ui.add_sale_item_dialog import (
    AddSaleItemDialog,
)

from app.modules.sales.ui.sale_form import (
    SaleForm,
)

from app.modules.sales.ui.sale_item_table import (
    SaleItemTable,
)

from app.modules.sales.ui.sale_table import (
    SaleTable,
)

from app.modules.sales.services.receipt_printer import (
    ReceiptPrinter,
)

from app.modules.sales.services.payment_service import (
    PaymentService,
)

from app.modules.sales.ui.payment_dialog import (
    PaymentDialog,
)

from app.modules.sales.ui.payment_table import (
    PaymentTable,
)


class SaleWindow(BaseWindow):

    def __init__(
        self,
        sale_service: SaleService,
        customer_service: CustomerService,
        variant_service: ProductVariantService,
        payment_service: PaymentService,
        refresh_product_variants: Callable[[], None],
        refresh_dashboard: Callable[[], None],
    ) -> None:

        super().__init__()

        self._sale_service = sale_service

        self._customer_service = customer_service

        self._variant_service = variant_service

        self._payment_service = payment_service

        self._refresh_product_variants = (
            refresh_product_variants
        )

        self._refresh_dashboard = (
            refresh_dashboard
        )

        self._selected_sale = None
        self._selected_item = None

        self._receipt_printer = ReceiptPrinter(
            self
        )

        self._build_ui()

        self._connect_signals()

        self._load_customers()

        self._load_sales()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Sales"
        )

        self.setObjectName(
            "saleWindow"
        )

        self.setMinimumSize(
            950,
            650,
        )

        self.resize(
            1100,
            750,
        )

        # =====================================================
        # Sale Form
        # =====================================================

        self.form = SaleForm()

        self.form.invoice_number_edit.setReadOnly(
            True
        )

        # =====================================================
        # Sale Table
        # =====================================================

        self.sale_table = SaleTable()

        # =====================================================
        # Sale Item Table
        # =====================================================

        self.item_table = SaleItemTable()

        self.item_table.setObjectName(
            "saleItemTable"
        )

        # =====================================================
        # Payment Summary
        # =====================================================

        self.total_label = QLabel(
            "Total: 0.00"
        )

        self.paid_label = QLabel(
            "Paid: 0.00"
        )

        self.balance_label = QLabel(
            "Balance: 0.00"
        )

        payment_summary_layout = QHBoxLayout()

        payment_summary_layout.addWidget(
            self.total_label
        )

        payment_summary_layout.addWidget(
            self.paid_label
        )

        payment_summary_layout.addWidget(
            self.balance_label
        )

        payment_summary_layout.addStretch()

        # =====================================================
        # Payment Table
        # =====================================================

        self.payment_table = PaymentTable()

        self.payment_table.setObjectName(
            "salePaymentTable"
        )

        # =====================================================
        # Action Buttons
        # =====================================================

        self.add_item_button = QPushButton(
            "Add Item"
        )

        self.add_item_button.setObjectName(
            "addItemButton"
        )

        self.edit_item_button = QPushButton(
            "Edit Item"
        )

        self.edit_item_button.setObjectName(
            "editItemButton"
        )

        self.delete_item_button = QPushButton(
            "Delete Item"
        )

        self.delete_item_button.setObjectName(
            "deleteItemButton"
        )

        self.complete_button = QPushButton(
            "Complete Sale"
        )

        self.complete_button.setObjectName(
            "completeButton"
        )

        self.print_receipt_button = QPushButton(
            "Print Receipt"
        )

        self.print_receipt_button.setObjectName(
            "printReceiptButton"
        )

        self.save_pdf_button = QPushButton(
            "Save Receipt as PDF"
        )

        self.save_pdf_button.setObjectName(
            "savePdfButton"
        )

        self.delete_button = QPushButton(
            "Delete Sale"
        )

        self.delete_button.setObjectName(
            "deleteSaleButton"
        )

        self.record_payment_button = QPushButton(
            "Record Payment"
        )

        self.record_payment_button.setObjectName(
            "recordPaymentButton"
        )

        self.record_payment_button.setEnabled(
            False
        )

        # -----------------------------------------------------
        # Initially disabled
        # -----------------------------------------------------

        for button in (
            self.add_item_button,
            self.edit_item_button,
            self.delete_item_button,
            self.complete_button,
            self.delete_button,
            self.print_receipt_button,
            self.save_pdf_button,
        ):

            button.setEnabled(
                False
            )

        # =====================================================
        # Button Layout
        # =====================================================

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.add_item_button
        )

        button_layout.addWidget(
            self.edit_item_button
        )

        button_layout.addWidget(
            self.delete_item_button
        )

        button_layout.addWidget(
            self.complete_button
        )

        button_layout.addWidget(
            self.record_payment_button
        )

        button_layout.addWidget(
            self.print_receipt_button
        )

        button_layout.addWidget(
            self.save_pdf_button
        )

        button_layout.addWidget(
            self.delete_button
        )

        # =====================================================
        # Main Layout
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
            self.form
        )

        layout.addWidget(
            self.sale_table
        )

        layout.addWidget(
            self.item_table
        )

        layout.addLayout(
            payment_summary_layout
        )

        layout.addWidget(
            self.payment_table
        )

        layout.addLayout(
            button_layout
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.sale_table.sale_selected.connect(
            self._sale_selected
        )

        self.item_table.item_selected.connect(
            self._item_selected
        )

        self.form.create_clicked.connect(
            self._create_sale
        )

        self.form.update_clicked.connect(
            self._update_sale
        )

        self.form.clear_clicked.connect(
            self._clear_form
        )

        self.add_item_button.clicked.connect(
            self._add_item
        )

        self.edit_item_button.clicked.connect(
            self._edit_item
        )

        self.delete_item_button.clicked.connect(
            self._delete_item
        )

        self.complete_button.clicked.connect(
            self._complete_sale
        )

        self.print_receipt_button.clicked.connect(
            self._print_receipt
        )

        self.save_pdf_button.clicked.connect(
            self._save_receipt_pdf
        )

        self.delete_button.clicked.connect(
            self._delete_sale
        )

        self.record_payment_button.clicked.connect(
            self._record_payment
        )

    # =========================================================
    # LOADING
    # =========================================================

    def _load_customers(self) -> None:

        self.form.customer_combo.clear()

        self.form.customer_combo.addItem(
            "Walk-in Customer",
            None,
        )

        customers = (
            self._customer_service.get_all()
        )

        for customer in customers:

            self.form.customer_combo.addItem(
                customer.name,
                customer.id,
            )

    def refresh_customers(self) -> None:
        """
        Refresh the customer dropdown.

        This is called by ApplicationController when a new
        customer is created from CustomerWindow.
        """

        current_customer_id = (
            self.form.customer_combo.currentData()
        )

        self._load_customers()

        if current_customer_id is None:

            self.form.customer_combo.setCurrentIndex(
                0
            )

            return

        index = (
            self.form.customer_combo.findData(
                current_customer_id
            )
        )

        if index >= 0:

            self.form.customer_combo.setCurrentIndex(
                index
            )

    def _load_sales(self) -> None:

        sales = (
            self._sale_service.get_all()
        )

        self.sale_table.load(
            sales
        )

    # =========================================================
    # SALE SELECTION
    # =========================================================

    def _sale_selected(
        self,
        sale,
    ) -> None:

        self._selected_sale = sale

        self.form.invoice_number_edit.setText(
            sale.invoice_number
        )

        self.form.notes_edit.setPlainText(
            sale.notes or ""
        )

        index = (
            self.form.customer_combo.findData(
                sale.customer_id
            )
        )

        if index >= 0:

            self.form.customer_combo.setCurrentIndex(
                index
            )

        else:

            self.form.customer_combo.setCurrentIndex(
                0
            )

        self.form.sale_date_edit.setDate(
            QDate(
                sale.sale_date.year,
                sale.sale_date.month,
                sale.sale_date.day,
            )
        )

        self.form.create_button.setEnabled(
            False
        )

        self.form.update_button.setEnabled(
            True
        )

        self.item_table.load(
            sale.items
        )

        is_draft = (
            sale.status
            == SaleStatus.DRAFT
        )

        self.add_item_button.setEnabled(
            is_draft
        )

        self.complete_button.setEnabled(
            is_draft
        )

        self.delete_button.setEnabled(
            is_draft
        )

        is_completed = (
            sale.status
            == SaleStatus.COMPLETED
        )

        self.print_receipt_button.setEnabled(
            is_completed
        )

        self.save_pdf_button.setEnabled(
            is_completed
        )

        self.edit_item_button.setEnabled(
            False
        )

        self.delete_item_button.setEnabled(
            False
        )

        self._selected_item = None

        self._load_payment_information()

    # =========================================================
    # ITEM SELECTION
    # =========================================================

    def _item_selected(
        self,
        item,
    ) -> None:

        if self._selected_sale is None:
            return

        self._selected_item = item

        is_draft = (
            self._selected_sale.status
            == SaleStatus.DRAFT
        )

        self.edit_item_button.setEnabled(
            is_draft
        )

        self.delete_item_button.setEnabled(
            is_draft
        )

    # =========================================================
    # CREATE
    # =========================================================

    def _create_sale(self) -> None:

        customer_id = (
            self.form.customer_combo.currentData()
        )

        sale_date = cast(
            date,
            self.form.sale_date_edit
            .date()
            .toPython(),
        )

        notes = (
            self.form.notes_edit
            .toPlainText()
            .strip()
        )

        try:

            sale = self._sale_service.create(
                customer_id=customer_id,
                sale_date=sale_date,
                notes=notes,
            )

            self._load_sales()

            self._sale_selected(
                sale
            )

            self.show_information(
                f"Sale created successfully.\n"
                f"Invoice: {sale.invoice_number}"
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # UPDATE
    # =========================================================

    def _update_sale(self) -> None:

        if self._selected_sale is None:
            return

        customer_id = (
            self.form.customer_combo.currentData()
        )

        sale_date = cast(
            date,
            self.form.sale_date_edit
            .date()
            .toPython(),
        )

        notes = (
            self.form.notes_edit
            .toPlainText()
            .strip()
        )

        try:

            self._sale_service.update(
                sale_id=self._selected_sale.id,
                customer_id=customer_id,
                sale_date=sale_date,
                notes=notes,
            )

            self._load_sales()

            self._clear_form()

            self.show_information(
                "Sale updated successfully."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def _clear_form(self) -> None:

        self._selected_sale = None
        self._selected_item = None

        self.form.clear()

        self.form.create_button.setEnabled(
            True
        )

        self.form.update_button.setEnabled(
            False
        )

        self.item_table.clear()

        self.add_item_button.setEnabled(
            False
        )

        self.edit_item_button.setEnabled(
            False
        )

        self.delete_item_button.setEnabled(
            False
        )

        self.complete_button.setEnabled(
            False
        )

        self.delete_button.setEnabled(
            False
        )

        self.print_receipt_button.setEnabled(
            False
        )

        self.save_pdf_button.setEnabled(
            False
        )

        self.payment_table.clear()

        self.total_label.setText(
            "Total: 0.00"
        )

        self.paid_label.setText(
            "Paid: 0.00"
        )

        self.balance_label.setText(
            "Balance: 0.00"
        )

        self.record_payment_button.setEnabled(
            False
        )

        self.sale_table.table.clearSelection()

    # =========================================================
    # DELETE SALE
    # =========================================================

    def _delete_sale(self) -> None:

        if self._selected_sale is None:
            return

        if not self.ask_confirmation(
            "Delete Sale",
            "Delete selected sale?",
        ):
            return

        try:

            self._sale_service.delete(
                self._selected_sale.id
            )

            self._load_sales()

            self._clear_form()

            self.show_information(
                "Sale deleted successfully."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # ADD ITEM
    # =========================================================

    def _add_item(self) -> None:

        if self._selected_sale is None:
            return

        try:

            dialog = AddSaleItemDialog(
                self._variant_service,
                self,
            )

            if not dialog.exec():
                return

            values = dialog.values()

            self._sale_service.add_item(
                sale_id=self._selected_sale.id,
                variant_id=values["variant_id"],
                quantity=values["quantity"],
                unit_price=values["unit_price"],
            )

            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id
                )
            )

            if self._selected_sale is None:

                self._clear_form()

                return

            self.item_table.load(
                self._selected_sale.items
            )

            self._load_sales()

            self._load_payment_information()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # EDIT ITEM
    # =========================================================

    def _edit_item(self) -> None:

        if self._selected_item is None:
            return

        dialog = AddSaleItemDialog(
            self._variant_service,
            self,
        )

        index = (
            dialog.variant_combo.findData(
                self._selected_item.product_variant_id
            )
        )

        if index >= 0:

            dialog.variant_combo.setCurrentIndex(
                index
            )

        dialog.quantity_spin.setValue(
            self._selected_item.quantity
        )

        dialog.unit_price_spin.setValue(
            float(
                self._selected_item.unit_price
            )
        )

        if not dialog.exec():
            return

        values = dialog.values()

        try:

            self._sale_service.update_item(
                item_id=self._selected_item.id,
                quantity=values["quantity"],
                unit_price=values["unit_price"],
            )

            if self._selected_sale is None:
                return

            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id
                )
            )

            if self._selected_sale is None:

                self._clear_form()

                return

            self.item_table.load(
                self._selected_sale.items
            )

            self._selected_item = None

            self.edit_item_button.setEnabled(
                False
            )

            self.delete_item_button.setEnabled(
                False
            )

            self._load_sales()

            self._load_payment_information()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # DELETE ITEM
    # =========================================================

    def _delete_item(self) -> None:

        if self._selected_item is None:
            return

        if not self.ask_confirmation(
            "Delete Item",
            "Delete selected item?",
        ):
            return

        try:

            self._sale_service.delete_item(
                self._selected_item.id
            )

            if self._selected_sale is None:
                return

            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id
                )
            )

            if self._selected_sale is None:

                self._clear_form()

                return

            self.item_table.load(
                self._selected_sale.items
            )

            self._selected_item = None

            self.edit_item_button.setEnabled(
                False
            )

            self.delete_item_button.setEnabled(
                False
            )

            self._load_sales()

            self._load_payment_information()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # COMPLETE SALE
    # =========================================================

    def _complete_sale(self) -> None:

        if self._selected_sale is None:
            return

        if not self.ask_confirmation(
            "Complete Sale",
            "Are you sure you want to complete this sale?",
        ):
            return

        try:

            sale_id = (
                self._selected_sale.id
            )

            self._sale_service.complete(
                sale_id
            )

            self._load_sales()

            self._refresh_product_variants()

            self._refresh_dashboard()

            self._selected_sale = (
                self._sale_service.get_by_id(
                    sale_id
                )
            )

            if self._selected_sale is not None:

                self._sale_selected(
                    self._selected_sale
                )

            self.show_information(
                "Sale completed successfully."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # PRINT RECEIPT
    # =========================================================

    def _print_receipt(self) -> None:

        if self._selected_sale is None:
            return

        if (
            self._selected_sale.status
            != SaleStatus.COMPLETED
        ):
            return

        try:

            sale = self._sale_service.get_by_id(
                self._selected_sale.id
            )

            settings = (
                self._sale_service.get_settings()
            )

            self._receipt_printer.print_receipt(
                sale,
                settings,
                payment_service=self._payment_service,
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # SAVE RECEIPT AS PDF
    # =========================================================

    def _save_receipt_pdf(self) -> None:

        if self._selected_sale is None:
            return

        if (
            self._selected_sale.status
            != SaleStatus.COMPLETED
        ):
            return

        try:

            sale = self._sale_service.get_by_id(
                self._selected_sale.id
            )

            settings = (
                self._sale_service.get_settings()
            )

            saved = (
                self._receipt_printer.save_pdf(
                    sale,
                    settings,
                    payment_service=self._payment_service,
                )
            )

            if saved:

                self.show_information(
                    "Receipt saved successfully."
                )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # LOAD PAYMENT INFORMATION
    # =========================================================

    def _load_payment_information(
        self,
    ) -> None:

        if self._selected_sale is None:

            self.payment_table.clear()

            self.total_label.setText(
                "Total: 0.00"
            )

            self.paid_label.setText(
                "Paid: 0.00"
            )

            self.balance_label.setText(
                "Balance: 0.00"
            )

            self.record_payment_button.setEnabled(
                False
            )

            return

        sale_id = self._selected_sale.id

        if sale_id is None:
            return

        payments = (
            self._payment_service.get_by_sale(
                sale_id
            )
        )

        paid = (
            self._payment_service.get_total_paid(
                sale_id
            )
        )

        balance = (
            self._payment_service.get_balance(
                sale_id
            )
        )

        self.payment_table.load(
            payments
        )

        self.total_label.setText(
            f"Total: {self._format_money(
                self._selected_sale.total_amount
            )}"
        )

        self.paid_label.setText(
            f"Paid: {self._format_money(
                paid
            )}"
        )

        self.balance_label.setText(
            f"Balance: {self._format_money(
                balance
            )}"
        )

        is_completed = (
            self._selected_sale.status
            == SaleStatus.COMPLETED
        )

        self.record_payment_button.setEnabled(
            is_completed
            and balance > Decimal("0.00")
        )

    # =========================================================
    # RECORD PAYMENT
    # =========================================================

    def _record_payment(self) -> None:

        if self._selected_sale is None:
            return

        if self._selected_sale.id is None:
            return

        if (
            self._selected_sale.status
            != SaleStatus.COMPLETED
        ):
            return

        dialog = PaymentDialog(
            sale_id=self._selected_sale.id,
            payment_service=self._payment_service,
            parent=self,
        )

        if not dialog.exec():
            return

        self._selected_sale = (
            self._sale_service.get_by_id(
                self._selected_sale.id
            )
        )

        if self._selected_sale is None:

            self._clear_form()

            return

        self._load_payment_information()

        self.show_information(
            "Payment recorded successfully."
        )

    # =========================================================
    # FORMAT MONEY
    # =========================================================

    @staticmethod
    def _format_money(
        amount: Decimal,
    ) -> str:

        return f"{amount:,.2f}"
