from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.modules.sales.exceptions import (
    CustomerNotFoundError,
    CustomerAlreadyExistsError,
    InvalidCustomerNameError,
)
from app.modules.sales.models.customer import Customer
from app.modules.sales.services.customer_service import (
    CustomerService,
)
from app.modules.sales.ui.customer_form import CustomerForm
from app.modules.sales.ui.customer_table import CustomerTable
from app.core.ui.base_window import BaseWindow


class CustomerWindow(BaseWindow):

    def __init__(
        self,
        customer_service: CustomerService,
    ) -> None:
        super().__init__()

        self._customer_service = customer_service

        self._selected_customer_id = None

        self._build_ui()
        self._connect_signals()

        self.load_customers()

    def _build_ui(self) -> None:

        self.setWindowTitle("Customer Management")

        self.form = CustomerForm()

        self.table = CustomerTable()

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

        self.table.customer_selected.connect(
            self.edit_selected,
        )

    def load_customers(self) -> None:

        customers = self._customer_service.get_all()

        self.table.set_customers(
            customers,
        )

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
                """
                QMessageBox.information(
                    self,
                    "Success",
                    "Customer created successfully.",
                )
                """
                #####
                self.show_information(
                    "Customer created successfully.",
                )

            else:

                self._customer_service.update(
                    customer_id=self._selected_customer_id,
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                )
                """
                QMessageBox.information(
                    self,
                    "Success",
                    "Customer updated successfully.",
                )
                """
                self.show_information(
                    "Customer created successfully.",
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

    def edit_selected(
        self,
        customer: Customer,
    ) -> None:

        if customer.id is None:
            return

        self._selected_customer_id = customer.id

        self.form.set_customer(
            customer.name,
            customer.phone,
            customer.email,
            customer.address,
        )

        self.form.set_edit_mode()

    def delete(self) -> None:

        customer = self.table.selected_customer()

        if customer is None or Customer.id is None:
            return
        """
        answer = QMessageBox.question(
            self,
            "Delete Customer",
            f'Delete "{Customer.name}"?',
        )

        if answer != QMessageBox.StandardButton.Yes:
            return
        """
        if not self.ask_confirmation(
            "Delete Customer",
            f'Delete "{customer.name}"?',
        ):
            return

        try:

            self._customer_service.delete(
                customer.id,
            )

            self.clear_form()

            self.load_customers()

        except CustomerNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def clear_form(self) -> None:

        self._selected_customer_id = None

        self.form.clear()
        self.form.set_create_mode()