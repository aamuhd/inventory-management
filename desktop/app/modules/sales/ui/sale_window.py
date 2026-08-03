from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import QDate

from datetime import date
from typing import cast

from app.modules.sales.services.sale_service import SaleService
from app.modules.sales.services.customer_service import CustomerService
from app.modules.inventory.services.product_variant_service import ProductVariantService

from app.core.ui.base_window import BaseWindow
from app.modules.sales.ui.sale_form import SaleForm
from app.modules.sales.ui.sale_item_table import SaleItemTable
from app.modules.sales.ui.sale_table import SaleTable
from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.ui.add_sale_item_dialog import AddSaleItemDialog

#import traceback


class SaleWindow(BaseWindow):

    def __init__(
        self,
        sale_service: SaleService,
        customer_service: CustomerService,
        variant_service: ProductVariantService,
    ):
        super().__init__()

        self._sale_service = sale_service
        self._customer_service = customer_service
        self._variant_service = variant_service

        self._selected_sale = None
        self._selected_item = None

        self._build_ui()

        self._load_customers()
        self._load_sales()

        self._connect_signals()

    def _build_ui(self):
        self.setWindowTitle("Sales")

        layout = QVBoxLayout(self)

        self.form = SaleForm()

        self.sale_table = SaleTable()

        self.item_table = SaleItemTable()

        layout.addWidget(self.form)

        layout.addWidget(self.sale_table)

        layout.addWidget(self.item_table)

        button_layout = QHBoxLayout()

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
            "Complete Sale",
        )

        self.delete_button = QPushButton(
            "Delete Sale",
        )

        for button in (
            self.add_item_button,
            self.edit_item_button,
            self.delete_item_button,
            self.complete_button,
            self.delete_button,
        ):
            button.setEnabled(False)

            button_layout.addWidget(
                self.add_item_button,
            )

            button_layout.addWidget(
                self.edit_item_button,
            )

            button_layout.addWidget(
                self.delete_item_button,
            )

            button_layout.addWidget(
                self.complete_button,
            )

            button_layout.addWidget(
                self.delete_button,
            )

            layout.addLayout(
                button_layout,
            )

    def _connect_signals(self):
        self.sale_table.sale_selected.connect(
            self._sale_selected,
        )

        self.item_table.item_selected.connect(
            self._item_selected,
        )

        self.form.create_clicked.connect(
            self._create_sale,
        )

        self.form.update_clicked.connect(
            self._update_sale,
        )

        self.form.clear_clicked.connect(
            self._clear_form,
        )

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
            self._complete_sale,
        )

        self.delete_button.clicked.connect(
            self._delete_sale,
        )

    def _load_customers(self):
        self.form.customer_combo.clear()

        self.form.customer_combo.addItem(
            "Walk-in Customer",
            None,
        )

        customers = self._customer_service.get_all()

        for customer in customers:

            self.form.customer_combo.addItem(
                customer.name,
                customer.id,
            )

    def _load_sales(self):
        sales = self._sale_service.get_all()

        self.sale_table.load(
            sales,
        )

    def _create_sale(self):

        customer_id = self.form.customer_combo.currentData()

        invoice_number = (
            self.form.invoice_number_edit.text().strip()
        )

        """
        sale_date = (
            self.form.sale_date_edit.date().toPython()
        )
        """

        sale_date = cast(
            date,
            self.form.sale_date_edit.date().toPython(),
        )

        notes = (
            self.form.notes_edit.toPlainText().strip()
        )

        try:

            self._sale_service.create(
                customer_id=customer_id,
                invoice_number=invoice_number,
                sale_date=sale_date,
                notes=notes,
            )

            self._load_sales()

            self._clear_form()

            self.show_information(
                "Sale created successfully.",
            )
      
        except Exception as error:

            self.show_error(
                str(error),
            )
        
    
    def _update_sale(self):

        if self._selected_sale is None:
            return

        customer_id = self.form.customer_combo.currentData()

        invoice_number = (
            self.form.invoice_number_edit.text().strip()
        )
        """
        sale_date = (
            self.form.sale_date_edit.date().toPython()
        )
        """
        sale_date = cast(
            date,
            self.form.sale_date_edit.date().toPython(),
        )

        notes = (
            self.form.notes_edit.toPlainText().strip()
        )

        try:

            self._sale_service.update(
                sale_id=self._selected_sale.id,
                customer_id=customer_id,
                invoice_number=invoice_number,
                sale_date=sale_date,
                notes=notes,
            )

            self._load_sales()

            self._clear_form()

            self.show_information(
                "Sale updated successfully.",
            )
        

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _clear_form(self):

        self._selected_sale = None
        self._selected_item = None

        self.form.clear()

        self.form.create_button.setEnabled(True)
        self.form.update_button.setEnabled(False)

        self.item_table.clear()

        self.add_item_button.setEnabled(False)
        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)
        self.complete_button.setEnabled(False)
        self.delete_button.setEnabled(False)


        """ 
        """

    def _sale_selected(
        self,
        sale,
    ):

        self._selected_sale = sale

        self.form.invoice_number_edit.setText(
            sale.invoice_number,
        )

        self.form.notes_edit.setPlainText(
            sale.notes or "",
        )

        index = self.form.customer_combo.findData(
            sale.customer_id,
        )

        if index >= 0:
            self.form.customer_combo.setCurrentIndex(
                index,
            )
        else:
            self.form.customer_combo.setCurrentIndex(0)

        self.item_table.load(
            sale.items,
        )

        self.form.sale_date_edit.setDate(
            QDate(
                sale.sale_date.year,
                sale.sale_date.month,
                sale.sale_date.day,
            )
        )

        self.form.create_button.setEnabled(False)
        self.form.update_button.setEnabled(True)

        is_draft = (
            sale.status == SaleStatus.DRAFT
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

        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)

    def _item_selected(
        self,
        item,
    ):

        if self._selected_sale is None:
                    return
        
        self._selected_item = item

        ####

        if (
            self._selected_sale.status
            == SaleStatus.DRAFT
        ):
            self.edit_item_button.setEnabled(True)
            self.delete_item_button.setEnabled(True)
        else:
            self.edit_item_button.setEnabled(False)
            self.delete_item_button.setEnabled(False)

    def _delete_sale(self):

        if self._selected_sale is None:
            return

        if not self.ask_confirmation(
            "Delete Sale",
            "Delete selected sale?",
        ):
            return

        try:

            self._sale_service.delete(
                self._selected_sale.id,
            )

            self._load_sales()

            self._clear_form()

            self.show_information(
                "Sale deleted successfully.",
            )
        except Exception as error:
        
            self.show_error(
                str(error),
            )
        """
        except Exception:
            traceback.print_exc()
            raise    
        """
       
        

    def _add_item(self):

        if self._selected_sale is None:
            return

        dialog = AddSaleItemDialog(
            self._variant_service,
            self,
        )

        if dialog.exec():

            values = dialog.values()

            self._sale_service.add_item(
                sale_id=self._selected_sale.id,
                variant_id=values["variant_id"],
                quantity=values["quantity"],
                unit_price=values["unit_price"],
            )

            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id,
                )
            )

            self.item_table.load(
                self._selected_sale.items,
            )

            self._load_sales()

    def _edit_item(self):

        if self._selected_item is None:
            return

        dialog = AddSaleItemDialog(
            self._variant_service,
            self,
        )

        dialog.variant_combo.setCurrentIndex(
            dialog.variant_combo.findData(
                self._selected_item.product_variant_id,
            )
        )

        dialog.quantity_spin.setValue(
            self._selected_item.quantity,
        )

        dialog.unit_price_spin.setValue(
            float(
                self._selected_item.unit_price,
            )
        )

        if dialog.exec():

            values = dialog.values()

            self._sale_service.update_item(
                item_id=self._selected_item.id,
                quantity=values["quantity"],
                unit_price=values["unit_price"],
            )

            if self._selected_sale is None:
                return
            
            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id,
                )
            )

            self.item_table.load(
                self._selected_sale.items,
            )

            self._load_sales()

    def _delete_item(self):

        if self._selected_item is None:
            return

        if not self.ask_confirmation(
            "Delete Item",
            "Delete selected item?",
        ):
            return

        self._sale_service.delete_item(
            self._selected_item.id,
        )

        if self._selected_sale is None:
            return
        self._selected_sale = (
            self._sale_service.get_by_id(
                self._selected_sale.id,
            )
        )

        self.item_table.load(
            self._selected_sale.items,
        )

        self._selected_item = None

        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)

        self._load_sales()


    def _complete_sale(self):

        if self._selected_sale is None:
            return

        if not self.ask_confirmation(
            "Complete Sale",
            "Are you sure you want to complete this sale?",
        ):
            return

        try:
            
            self._sale_service.complete(
                self._selected_sale.id,
            )

            
            self._selected_sale = (
                self._sale_service.get_by_id(
                    self._selected_sale.id,
                )
            )

            self._load_sales()
            self._clear_form()
           

            self.add_item_button.setEnabled(False)
            self.edit_item_button.setEnabled(False)
            self.delete_item_button.setEnabled(False)
            self.complete_button.setEnabled(False)
            self.delete_button.setEnabled(False)

            self.form.update_button.setEnabled(False)

            self.show_information(
                "Sale completed successfully.",
            )
       
        except Exception as error:

            self.show_error(
                str(error),
            )
        