from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import QDate

from app.modules.inventory.ui.purchase_order_form import PurchaseOrderForm
from app.modules.inventory.ui.purchase_order_item_table import PurchaseOrderItemTable
from app.modules.inventory.ui.purchase_order_table import PurchaseOrderTable
from app.modules.inventory.ui.add_purchase_order_item_dialog import (
    AddPurchaseOrderItemDialog,
)
from app.modules.inventory.enums.purchase_order_status import PurchaseOrderStatus
from app.core.ui.base_window import BaseWindow


class PurchaseOrderWindow(BaseWindow):

    def __init__(
         self,
        purchase_order_service,
        supplier_service,
        variant_service,
    ):
        super().__init__()

        self._purchase_order_service = purchase_order_service
        self._supplier_service = supplier_service
        self._variant_service = variant_service

        self._selected_order = None
        self._selected_item = None

        self._build_ui()
        self._load_suppliers()
        self._load_purchase_orders()
        self._connect_signals()
        

    def _build_ui(self):

        self.setWindowTitle(
            "Purchase Orders",
        )

        layout = QVBoxLayout(self)

        self.form = PurchaseOrderForm()

        self.order_table = PurchaseOrderTable()

        self.item_table = PurchaseOrderItemTable()

        layout.addWidget(self.form)
        layout.addWidget(self.order_table)
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

        self.receive_button = QPushButton(
            "Receive Order",
        )

        self.add_item_button.setEnabled(False)
        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)
        self.receive_button.setEnabled(False)

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
            self.receive_button,
        )

        layout.addLayout(
            button_layout,
        )

        self.delete_button = QPushButton(
            "Delete Order",
        )

        self.delete_button.setEnabled(False)

        button_layout.addWidget(
            self.delete_button,
        )

        self.delete_button.clicked.connect(
            self._delete_purchase_order,
        )

    def _connect_signals(self):

        self.order_table.purchase_order_selected.connect(
            self._purchase_order_selected,
        )

        self.item_table.item_selected.connect(
            self._item_selected,
        )
        self.form.create_clicked.connect(
            self._create_purchase_order,
        )

        self.form.update_clicked.connect(
            self._update_purchase_order,
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
        self.receive_button.clicked.connect(
            self._receive_order,
        )

    def _load_suppliers(self):

        self.form.supplier_combo.clear()

        suppliers = self._supplier_service.get_all()

        for supplier in suppliers:

            self.form.supplier_combo.addItem(
                supplier.name,
                supplier.id,
            )

    def _load_purchase_orders(self):

        orders = self._purchase_order_service.get_all()

        self.order_table.load(
            orders,
        )

    def _purchase_order_selected(
        self,
        purchase_order,
    ):

        self._selected_order = purchase_order

        self.form.order_number_edit.setText(
            purchase_order.order_number,
        )

        self.form.notes_edit.setPlainText(
            purchase_order.notes or "",
        )

        index = self.form.supplier_combo.findData(
            purchase_order.supplier_id,
        )

        if index >= 0:
            self.form.supplier_combo.setCurrentIndex(
                index,
            )

        self.item_table.load(
            purchase_order.items,
        )

        self.add_item_button.setEnabled(True)
        self.receive_button.setEnabled(True)
        self.delete_button.setEnabled(True)


        self.form.create_button.setEnabled(False)
        self.form.update_button.setEnabled(True)

        self.form.order_date_edit.setDate(
            QDate(
                purchase_order.order_date.year,
                purchase_order.order_date.month,
                purchase_order.order_date.day,
            )
        )
        is_draft = (
            purchase_order.status == PurchaseOrderStatus.DRAFT
        )

        self.add_item_button.setEnabled(
            is_draft,
        )

        self.receive_button.setEnabled(
            is_draft,
        )

        self.delete_button.setEnabled(
            is_draft,
        )
        
    def _item_selected(
        self,
        item,
    ):

        self._selected_item = item

        if self._selected_order is None:
            return

        if (
            self._selected_order.status == PurchaseOrderStatus.DRAFT
        ):
            self.edit_item_button.setEnabled(True)
            self.delete_item_button.setEnabled(True)
        else:
            self.edit_item_button.setEnabled(False)
            self.delete_item_button.setEnabled(False)

    def _create_purchase_order(self):

        supplier_id = self.form.supplier_combo.currentData()
        order_number = self.form.order_number_edit.text().strip()
        order_date = self.form.order_date_edit.date().toPython()
        notes = self.form.notes_edit.toPlainText().strip()

        try:

            self._purchase_order_service.create(
                supplier_id=supplier_id,
                order_number=order_number,
                order_date=order_date,
                notes=notes,
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:
            self.show_error(
                str(error),
            )
    
    def _update_purchase_order(self):

        if self._selected_order is None:
            return

        supplier_id = self.form.supplier_combo.currentData()
        order_number = self.form.order_number_edit.text().strip()
        order_date = self.form.order_date_edit.date().toPython()
        notes = self.form.notes_edit.toPlainText().strip()

        try:

            self._purchase_order_service.update(
                purchase_order_id=self._selected_order.id,
                supplier_id=supplier_id,
                order_number=order_number,
                order_date=order_date,
                notes=notes,
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:
            self.show_error(
                str(error),
            )

    def _clear_form(self):

        self._selected_order = None
        self._selected_item = None

        self.form.clear()
        self.item_table.clear()

        self.add_item_button.setEnabled(False)
        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)
        self.receive_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def _delete_purchase_order(self):

        if self._selected_order is None:
            return

        try:

            self._purchase_order_service.delete(
                self._selected_order.id,
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:

            self.show_error(
                str(error),
            )

    def _add_item(self):

        if self._selected_order is None:
            return

        dialog = AddPurchaseOrderItemDialog(
            self._variant_service,
            self,
        )

        if dialog.exec():

            values = dialog.values()

            self._purchase_order_service.add_item(
                purchase_order_id=self._selected_order.id,
                variant_id=values["variant_id"],
                quantity=values["quantity"],
                unit_cost=values["cost_price"],
            )


            self._selected_order = (
                self._purchase_order_service.get_by_id(
                    self._selected_order.id,
                )
            )

            self.item_table.load(
                self._selected_order.items,
            )

    def _edit_item(self):

        if self._selected_item is None:
            return

        dialog = AddPurchaseOrderItemDialog(
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

        dialog.cost_price_spin.setValue(
            float(self._selected_item.unit_cost),
        )

        if dialog.exec():

            values = dialog.values()

            self._purchase_order_service.update_item(
                item_id=self._selected_item.id,
                quantity=values["quantity"],
                unit_cost=values["cost_price"],
            )

            if self._selected_order is None:
                return

            if self._selected_item is None:
                return

            self._selected_order = (
                self._purchase_order_service.get_by_id(
                    self._selected_order.id,
                )
            )

            self.item_table.load(
                self._selected_order.items,
            )


    def _delete_item(self):

        if self._selected_item is None:
            return
        """
        answer = QMessageBox.question(
            self,
            "Delete Item",
            "Delete selected item?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return
        """
        if not self.ask_confirmation(
            "Delete Item",
            "Delete selected item?",
        ):
            return

        self._purchase_order_service.delete_item(
            self._selected_item.id,
        )

        if self._selected_order is None:
            return

        if self._selected_item is None:
            return

        self._selected_order = (
            self._purchase_order_service.get_by_id(
                self._selected_order.id,
            )
        )

        self.item_table.load(
            self._selected_order.items,
        )

        self._selected_item = None

        self.edit_item_button.setEnabled(False)
        self.delete_item_button.setEnabled(False)

    def _receive_order(self):

        if self._selected_order is None:
            return

        answer = QMessageBox.question(
            self,
            "Receive Purchase Order",
            "Are you sure you want to receive this purchase order?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._purchase_order_service.receive(
                self._selected_order.id,
            )

            self._selected_order = (
                self._purchase_order_service.get_by_id(
                    self._selected_order.id,
                )
            )

            self._load_purchase_orders()

            self.item_table.load(
                self._selected_order.items,
            )

            self.receive_button.setEnabled(False)
            self.add_item_button.setEnabled(False)
            self.edit_item_button.setEnabled(False)
            self.delete_item_button.setEnabled(False)
            self.delete_button.setEnabled(False)

        except Exception as error:

            self.show_error(
                str(error),
            )