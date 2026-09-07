from uuid import UUID

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QSpinBox,
)

from app.modules.sales.services.sale_item_service import SaleItemService


class AddSalesReturnItemDialog(QDialog):

    def __init__(
        self,
        sale_item_service: SaleItemService,
        sale_id: UUID,
        parent=None,
    ):
        super().__init__(parent)

        self._sale_item_service = sale_item_service
        self._sale_id = sale_id

        self._sale_items = []

        self._build_ui()
        self._load_sale_items()
        self._connect_signals()

    def _build_ui(self):

        self.setWindowTitle(
            "Sales Return Item",
        )

        layout = QFormLayout(self)

        self.sale_item_combo = QComboBox()

        self.available_label = QLabel()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)

        layout.addRow(
            "Sale Item",
            self.sale_item_combo,
        )

        layout.addRow(
            "Available",
            self.available_label,
        )

        layout.addRow(
            "Return Qty",
            self.quantity_spin,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept,
        )

        buttons.rejected.connect(
            self.reject,
        )

        layout.addWidget(
            buttons,
        )

    def _connect_signals(self):

        self.sale_item_combo.currentIndexChanged.connect(
            self._sale_item_changed,
        )

    def _load_sale_items(self):

        self.sale_item_combo.clear()

        self._sale_items = (
            self._sale_item_service.get_returnable_items(
                self._sale_id,
            )
        )

        if not self._sale_items:
            self.quantity_spin.setEnabled(False)
            return

        self.quantity_spin.setEnabled(True)

        for item in self._sale_items:

            variant = item.sale_item.product_variant

            text = (
                f"{variant.product.name}"
                f" - {variant.length} yards"
            )

            self.sale_item_combo.addItem(
                text,
                item.sale_item.id,
            )

        self._sale_item_changed()

    def _sale_item_changed(self):

        index = self.sale_item_combo.currentIndex()

        if index < 0:
            return

        item = self._sale_items[index]

        available = item.available_quantity

        self.available_label.setText(
            str(available),
        )

        self.quantity_spin.setMaximum(
            available,
        )

    def values(self):

        return {
            "sale_item_id": self.sale_item_combo.currentData(),
            "quantity": self.quantity_spin.value(),
        }

    def set_quantity(
        self,
        quantity: int,
    ):

        self.quantity_spin.setValue(
            quantity,
        )

    