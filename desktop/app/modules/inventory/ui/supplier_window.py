from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSplitter,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from sqlalchemy.exc import IntegrityError

from app.core.ui.base_window import BaseWindow

from app.modules.inventory.exceptions import (
    InvalidSupplierNameError,
    SupplierAlreadyExistsError,
    SupplierHasDependenciesError,
    SupplierNotFoundError,
)

from app.modules.inventory.models.supplier import Supplier

from app.modules.inventory.services.supplier_service import (
    SupplierService,
)

from app.modules.inventory.ui.supplier_form import (
    SupplierForm,
)

from app.modules.inventory.ui.supplier_table import (
    SupplierTable,
)


class SupplierWindow(BaseWindow):

    def __init__(
        self,
        supplier_service: SupplierService,
    ) -> None:

        super().__init__()

        self._supplier_service = (
            supplier_service
        )

        self._selected_supplier_id = None

        self._build_ui()
        self._connect_signals()

        self.load_suppliers()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Supplier Management"
        )

        self.setObjectName(
            "supplierWindow"
        )

        self.setMinimumSize(
            950,
            550,
        )

        self.resize(
            1200,
            700,
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form = SupplierForm()

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setObjectName(
            "deleteButton"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        self.delete_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        form_layout = QVBoxLayout()

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.setSpacing(
            10
        )

        form_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            self.delete_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "supplierFormContainer"
        )

        form_widget.setLayout(
            form_layout
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = SupplierTable()

        # -----------------------------------------------------
        # Splitter
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "supplierSplitter"
        )

        splitter.addWidget(
            form_widget
        )

        splitter.addWidget(
            self.table
        )

        splitter.setSizes(
            [
                380,
                820,
            ]
        )

        form_widget.setMinimumWidth(
            330
        )

        self.table.setMinimumWidth(
            450
        )

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        main_layout.addWidget(
            splitter
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(
        self,
    ) -> None:

        self.form.save_button.clicked.connect(
            self.save
        )

        self.form.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete
        )

        self.table.supplier_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load_suppliers(
        self,
    ) -> None:

        suppliers = (
            self._supplier_service.get_all()
        )

        self.table.set_suppliers(
            suppliers
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self,
    ) -> None:

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

                self.show_information(
                    "Supplier created successfully."
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

                self.show_information(
                    "Supplier updated successfully."
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

    # =========================================================
    # EDIT
    # =========================================================

    def edit_selected(
        self,
        supplier: Supplier,
    ) -> None:

        if supplier.id is None:
            return

        self._selected_supplier_id = (
            supplier.id
        )

        self.form.set_supplier(
            supplier.name,
            supplier.contact_person,
            supplier.phone,
            supplier.email,
            supplier.address,
            supplier.notes,
        )

        self.form.set_edit_mode()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
    ) -> None:

        supplier = (
            self.table.selected_supplier()
        )

        if (
            supplier is None
            or supplier.id is None
        ):
            return

        if not self.ask_confirmation(
            "Delete Supplier",
            f'Delete "{supplier.name}"?',
        ):
            return

        try:

            self._supplier_service.delete(
                supplier.id
            )

            self.clear_form()

            self.load_suppliers()

            self.show_information(
                "Supplier deleted successfully."
            )

        except SupplierNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

        except SupplierHasDependenciesError as error:

            QMessageBox.warning(
                self,
                "Cannot Delete Supplier",
                str(error),
            )
            
    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(
        self,
    ) -> None:

        self._selected_supplier_id = None

        self.form.clear()

        self.form.set_create_mode()