from datetime import date

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtCore import QDate, Qt
from typing import cast


from app.modules.sales.services.sale_service import SaleService
from app.modules.sales.services.sale_item_service import SaleItemService
from app.modules.sales.services.sale_return_service import SalesReturnService


from app.modules.sales.ui.sale_return_form import SalesReturnForm
from app.modules.sales.ui.sales_return_table import SalesReturnTable
from app.modules.sales.ui.sale_return_item_table import SalesReturnItemTable

from app.modules.sales.enums.sales_return_status import SalesReturnStatus
from app.modules.sales.ui.add_sales_return_item_dialog import AddSalesReturnItemDialog
from app.core.ui.base_window import BaseWindow
from app.modules.sales.enums.sale_status import SaleStatus


class SalesReturnWindow(
    BaseWindow,
):

    def __init__(
        self,
        sales_return_service: SalesReturnService,
        sale_service: SaleService,
        sale_item_service: SaleItemService,
    ):
        super().__init__()

        self._sales_return_service = sales_return_service
        self._sale_service = sale_service
        self._sale_item_service = sale_item_service

        self._selected_return = None
        self._selected_item = None

        ###
        ###

        self._build_ui()
        self._connect_signals()

        self._load_sales()
        self._load_returns()

        self._clear_form()

    def _build_ui(self):

        self.setWindowTitle(
            "Sales Returns",
        )

        self.return_table = SalesReturnTable()

        self.form = SalesReturnForm()

        self.item_table = SalesReturnItemTable()

        #
        # Buttons
        #

        self.print_button = QPushButton(
            "Print",
        )
        self.print_button.setEnabled(False)

        self.add_item_button = QPushButton(
            "Add Item",
        )

        self.edit_item_button = QPushButton(
            "Edit Item",
        )

        self.delete_item_button = QPushButton(
            "Delete Item",
        )

        self.complete_button = QPushButton(
            "Complete Return",
        )

        self.delete_button = QPushButton(
            "Delete Return",
        )

        #
        # Button Layout
        #

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.add_item_button,
        )

        button_layout.addWidget(
            self.edit_item_button,
        )

        button_layout.addWidget(
            self.delete_item_button,
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.complete_button,
        )


        button_layout.addWidget(
            self.print_button,
        )

        button_layout.addWidget(
            self.delete_button,
        )

        #
        # Main Layout
        #

        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(self.form)
        layout.addWidget(self.return_table)
        layout.addWidget(self.item_table)
        layout.addLayout(button_layout)
            

    def _connect_signals(self):

        self.print_button.clicked.connect(
            self._print_return,
        )
        #
        # Tables
        #

        self.return_table.sales_return_selected.connect(
            self._return_selected,
        )

        self.item_table.item_selected.connect(
            self._item_selected,
        )

        #
        # Form
        #

        self.form.create_button.clicked.connect(
            self._create,
        )

        self.form.update_button.clicked.connect(
            self._update,
        )

        self.form.clear_button.clicked.connect(
            self._clear_form,
        )

        #
        # Buttons
        #

        self.add_item_button.clicked.connect(
            self._add_item,
        )

        self.edit_item_button.clicked.connect(
            self._edit_item,
        )

        self.delete_item_button.clicked.connect(
            self._delete_item,
        )

        self.complete_button.clicked.connect(
            self._complete_return,
        )

        self.delete_button.clicked.connect(
            self._delete,
        )
        self.form.sale_combo.currentIndexChanged.connect(
            self._sale_changed,
        )

    def _load_sales(self):

        current = self.form.sale_combo.currentData()

        self.form.sale_combo.clear()

        sales = self._sale_service.get_all()

        for sale in sales:

            if sale.status != SaleStatus.COMPLETED:
                continue
            customer = (
                sale.customer.name
                if sale.customer
                else "Walk-in Customer"
            )

            text = (
                f"{sale.invoice_number}"
                f" - {customer}"
            )

            self.form.sale_combo.addItem(
                text,
                sale.id,
            )

        index = self.form.sale_combo.findData(
            current,
        )

        if index >= 0:
            self.form.sale_combo.setCurrentIndex(
                index,
            )

        self.form.return_number_edit.setText(
            self._sales_return_service.generate_return_number()
        )

    def _load_returns(self):

        returns = (
            self._sales_return_service.get_all()
        )
        self.return_table.load(
            returns,
        )

    def _create(self):

        sale_id = self.form.sale_combo.currentData()

        if sale_id is None:

            self.show_error(
                "Please select a sale.",
            )

            return

        try:
            return_date = cast(
                date,
                self.form.return_date_edit.date().toPython(),
            )

            sales_return = (
                self._sales_return_service.create(
                    sale_id=sale_id,
                    return_date=return_date,
                    reason=self.form.reason_edit.toPlainText().strip() or None,
                )
            )

            self._selected_return = (
                self._sales_return_service.get_by_id(
                    sales_return.id,
                )
            )

            self.form.status_edit.setText(
                self._selected_return.status.value,
            )

            self._load_returns()

            self.return_table.select_return(
                self._selected_return.id,
            )

            self.form.create_button.setEnabled(
                False,
            )

            self.form.update_button.setEnabled(
                True,
            )

            self.add_item_button.setEnabled(
                True,
            )

            self.complete_button.setEnabled(
                True,
            )

            self.delete_button.setEnabled(
                True,
            )

            self.show_information(
                "Sales return created successfully.",
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _return_selected(
        self,
        sales_return,
    ):

        self._selected_return = sales_return

        sale = sales_return.sale

        index = self.form.sale_combo.findData(
            sale.id,
        )

        if index >= 0:

            self.form.sale_combo.setCurrentIndex(
                index,
            )

        self.form.return_number_edit.setText(
            sales_return.return_number,
        )

        self.form.status_edit.setText(
            sales_return.status.value,
        )

        self.form.reason_edit.setPlainText(
            sales_return.reason or "",
        )

        self.form.return_date_edit.setDate(
            QDate(
                sales_return.return_date.year,
                sales_return.return_date.month,
                sales_return.return_date.day,
            )
        )

        self.item_table.load(
            sales_return.items,
        )

        self.form.create_button.setEnabled(
            False,
        )

        self.form.update_button.setEnabled(
            True,
        )

        is_draft = (
            sales_return.status
            == SalesReturnStatus.DRAFT
        )

        self.add_item_button.setEnabled(
            is_draft,
        )

        self.complete_button.setEnabled(
            is_draft,
        )

        self.delete_button.setEnabled(
            is_draft,
        )

        self.edit_item_button.setEnabled(
            False,
        )

        self.delete_item_button.setEnabled(
            False,
        )
        self.form.sale_combo.setEnabled(False)

        self.print_button.setEnabled(
            sales_return.status == SalesReturnStatus.COMPLETED,
        )

    def _clear_form(self):

        self._selected_return = None
        self._selected_item = None

        self.form.clear()

        self.form.return_number_edit.setText(
            self._sales_return_service.generate_return_number(),
        )

        self.item_table.clear()

        self.form.create_button.setEnabled(
            True,
        )

        self.form.update_button.setEnabled(
            False,
        )

        self.add_item_button.setEnabled(
            False,
        )

        self.edit_item_button.setEnabled(
            False,
        )

        self.delete_item_button.setEnabled(
            False,
        )

        self.complete_button.setEnabled(
            False,
        )

        self.delete_button.setEnabled(
            False,
        )

        self.form.sale_combo.setEnabled(True)
        self.print_button.setEnabled(False)

    def _item_selected(
        self,
        item,
    ):

        self._selected_item = item

        is_draft = (
            self._selected_return is not None
            and self._selected_return.status
            == SalesReturnStatus.DRAFT
        )

        self.edit_item_button.setEnabled(
            is_draft,
        )

        self.delete_item_button.setEnabled(
            is_draft,
        )

    def _add_item(self):

        if self._selected_return is None:
            return

        dialog = AddSalesReturnItemDialog(
            sale_item_service=self._sale_item_service,
            sale_id=self._selected_return.sale_id,
            parent=self,
        )

        if dialog.exec():

            values = dialog.values()

            try:

                self._sales_return_service.add_item(
                    sales_return_id=self._selected_return.id,
                    sale_item_id=values["sale_item_id"],
                    quantity=values["quantity"],
                )


                #
                # Reload selected return
                #
                self._selected_return = (
                    self._sales_return_service.get_by_id(
                        self._selected_return.id,
                    )
                )

                #
                # Reload table
                #
                self.item_table.load(
                    self._selected_return.items,
                )

                #
                # Reload return list
                #
                self._load_returns()

                self.show_information(
                    "Item added successfully.",
                )

            except Exception as error:

                self.show_error(
                    str(error),
                )

    def _edit_item(self):

        if self._selected_item is None:
            return

        if self._selected_return is None:
            return

        dialog = AddSalesReturnItemDialog(
            sale_item_service=self._sale_item_service,
            sale_id=self._selected_return.sale_id,
            parent=self,
        )

        dialog.set_quantity(
            self._selected_item.quantity,
        )

        if dialog.exec():

            values = dialog.values()

            try:

                self._sales_return_service.update_item(
                    return_item_id=self._selected_item.id,
                    quantity=values["quantity"],
                )

                self._selected_return = (
                    self._sales_return_service.get_by_id(
                        self._selected_return.id,
                    )
                )

                self.item_table.load(
                    self._selected_return.items,
                )

                self._load_returns()

                self.show_information(
                    "Item updated successfully.",
                )

            except Exception as error:

                self.show_error(
                    str(error),
                )

    def _delete_item(self):

        if self._selected_item is None:
            return

        if not self.ask_confirmation(
            "Delete Item",
            "Are you sure you want to delete this item?",
        ):
            return

        try:

            self._sales_return_service.delete_item(
                self._selected_item.id,
            )

            if self._selected_return is None:
                return

            self._selected_return = (
                self._sales_return_service.get_by_id(
                    self._selected_return.id,
                )
            )

            self.item_table.load(
                self._selected_return.items,
            )

            self._load_returns()
            self._selected_item = None
            self.edit_item_button.setEnabled(False)
            self.delete_item_button.setEnabled(False)

            self.show_information(
                "Item deleted successfully.",
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _update(self):

        if self._selected_return is None:
            return

        try:

            return_date = cast(
                date,
                self.form.return_date_edit.date().toPython(),
            )

            self._sales_return_service.update(
                sales_return_id=self._selected_return.id,
                return_date=return_date,
                reason=self.form.reason_edit.toPlainText().strip() or None,
            )

            self._selected_return = (
                self._sales_return_service.get_by_id(
                    self._selected_return.id,
                )
            )

            self._load_returns()

            self.return_table.select_return(
                self._selected_return.id,
            )

            self.show_information(
                "Sales return updated successfully.",
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _complete_return(self):

        if self._selected_return is None:
            return

        if not self.ask_confirmation(
            "Complete Return",
            "Are you sure you want to complete this return?",
        ):
            return

        try:
            
            self._sales_return_service.complete(
                self._selected_return.id,
            )

            # Reload the updated return
            self._selected_return = (
                self._sales_return_service.get_by_id(
                    self._selected_return.id,
                )
            )

            # Reload the table
            self._load_returns()

            # Keep the completed return selected
            self.return_table.select_return(
                self._selected_return.id,
            )

            self.show_information(
                "Sales return completed successfully.",
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _delete(self):

        if self._selected_return is None:
            return

        if not self.ask_confirmation(
            "Delete Return",
            "Delete selected return?",
        ):
            return

        try:

            self._sales_return_service.delete(
                self._selected_return.id,
            )

            self._load_returns()

            self._clear_form()

            self.show_information(
                "Sales return deleted successfully.",
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _sale_changed(self):

        sale_id = self.form.sale_combo.currentData()

        if sale_id is None:
            self.form.customer_edit.clear()
            return

        sale = self._sale_service.get_by_id(sale_id)

        if sale.customer:
            self.form.customer_edit.setText(
                sale.customer.name,
            )
        else:
            self.form.customer_edit.setText(
                "Walk-in Customer",
            )

    def _print_return(self):

        if self._selected_return is None:
            return

        sales_return = self._selected_return

        lines = []

        lines.append("========== SALES RETURN ==========")
        lines.append(f"Return No : {sales_return.return_number}")
        lines.append(f"Invoice   : {sales_return.sale.invoice_number}")

        customer = (
            sales_return.sale.customer.name
            if sales_return.sale.customer
            else "Walk-in Customer"
        )

        lines.append(f"Customer  : {customer}")
        lines.append(f"Date      : {sales_return.return_date}")
        lines.append("")

        lines.append("Items")
        lines.append("--------------------------------")

        for item in sales_return.items:

            variant = item.sale_item.product_variant

            subtotal = (
                item.quantity * item.unit_price
            )

            lines.append(
                f"{variant.product.name}"
            )

            lines.append(
                f"  {variant.length} yards"
            )

            lines.append(
                f"  Qty: {item.quantity}"
            )

            lines.append(
                f"  Price: {item.unit_price}"
            )

            lines.append(
                f"  Subtotal: {subtotal}"
            )

            lines.append("")

        lines.append("--------------------------------")
        lines.append(
            f"TOTAL: {sales_return.total_amount}"
        )

        self.show_information(
            "\n".join(lines),
        )