from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ChangePasswordForm(QWidget):

    def __init__(
        self,
    ) -> None:

        super().__init__()

        self.setObjectName(
            "changePasswordForm"
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = QLabel(
            "Change Your Password"
        )

        self.title_label.setObjectName(
            "changePasswordTitle"
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        self.description_label = QLabel(
            "For security, you must change your password "
            "before continuing."
        )

        self.description_label.setObjectName(
            "changePasswordDescription"
        )

        self.description_label.setWordWrap(
            True
        )

        # =====================================================
        # PASSWORD
        # =====================================================

        self.password_edit = QLineEdit()

        self.password_edit.setObjectName(
            "changePasswordEdit"
        )

        self.password_edit.setPlaceholderText(
            "Enter new password"
        )

        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # =====================================================
        # CONFIRM PASSWORD
        # =====================================================

        self.confirm_password_edit = QLineEdit()

        self.confirm_password_edit.setObjectName(
            "changePasswordConfirmEdit"
        )

        self.confirm_password_edit.setPlaceholderText(
            "Confirm new password"
        )

        self.confirm_password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # =====================================================
        # BUTTON
        # =====================================================

        self.change_button = QPushButton(
            "Change Password"
        )

        self.change_button.setObjectName(
            "changePasswordButton"
        )

        self.change_button.setMinimumHeight(
            40
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        form_layout = QFormLayout()

        form_layout.setSpacing(
            12
        )

        form_layout.addRow(
            "New Password:",
            self.password_edit,
        )

        form_layout.addRow(
            "Confirm Password:",
            self.confirm_password_edit,
        )

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        main_layout.setSpacing(
            15
        )

        main_layout.addWidget(
            self.title_label
        )

        main_layout.addWidget(
            self.description_label
        )

        main_layout.addSpacing(
            15
        )

        main_layout.addLayout(
            form_layout
        )

        main_layout.addSpacing(
            15
        )

        main_layout.addWidget(
            self.change_button
        )

        main_layout.addStretch()