from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)

from app.modules.sales.services.payment_service import (
    PaymentService,
)


class PaymentDialog(QDialog):

    def __init__(
        self,
        sale_id: UUID,
        payment_service: PaymentService,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self._sale_id = sale_id
        self._payment_service = payment_service

        self.setWindowTitle(
            "Record Payment"
        )

        self.setMinimumWidth(
            400
        )

        self._build_ui()
        self._load_balance()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.balance_label = QLabel()

        self.amount_spin = QDoubleSpinBox()

        self.amount_spin.setDecimals(
            2
        )

        self.amount_spin.setMinimum(
            0.01
        )

        self.amount_spin.setMaximum(
            999999999.99
        )

        self.payment_date_edit = QDateEdit()

        self.payment_date_edit.setCalendarPopup(
            True
        )

        today = date.today()

        self.payment_date_edit.setDate(
            QDate(
                today.year,
                today.month,
                today.day,
            )
        )

        self.payment_method_combo = QComboBox()

        self.payment_method_combo.addItems(
            [
                "Cash",
                "Bank Transfer",
            ]
        )

        self.notes_edit = QLabel()

        form = QFormLayout()

        form.addRow(
            "Outstanding Balance:",
            self.balance_label,
        )

        form.addRow(
            "Payment Amount:",
            self.amount_spin,
        )

        form.addRow(
            "Payment Date:",
            self.payment_date_edit,
        )

        form.addRow(
            "Payment Method:",
            self.payment_method_combo,
        )

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(
            self._save
        )

        self.buttons.rejected.connect(
            self.reject
        )

        layout = QVBoxLayout(
            self
        )

        layout.addLayout(
            form
        )

        layout.addWidget(
            self.buttons
        )

    # =========================================================
    # LOAD BALANCE
    # =========================================================

    def _load_balance(self) -> None:

        balance = (
            self._payment_service.get_balance(
                self._sale_id
            )
        )

        self._balance = balance

        self.balance_label.setText(
            f"{balance:,.2f}"
        )

        if balance > Decimal("0.00"):

            self.amount_spin.setMaximum(
                float(balance)
            )

            self.amount_spin.setValue(
                float(balance)
            )

    # =========================================================
    # SAVE
    # =========================================================

    def _save(self) -> None:

        amount = Decimal(
            str(
                self.amount_spin.value()
            )
        )

        payment_date = (
            self.payment_date_edit
            .date()
            .toPython()
        )

        payment_method = (
            self.payment_method_combo
            .currentText()
        )

        try:

            self._payment_service.create(
                sale_id=self._sale_id,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method,
            )

            self.accept()

        except Exception as error:

            if self.parent() is not None:

                self.parent().show_error(
                    str(error)
                )

    # =========================================================
    # VALUES
    # =========================================================

    def values(self) -> dict:

        return {
            "amount": Decimal(
                str(
                    self.amount_spin.value()
                )
            ),
            "payment_date": (
                self.payment_date_edit
                .date()
                .toPython()
            ),
            "payment_method": (
                self.payment_method_combo
                .currentText()
            ),
        }
