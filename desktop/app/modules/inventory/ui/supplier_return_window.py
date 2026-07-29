from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.supplier_return import (
    SupplierReturnStatus,
)

from app.modules.inventory.services.supplier_return_service import (
    SupplierReturnService,
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)
from app.modules.inventory.services.purchase_order_service import (
    PurchaseOrderService,
)
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)

from app.modules.inventory.ui.supplier_return_form import (
    SupplierReturnForm,
)
from app.modules.inventory.ui.supplier_return_table import (
    SupplierReturnTable,
)
from app.modules.inventory.ui.supplier_return_item_table import (
    SupplierReturnItemTable,
)
from app.modules.inventory.ui.add_supplier_return_item_dialog import AddSupplierReturnItemDialog


class SupplierReturnWindow(QWidget):

    def __init__(
        self,
        supplier_return_service: SupplierReturnService,
        supplier_service: SupplierService,
        purchase_order_service: PurchaseOrderService,
        variant_service: ProductVariantService,
    ):
        super().__init__()

        self._supplier_return_service = supplier_return_service
        self._supplier_service = supplier_service
        self._purchase_order_service = purchase_order_service
        self._variant_service = variant_service

        self._selected_supplier_return = None
        self._selected_item = None

        self._build_ui()
        self._connect_signals()

        self._load_suppliers()
        self._load_supplier_returns()

    def _build_ui(self):

        self.setWindowTitle(
            "Supplier Returns",
        )

        main_layout = QVBoxLayout(self)

        self.form = SupplierReturnForm()

        main_layout.addWidget(
            self.form,
        )

        splitter = QSplitter()

        self.table = SupplierReturnTable()

        self.item_table = SupplierReturnItemTable()

        splitter.addWidget(
            self.table,
        )

        splitter.addWidget(
            self.item_table,
        )

        splitter.setStretchFactor(
            0,
            1,
        )

        splitter.setStretchFactor(
            1,
            1,
        )

        main_layout.addWidget(
            splitter,
        )

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

        self.submit_button = QPushButton(
            "Submit",
        )

        self.delete_button = QPushButton(
            "Delete",
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

        self.submit_button.setEnabled(
            False,
        )

        self.delete_button.setEnabled(
            False,
        )

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
            self.submit_button,
        )

        button_layout.addWidget(
            self.delete_button,
        )

        main_layout.addLayout(
            button_layout,
        )

    def _connect_signals(self):

        self.form.create_clicked.connect(
            self._create_supplier_return,
        )

        self.form.update_clicked.connect(
            self._update_supplier_return,
        )

        self.form.clear_clicked.connect(
            self._clear_form,
        )

        self.table.supplier_return_selected.connect(
            self._supplier_return_selected,
        )

        self.item_table.item_selected.connect(
            self._item_selected,
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

        self.submit_button.clicked.connect(
            self._submit_supplier_return,
        )

        self.delete_button.clicked.connect(
            self._delete_supplier_return,
        )

        self.form.supplier_combo.currentIndexChanged.connect(
            self._supplier_changed,
        )

    def _reload_selected_supplier_return(self):

        if self._selected_supplier_return is None:
            return
        self._selected_supplier_return = (
            self._supplier_return_service.get_by_id(
                self._selected_supplier_return.id,
            )
        )
        self.item_table.load(
            self._selected_supplier_return.items,
        )
        self._load_supplier_returns()

    def _load_suppliers(self):

        suppliers = self._supplier_service.get_all()
        self.form.load_suppliers(
            suppliers,
        )
        self._supplier_changed()

    def _load_supplier_returns(self):

        supplier_returns = (
            self._supplier_return_service.get_all()
        )
        self.table.load(
            supplier_returns,
        )

    def _supplier_changed(self):

        supplier_id = self.form.supplier_id()
        if supplier_id is None:
            self.form.load_purchase_orders(
                [],
            )
            return
        purchase_orders = (
            self._purchase_order_service.get_by_supplier(
                supplier_id,
            )
        )
        self.form.load_purchase_orders(
            purchase_orders,
        )

    def _create_supplier_return(self):

        try:

            supplier_return = (
                self._supplier_return_service.create(
                    supplier_id=self.form.supplier_id(),
                    purchase_order_id=self.form.purchase_order_id(),
                    return_number=self.form.return_number(),
                    return_date=self.form.return_date(),
                    notes=self.form.notes(),
                )
            )

            self._load_supplier_returns()
            self._supplier_return_selected(
                supplier_return,
            )
        except Exception as error:

            self._show_error(
                str(error),
            )

    def _update_supplier_return(self):

        if self._selected_supplier_return is None:
            return

        try:
            supplier_return = (
                self._supplier_return_service.update(
                    supplier_return_id=self._selected_supplier_return.id,
                    supplier_id=self.form.supplier_id(),
                    purchase_order_id=self.form.purchase_order_id(),
                    return_number=self.form.return_number(),
                    return_date=self.form.return_date(),
                    notes=self.form.notes(),
                )
            )

            self._load_supplier_returns()
            self._supplier_return_selected(
                supplier_return,
            )
        except Exception as error:
            self._show_error(
                str(error),
            )

    def _supplier_return_selected(
        self,
        supplier_return,
    ):

        self._selected_supplier_return = supplier_return

        self.form.load_suppliers(
            supplier_return,
        )

        self.item_table.load(
            supplier_return.items,
        )

        self.delete_button.setEnabled(
            True,
        )
        
        if supplier_return.status == SupplierReturnStatus.DRAFT:

            self.add_item_button.setEnabled(
                True,
            )

            self.submit_button.setEnabled(
                True,
            )

        else:

            self.add_item_button.setEnabled(
                False,
            )

            self.edit_item_button.setEnabled(
                False,
            )

            self.delete_item_button.setEnabled(
                False,
            )

            self.submit_button.setEnabled(
                False,
            )

    def _item_selected(
        self,
        item,
    ):

        self._selected_item = item

        if (
            self._selected_supplier_return
            and self._selected_supplier_return.status == SupplierReturnStatus.DRAFT
        ):

            self.edit_item_button.setEnabled(
                True,
            )

            self.delete_item_button.setEnabled(
                True,
            )

    def _add_item(self):

        if self._selected_supplier_return is None:
            return

        dialog = AddSupplierReturnItemDialog(
            self._variant_service,
            self,
        )

        if not dialog.exec():
            return

        values = dialog.values()

        try:

            self._supplier_return_service.add_item(
                supplier_return_id=self._selected_supplier_return.id,
                variant_id=values["variant_id"],
                quantity=values["quantity"],
                reason=values["reason"],
            )

            self._reload_selected_supplier_return()

        except Exception as error:

            self._show_error(
                str(error),
            )    

    def _edit_item(self):

        if self._selected_item is None:
            return

        dialog = AddSupplierReturnItemDialog(
            self._variant_service,
            self,
        )

        dialog.load_item(
            variant_id=self._selected_item.variant_id,
            quantity=self._selected_item.quantity,
            reason=self._selected_item.reason,
        )

        if not dialog.exec():
            return

        values = dialog.values()

        try:

            self._supplier_return_service.update_item(
                item_id=self._selected_item.id,
                quantity=values["quantity"],
                reason=values["reason"],
            )

            self._reload_selected_supplier_return()

        except Exception as error:

            self._show_error(
                str(error),
            )

    def _delete_item(self):

        if self._selected_item is None:
            return

        try:

            self._supplier_return_service.delete_item(
                self._selected_item.id,
            )

            self._reload_selected_supplier_return()

            self._selected_item = None

            self.edit_item_button.setEnabled(
                False,
            )

            self.delete_item_button.setEnabled(
                False,
            )

        except Exception as error:

            self._show_error(
                str(error),
            )

    def _submit_supplier_return(self):

        if self._selected_supplier_return is None:
            return

        try:

            supplier_return = (
                self._supplier_return_service.submit(
                    self._selected_supplier_return.id,
                )
            )

            self._load_supplier_returns()

            self._supplier_return_selected(
                supplier_return,
            )

        except Exception as error:

            self._show_error(
                str(error),
            )

    def _delete_supplier_return(self):

        if self._selected_supplier_return is None:
            return

        try:

            self._supplier_return_service.delete(
                self._selected_supplier_return.id,
            )

            self._clear_form()

            self._load_supplier_returns()

        except Exception as error:

            self._show_error(
                str(error),
            )

    def _clear_form(self):

        self.form.clear()
        self.item_table.clear_table()
        self._selected_supplier_return = None
        self._selected_item = None
        self.add_item_button.setEnabled(
            False,
        )
        self.edit_item_button.setEnabled(
            False,
        )
        self.delete_item_button.setEnabled(
            False,
        )
        self.submit_button.setEnabled(
            False,
        )
        self.delete_button.setEnabled(
            False,
        )

    def _show_error(
        self,
        message: str,
    ):

        QMessageBox.critical(
            self,
            "Error",
            message,
        )
        