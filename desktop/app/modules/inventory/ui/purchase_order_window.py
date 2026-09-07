from __future__ import annotations
from collections.abc import Callable

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow

from app.modules.inventory.enums.purchase_order_status import (
    PurchaseOrderStatus,
)

from app.modules.inventory.ui.purchase_order_form import (
    PurchaseOrderForm,
)

from app.modules.inventory.ui.purchase_order_table import (
    PurchaseOrderTable,
)

from app.modules.inventory.ui.purchase_order_item_table import (
    PurchaseOrderItemTable,
)

from app.modules.inventory.ui.add_purchase_order_item_dialog import (
    AddPurchaseOrderItemDialog,
)


class PurchaseOrderWindow(BaseWindow):

    def __init__(
        self,
        purchase_order_service,
        supplier_service,
        variant_service,
        refresh_dashboard: Callable[[], None]
    ) -> None:

        super().__init__()

        self._purchase_order_service = (
            purchase_order_service
        )

        self._supplier_service = (
            supplier_service
        )

        self._variant_service = (
            variant_service
        )

        self._refresh_dashboard = (
            refresh_dashboard
        )

        self._selected_order = None

        self._selected_item = None

        self._build_ui()

        self._connect_signals()

        self._load_suppliers()

        self._load_purchase_orders()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Purchase Orders"
        )

        self.setObjectName(
            "purchaseOrderWindow"
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
        # Purchase Order Form
        # =====================================================

        self.form = PurchaseOrderForm()

        self.form.setObjectName(
            "purchaseOrderForm"
        )

        # =====================================================
        # Purchase Order Table
        # =====================================================

        self.order_table = PurchaseOrderTable()

        self.order_table.setObjectName(
            "purchaseOrderTable"
        )

        # =====================================================
        # Purchase Order Items
        # =====================================================

        self.item_table = PurchaseOrderItemTable()

        self.item_table.setObjectName(
            "purchaseOrderItemTable"
        )

        # =====================================================
        # Item Buttons
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

        self.receive_button = QPushButton(
            "Receive Order"
        )

        self.receive_button.setObjectName(
            "receiveButton"
        )

        # -----------------------------------------------------
        # Initially disabled
        # -----------------------------------------------------

        self.add_item_button.setEnabled(
            False
        )

        self.edit_item_button.setEnabled(
            False
        )

        self.delete_item_button.setEnabled(
            False
        )

        self.receive_button.setEnabled(
            False
        )

        # =====================================================
        # Item Button Layout
        # =====================================================

        item_button_layout = QHBoxLayout()

        item_button_layout.setSpacing(
            10
        )

        item_button_layout.addWidget(
            self.add_item_button
        )

        item_button_layout.addWidget(
            self.edit_item_button
        )

        item_button_layout.addWidget(
            self.delete_item_button
        )

        item_button_layout.addWidget(
            self.receive_button
        )

        # =====================================================
        # Delete Order
        # =====================================================

        self.delete_button = QPushButton(
            "Delete Order"
        )

        self.delete_button.setObjectName(
            "deleteOrderButton"
        )

        self.delete_button.setEnabled(
            False
        )

        # =====================================================
        # Main Layout
        # =====================================================

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        main_layout.setSpacing(
            10
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        main_layout.addWidget(
            self.form
        )

        # -----------------------------------------------------
        # Purchase Orders
        # -----------------------------------------------------

        main_layout.addWidget(
            self.order_table,
            1,
        )

        # -----------------------------------------------------
        # Purchase Order Items
        # -----------------------------------------------------

        main_layout.addWidget(
            self.item_table,
            1,
        )

        # -----------------------------------------------------
        # Item buttons
        # -----------------------------------------------------

        main_layout.addLayout(
            item_button_layout
        )

        # -----------------------------------------------------
        # Delete order
        # -----------------------------------------------------

        main_layout.addWidget(
            self.delete_button
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.form.create_clicked.connect(
            self._create_purchase_order
        )

        self.form.update_clicked.connect(
            self._update_purchase_order
        )

        self.form.clear_clicked.connect(
            self._clear_form
        )

        self.order_table.purchase_order_selected.connect(
            self._purchase_order_selected
        )

        self.item_table.item_selected.connect(
            self._item_selected
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

        self.receive_button.clicked.connect(
            self._receive_order
        )

        self.delete_button.clicked.connect(
            self._delete_purchase_order
        )

    # =========================================================
    # LOADING
    # =========================================================

    def _load_suppliers(self) -> None:

        self.form.supplier_combo.clear()

        suppliers = (
            self._supplier_service.get_all()
        )

        for supplier in suppliers:

            if supplier.id is None:
                continue

            self.form.supplier_combo.addItem(
                supplier.name,
                supplier.id,
            )

        # -----------------------------------------------------
        # Select the first supplier automatically.
        # -----------------------------------------------------

        if self.form.supplier_combo.count() > 0:

            self.form.supplier_combo.setCurrentIndex(
                0
            )

        else:

            self.form.supplier_combo.setCurrentIndex(
                -1
            )

    def _load_purchase_orders(self) -> None:

        orders = (
            self._purchase_order_service.get_all()
        )

        self.order_table.load(
            orders
        )

    # =========================================================
    # PURCHASE ORDER SELECTION
    # =========================================================

    def _purchase_order_selected(
        self,
        purchase_order,
    ) -> None:

        self._selected_order = (
            purchase_order
        )

        self.form.order_number_edit.setText(
            purchase_order.order_number
        )

        self.form.notes_edit.setPlainText(
            purchase_order.notes or ""
        )

        index = (
            self.form.supplier_combo.findData(
                purchase_order.supplier_id
            )
        )

        if index >= 0:

            self.form.supplier_combo.setCurrentIndex(
                index
            )

        self.form.order_date_edit.setDate(
            QDate(
                purchase_order.order_date.year,
                purchase_order.order_date.month,
                purchase_order.order_date.day,
            )
        )

        self.form.set_edit_mode()

        # -----------------------------------------------------
        # Load items
        # -----------------------------------------------------

        self.item_table.load(
            purchase_order.items
        )

        # -----------------------------------------------------
        # Draft permissions
        # -----------------------------------------------------

        is_draft = (
            purchase_order.status
            == PurchaseOrderStatus.DRAFT
        )

        self.add_item_button.setEnabled(
            is_draft
        )

        self.receive_button.setEnabled(
            is_draft
        )

        self.delete_button.setEnabled(
            is_draft
        )

        self.edit_item_button.setEnabled(
            False
        )

        self.delete_item_button.setEnabled(
            False
        )

        self._selected_item = None

    # =========================================================
    # ITEM SELECTION
    # =========================================================

    def _item_selected(
        self,
        item,
    ) -> None:

        self._selected_item = item

        if self._selected_order is None:
            return

        is_draft = (
            self._selected_order.status
            == PurchaseOrderStatus.DRAFT
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

    def _create_purchase_order(
        self,
    ) -> None:

        supplier_id = (
            self.form.supplier_combo.currentData()
        )

        order_number = (
            self.form.order_number_edit
            .text()
            .strip()
        )

        order_date = (
            self.form.order_date_edit
            .date()
            .toPython()
        )

        notes = (
            self.form.notes_edit
            .toPlainText()
            .strip()
        )

        try:

            self._purchase_order_service.create(
                supplier_id=supplier_id,
                order_number=order_number,
                order_date=order_date,
                notes=notes,
            )

            self.show_information(
                "Purchase order created successfully."
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # UPDATE
    # =========================================================

    def _update_purchase_order(
        self,
    ) -> None:

        if self._selected_order is None:
            return

        supplier_id = (
            self.form.supplier_combo.currentData()
        )

        order_number = (
            self.form.order_number_edit
            .text()
            .strip()
        )

        order_date = (
            self.form.order_date_edit
            .date()
            .toPython()
        )

        notes = (
            self.form.notes_edit
            .toPlainText()
            .strip()
        )

        try:

            self._purchase_order_service.update(
                purchase_order_id=(
                    self._selected_order.id
                ),
                supplier_id=supplier_id,
                order_number=order_number,
                order_date=order_date,
                notes=notes,
            )

            self.show_information(
                "Purchase order updated successfully."
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def _clear_form(self) -> None:

        self._selected_order = None

        self._selected_item = None

        self.form.clear()

        # -----------------------------------------------------
        # Keep suppliers available after clearing the form.
        # -----------------------------------------------------

        self._load_suppliers()

        self.form.set_create_mode()

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

        self.receive_button.setEnabled(
            False
        )

        self.delete_button.setEnabled(
            False
        )

        self.order_table.clearSelection()

    # =========================================================
    # DELETE PURCHASE ORDER
    # =========================================================

    def _delete_purchase_order(
        self,
    ) -> None:

        if self._selected_order is None:
            return

        if not self.ask_confirmation(
            "Delete Purchase Order",
            (
                "Are you sure you want to delete "
                f'"{self._selected_order.order_number}"?'
            ),
        ):
            return

        try:

            self._purchase_order_service.delete(
                self._selected_order.id
            )

            self.show_information(
                "Purchase order deleted successfully."
            )

            self._load_purchase_orders()

            self._clear_form()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # ADD ITEM
    # =========================================================

    def _add_item(self) -> None:

        if self._selected_order is None:
            return

        dialog = AddPurchaseOrderItemDialog(
            self._variant_service,
            self,
        )

        if not dialog.exec():
            return

        values = dialog.values()

        try:

            self._purchase_order_service.add_item(
                purchase_order_id=(
                    self._selected_order.id
                ),
                variant_id=values["variant_id"],
                quantity=values["quantity"],
                unit_cost=values["cost_price"],
            )

            self._reload_selected_order()

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

        dialog = AddPurchaseOrderItemDialog(
            self._variant_service,
            self,
        )

        index = dialog.variant_combo.findData(
            self._selected_item.product_variant_id
        )

        if index >= 0:

            dialog.variant_combo.setCurrentIndex(
                index
            )

        dialog.quantity_spin.setValue(
            self._selected_item.quantity
        )

        dialog.cost_price_spin.setValue(
            float(
                self._selected_item.unit_cost
            )
        )

        if not dialog.exec():
            return

        values = dialog.values()

        try:

            self._purchase_order_service.update_item(
                item_id=self._selected_item.id,
                quantity=values["quantity"],
                unit_cost=values["cost_price"],
            )

            self._reload_selected_order()

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
            (
                "Are you sure you want to delete "
                "the selected item?"
            ),
        ):
            return

        try:

            self._purchase_order_service.delete_item(
                self._selected_item.id
            )

            self._reload_selected_order()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # RECEIVE ORDER
    # =========================================================

    def _receive_order(self) -> None:

        if self._selected_order is None:
            return

        if not self.ask_confirmation(
            "Receive Purchase Order",
            (
                "Are you sure you want to receive "
                "this purchase order?"
            ),
        ):
            return

        try:

            self._purchase_order_service.receive(
                self._selected_order.id
            )

            self._reload_selected_order()

            self._load_purchase_orders()

            self._refresh_dashboard()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # RELOAD SELECTED ORDER
    # =========================================================

    def _reload_selected_order(
        self,
    ) -> None:

        if self._selected_order is None:
            return

        order_id = (
            self._selected_order.id
        )

        self._selected_order = (
            self._purchase_order_service.get_by_id(
                order_id
            )
        )

        if self._selected_order is None:

            self._clear_form()

            return

        # -----------------------------------------------------
        # Reload items
        # -----------------------------------------------------

        self.item_table.load(
            self._selected_order.items
        )

        # -----------------------------------------------------
        # Update permissions
        # -----------------------------------------------------

        is_draft = (
            self._selected_order.status
            == PurchaseOrderStatus.DRAFT
        )

        self.add_item_button.setEnabled(
            is_draft
        )

        self.receive_button.setEnabled(
            is_draft
        )

        self.delete_button.setEnabled(
            is_draft
        )

        self.edit_item_button.setEnabled(
            False
        )

        self.delete_item_button.setEnabled(
            False
        )

        self._selected_item = None