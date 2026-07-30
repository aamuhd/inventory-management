from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.modules.inventory.exceptions import (
    InvalidSupplierNameError,
    SupplierAlreadyExistsError,
    SupplierNotFoundError,
)
from app.modules.inventory.models.supplier import Supplier
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)
from app.modules.inventory.ui.supplier_form import SupplierForm
from app.modules.inventory.ui.supplier_table import SupplierTable
from app.core.ui.base_window import BaseWindow


class SupplierWindow(BaseWindow):

    def __init__(
        self,
        supplier_service: SupplierService,
    ) -> None:
        super().__init__()

        self._supplier_service = supplier_service

        self._selected_supplier_id = None

        self._build_ui()
        self._connect_signals()

        self.load_suppliers()

    def _build_ui(self) -> None:

        self.setWindowTitle("Supplier Management")

        self.form = SupplierForm()

        self.table = SupplierTable()

        self.delete_button = QPushButton("Delete")

        left_layout = QVBoxLayout()

        left_layout.addWidget(
            self.form,
        )

        left_layout.addWidget(
            self.delete_button,
        )

        main_layout = QHBoxLayout(self)

        main_layout.addLayout(
            left_layout,
            1,
        )

        main_layout.addWidget(
            self.table,
            2,
        )

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(
            self.save,
        )

        self.form.clear_button.clicked.connect(
            self.clear_form,
        )

        self.delete_button.clicked.connect(
            self.delete,
        )

        self.table.supplier_selected.connect(
            self.edit_selected,
        )

    def load_suppliers(self) -> None:

        suppliers = self._supplier_service.get_all()

        self.table.set_suppliers(
            suppliers,
        )

    def save(self) -> None:

        (
            name,
            contact_person,
            phone,
            email,
            address,
            notes,
        ) = self.form.supplier_data()

        try:

            if self._selected_supplier_id is None:

                self._supplier_service.create(
                    name=name,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    address=address,
                    notes=notes,
                )
                """
                QMessageBox.information(
                    self,
                    "Success",
                    "Supplier created successfully.",
                )
                """
                #####
                self.show_information(
                    "Supplier created successfully.",
                )

            else:

                self._supplier_service.update(
                    supplier_id=self._selected_supplier_id,
                    name=name,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    address=address,
                    notes=notes,
                )
                """
                QMessageBox.information(
                    self,
                    "Success",
                    "Supplier updated successfully.",
                )
                """
                self.show_information(
                    "Supplier created successfully.",
                )

            self.clear_form()

            self.load_suppliers()

        except (
            InvalidSupplierNameError,
            SupplierAlreadyExistsError,
        ) as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def edit_selected(
        self,
        supplier: Supplier,
    ) -> None:

        if supplier.id is None:
            return

        self._selected_supplier_id = supplier.id

        self.form.set_supplier(
            supplier.name,
            supplier.contact_person,
            supplier.phone,
            supplier.email,
            supplier.address,
            supplier.notes,
        )

        self.form.set_edit_mode()

    def delete(self) -> None:

        supplier = self.table.selected_supplier()

        if supplier is None or supplier.id is None:
            return
        """
        answer = QMessageBox.question(
            self,
            "Delete Supplier",
            f'Delete "{supplier.name}"?',
        )

        if answer != QMessageBox.StandardButton.Yes:
            return
        """
        if not self.ask_confirmation(
            "Delete Supplier",
            f'Delete "{supplier.name}"?',
        ):
            return

        try:

            self._supplier_service.delete(
                supplier.id,
            )

            self.clear_form()

            self.load_suppliers()

        except SupplierNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def clear_form(self) -> None:

        self._selected_supplier_id = None

        self.form.clear()

        self.form.set_create_mode()