from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.core.ui.base_window import BaseWindow

from app.modules.sales.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    InvalidCustomerNameError,
)

from app.modules.sales.models.customer import Customer

from app.modules.sales.services.customer_service import (
    CustomerService,
)

from app.modules.sales.ui.customer_form import (
    CustomerForm,
)

from app.modules.sales.ui.customer_table import (
    CustomerTable,
)


class CustomerWindow(BaseWindow):

    def __init__(
        self,
        customer_service: CustomerService,
        refresh_sale_customers: Callable[[], None] | None = None,
        show_customer_details: Callable[
            [Customer],
            None,
        ] | None = None,
    ) -> None:

        super().__init__()

        self._customer_service = (
            customer_service
        )

        self._refresh_sale_customers = (
            refresh_sale_customers
        )

        self._show_customer_details = (
            show_customer_details
        )

        self._selected_customer_id = None

        self._build_ui()
        self._connect_signals()

        self.load_customers()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Customer Management"
        )

        self.setObjectName(
            "customerWindow"
        )

        self.setMinimumSize(
            950,
            600,
        )

        self.resize(
            1100,
            700,
        )

        # =====================================================
        # FORM
        # =====================================================

        self.form = CustomerForm()

        self.form.setObjectName(
            "customerFormContainer"
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.delete_button = QPushButton(
            "Delete Customer"
        )

        self.delete_button.setObjectName(
            "customerDeleteButton"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        self.delete_button.setEnabled(
            False
        )

        self.details_button = QPushButton(
            "View Customer Details"
        )

        self.details_button.setObjectName(
            "customerDetailsButton"
        )

        self.details_button.setMinimumHeight(
            40
        )

        self.details_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.details_button.setEnabled(
            False
        )

        # =====================================================
        # LEFT PANEL
        # =====================================================

        form_layout = QVBoxLayout()

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.setSpacing(
            8
        )

        form_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            self.details_button
        )

        form_layout.addWidget(
            self.delete_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "customerFormPanel"
        )

        form_widget.setLayout(
            form_layout
        )

        form_widget.setMinimumWidth(
            320
        )

        # =====================================================
        # TABLE
        # =====================================================

        self.table = CustomerTable()

        self.table.setMinimumWidth(
            500
        )

        # =====================================================
        # SPLITTER
        # =====================================================

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "customerSplitter"
        )

        splitter.addWidget(
            form_widget
        )

        splitter.addWidget(
            self.table
        )

        splitter.setSizes(
            [
                350,
                750,
            ]
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        main_layout.setSpacing(
            10
        )

        main_layout.addWidget(
            splitter
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(
            self.save
        )

        self.form.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete
        )

        self.details_button.clicked.connect(
            self.show_details
        )

        self.table.customer_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load_customers(self) -> None:

        customers = (
            self._customer_service.get_all()
        )

        self.table.set_customers(
            customers
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(self) -> None:

        (
            name,
            phone,
            email,
            address,
        ) = self.form.customer_data()

        try:

            if self._selected_customer_id is None:

                self._customer_service.create(
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                )

                if self._refresh_sale_customers is not None:
                    self._refresh_sale_customers()

                self.show_information(
                    "Customer created successfully."
                )

            else:

                self._customer_service.update(
                    customer_id=(
                        self._selected_customer_id
                    ),
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                )

                self.show_information(
                    "Customer updated successfully."
                )

            self.clear_form()
            self.load_customers()

        except (
            InvalidCustomerNameError,
            CustomerAlreadyExistsError,
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
        customer: Customer,
    ) -> None:

        if customer.id is None:
            return

        self._selected_customer_id = (
            customer.id
        )

        self.form.set_customer(
            customer.name,
            customer.phone,
            customer.email,
            customer.address,
        )

        self.form.set_edit_mode()

        self.delete_button.setEnabled(
            True
        )

        self.details_button.setEnabled(
            True
        )

    # =========================================================
    # CUSTOMER DETAILS
    # =========================================================

    def show_details(self) -> None:

        customer = (
            self.table.selected_customer()
        )

        if customer is None:
            return

        if self._show_customer_details is None:
            return

        self._show_customer_details(
            customer
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self) -> None:

        customer = (
            self.table.selected_customer()
        )

        if customer is None:
            return

        if customer.id is None:
            return

        if not self.ask_confirmation(
            "Delete Customer",
            f'Delete "{customer.name}"?',
        ):
            return

        try:

            self._customer_service.delete(
                customer.id
            )

            self.clear_form()
            self.load_customers()

            self.show_information(
                "Customer deleted successfully."
            )

        except CustomerNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self) -> None:

        self._selected_customer_id = None

        self.form.clear()
        self.form.set_create_mode()

        self.delete_button.setEnabled(
            False
        )

        self.details_button.setEnabled(
            False
        )

        self.table.table.clearSelection()