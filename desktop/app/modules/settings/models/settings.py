from sqlmodel import Field

from app.core.database.models.base import BaseModel


class Settings(BaseModel, table=True):
    """
    Stores application-wide settings.

    The application normally uses one settings record.
    The `key` field identifies the default settings record.
    """

    __tablename__ = "settings"

    key: str = Field(
        default="default",
        unique=True,
        index=True,
        max_length=50,
    )

    # =========================================================
    # BUSINESS INFORMATION
    # =========================================================

    business_name: str = Field(
        default="",
        max_length=150,
    )

    business_address: str | None = Field(
        default=None,
        max_length=255,
    )

    business_phone: str | None = Field(
        default=None,
        max_length=30,
    )

    business_email: str | None = Field(
        default=None,
        max_length=255,
    )

    # =========================================================
    # SALES / INVOICE
    # =========================================================

    currency: str = Field(
        default="NGN",
        max_length=10,
    )

    invoice_prefix: str = Field(
        default="INV",
        max_length=20,
    )

    receipt_footer: str | None = Field(
        default=None,
        max_length=500,
    )

    # =========================================================
    # INVENTORY
    # =========================================================

    low_stock_notifications: bool = Field(
        default=True,
    )

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    recovery_code_hash: str | None = Field(
        default=None,
    )

    recovery_code_generated: bool = Field(
        default=False,
    )
