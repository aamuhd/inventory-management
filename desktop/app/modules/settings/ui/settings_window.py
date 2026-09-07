from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.modules.settings.services.settings_service import (
    SettingsService,
)


class SettingsWindow(QWidget):
    """
    Application settings window.

    Settings are loaded when the window opens and saved through
    SettingsService.

    Tax handling is intentionally not included.
    """

    def __init__(
        self,
        settings_service: SettingsService,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._settings_service = settings_service

        self.setWindowTitle(
            "Settings"
        )

        self.resize(
            700,
            720,
        )

        self._build_ui()
        self._connect_signals()
        self._load_settings()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        outer_layout = QVBoxLayout(
            self
        )

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # =====================================================
        # SCROLL AREA
        # =====================================================

        scroll_area = QScrollArea()

        scroll_area.setWidgetResizable(
            True
        )

        scroll_area.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()

        content.setObjectName(
            "settingsContent"
        )

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        content_layout.setSpacing(
            16
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = QLabel(
            "Application Settings"
        )

        header.setObjectName(
            "settingsHeader"
        )

        header.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        content_layout.addWidget(
            header
        )

        description = QLabel(
            "Configure your business information, "
            "sales documents, and inventory notifications."
        )

        description.setObjectName(
            "settingsDescription"
        )

        description.setWordWrap(
            True
        )

        content_layout.addWidget(
            description
        )

        # =====================================================
        # BUSINESS INFORMATION
        # =====================================================

        business_group = QGroupBox(
            "Business Information"
        )

        business_layout = QFormLayout(
            business_group
        )

        business_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        business_layout.setSpacing(
            12
        )

        self.business_name_input = QLineEdit()

        self.business_name_input.setPlaceholderText(
            "Business name"
        )

        self.business_address_input = QLineEdit()

        self.business_address_input.setPlaceholderText(
            "Business address"
        )

        self.business_phone_input = QLineEdit()

        self.business_phone_input.setPlaceholderText(
            "Business phone"
        )

        self.business_email_input = QLineEdit()

        self.business_email_input.setPlaceholderText(
            "Business email"
        )

        business_layout.addRow(
            "Business Name:",
            self.business_name_input,
        )

        business_layout.addRow(
            "Address:",
            self.business_address_input,
        )

        business_layout.addRow(
            "Phone:",
            self.business_phone_input,
        )

        business_layout.addRow(
            "Email:",
            self.business_email_input,
        )

        content_layout.addWidget(
            business_group
        )

        # =====================================================
        # SALES / INVOICE
        # =====================================================

        sales_group = QGroupBox(
            "Sales & Invoice"
        )

        sales_layout = QFormLayout(
            sales_group
        )

        sales_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        sales_layout.setSpacing(
            12
        )

        self.currency_input = QLineEdit()

        self.currency_input.setPlaceholderText(
            "NGN"
        )

        self.invoice_prefix_input = QLineEdit()

        self.invoice_prefix_input.setPlaceholderText(
            "INV"
        )

        self.receipt_footer_input = QTextEdit()

        self.receipt_footer_input.setPlaceholderText(
            "Optional text printed at the bottom of receipts."
        )

        self.receipt_footer_input.setMinimumHeight(
            90
        )

        self.receipt_footer_input.setMaximumHeight(
            140
        )

        sales_layout.addRow(
            "Currency:",
            self.currency_input,
        )

        sales_layout.addRow(
            "Invoice Prefix:",
            self.invoice_prefix_input,
        )

        sales_layout.addRow(
            "Receipt Footer:",
            self.receipt_footer_input,
        )

        content_layout.addWidget(
            sales_group
        )

        # =====================================================
        # INVENTORY
        # =====================================================

        inventory_group = QGroupBox(
            "Inventory"
        )

        inventory_layout = QVBoxLayout(
            inventory_group
        )

        inventory_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        inventory_layout.setSpacing(
            10
        )

        self.low_stock_notifications_checkbox = (
            QCheckBox(
                "Enable low-stock notifications"
            )
        )

        inventory_layout.addWidget(
            self.low_stock_notifications_checkbox
        )

        content_layout.addWidget(
            inventory_group
        )

        # =====================================================
        # PASSWORD RECOVERY
        # =====================================================

        recovery_group = QGroupBox(
            "Password Recovery"
        )

        recovery_layout = QVBoxLayout(
            recovery_group
        )

        recovery_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        recovery_layout.setSpacing(
            10
        )

        recovery_description = QLabel(
            "Generate a local recovery code for recovering "
            "the administrator password if it is forgotten."
        )

        recovery_description.setObjectName(
            "settingsRecoveryDescription"
        )

        recovery_description.setWordWrap(
            True
        )

        recovery_layout.addWidget(
            recovery_description
        )

        self.recovery_status_label = QLabel()

        self.recovery_status_label.setObjectName(
            "settingsRecoveryStatus"
        )

        recovery_layout.addWidget(
            self.recovery_status_label
        )

        recovery_button_layout = QHBoxLayout()

        recovery_button_layout.addStretch()

        self.generate_recovery_code_button = (
            QPushButton(
                "Generate Recovery Code"
            )
        )

        self.generate_recovery_code_button.setObjectName(
            "settingsGenerateRecoveryCodeButton"
        )

        self.generate_recovery_code_button.setMinimumWidth(
            190
        )

        self.generate_recovery_code_button.setMinimumHeight(
            38
        )

        self.generate_recovery_code_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        recovery_button_layout.addWidget(
            self.generate_recovery_code_button
        )

        recovery_layout.addLayout(
            recovery_button_layout
        )

        content_layout.addWidget(
            recovery_group
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            10
        )

        button_layout.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.cancel_button.setObjectName(
            "settingsCancelButton"
        )

        self.cancel_button.setMinimumWidth(
            100
        )

        self.save_button = QPushButton(
            "Save Settings"
        )

        self.save_button.setObjectName(
            "settingsSaveButton"
        )

        self.save_button.setMinimumWidth(
            130
        )

        button_layout.addWidget(
            self.cancel_button
        )

        button_layout.addWidget(
            self.save_button
        )

        content_layout.addLayout(
            button_layout
        )

        content_layout.addStretch()

        scroll_area.setWidget(
            content
        )

        outer_layout.addWidget(
            scroll_area
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.save_button.clicked.connect(
            self._save_settings
        )

        self.cancel_button.clicked.connect(
            self.close
        )

        self.generate_recovery_code_button.clicked.connect(
            self._generate_recovery_code
        )

    # =========================================================
    # LOAD SETTINGS
    # =========================================================

    def _load_settings(self) -> None:

        settings = self._settings_service.get()

        self.business_name_input.setText(
            settings.business_name
        )

        self.business_address_input.setText(
            settings.business_address or ""
        )

        self.business_phone_input.setText(
            settings.business_phone or ""
        )

        self.business_email_input.setText(
            settings.business_email or ""
        )

        self.currency_input.setText(
            settings.currency
        )

        self.invoice_prefix_input.setText(
            settings.invoice_prefix
        )

        self.receipt_footer_input.setPlainText(
            settings.receipt_footer or ""
        )

        self.low_stock_notifications_checkbox.setChecked(
            settings.low_stock_notifications
        )

        # -----------------------------------------------------
        # Recovery status
        # -----------------------------------------------------

        if settings.recovery_code_generated:

            self.recovery_status_label.setText(
                "A recovery code has already been generated. "
                "Generating a new code will invalidate the "
                "previous code."
            )

        else:

            self.recovery_status_label.setText(
                "No recovery code has been generated yet."
            )

    # =========================================================
    # GENERATE RECOVERY CODE
    # =========================================================

    def _generate_recovery_code(self) -> None:

        confirmation = QMessageBox.question(
            self,
            "Generate Recovery Code",
            (
                "Are you sure you want to generate a new "
                "recovery code?\n\n"
                "Any previously generated recovery code "
                "will become invalid."
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if (
            confirmation
            != QMessageBox.StandardButton.Yes
        ):
            return

        try:

            recovery_code = (
                self._settings_service
                .generate_recovery_code()
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Recovery Code",
                (
                    "Unable to generate the recovery code.\n\n"
                    f"{exc}"
                ),
            )

            return

        # -----------------------------------------------------
        # Display code once
        # -----------------------------------------------------

        message_box = QMessageBox(
            self
        )

        message_box.setWindowTitle(
            "Recovery Code Generated"
        )

        message_box.setIcon(
            QMessageBox.Icon.Information
        )

        message_box.setText(
            "Your new recovery code is:"
        )

        message_box.setInformativeText(
            (
                "Write this code down and keep it somewhere "
                "safe. It will not be shown again."
            )
        )

        message_box.setDetailedText(
            recovery_code
        )

        message_box.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

        message_box.exec()

        # -----------------------------------------------------
        # Update status
        # -----------------------------------------------------

        self.recovery_status_label.setText(
            "A recovery code has been generated. "
            "The previous code is now invalid."
        )

    # =========================================================
    # SAVE SETTINGS
    # =========================================================

    def _save_settings(self) -> None:

        try:

            self._settings_service.update(
                business_name=(
                    self.business_name_input.text()
                ),
                business_address=(
                    self.business_address_input.text()
                    or None
                ),
                business_phone=(
                    self.business_phone_input.text()
                    or None
                ),
                business_email=(
                    self.business_email_input.text()
                    or None
                ),
                currency=(
                    self.currency_input.text()
                ),
                invoice_prefix=(
                    self.invoice_prefix_input.text()
                ),
                receipt_footer=(
                    self.receipt_footer_input
                    .toPlainText()
                    or None
                ),
                low_stock_notifications=(
                    self.low_stock_notifications_checkbox
                    .isChecked()
                ),
            )

        except Exception as exc:

            QMessageBox.warning(
                self,
                "Unable to Save",
                str(exc),
            )

            return

        QMessageBox.information(
            self,
            "Settings Saved",
            "Application settings have been saved successfully.",
        )

        self.close()
