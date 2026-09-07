import pytest

from app.modules.settings.exceptions import (
    InvalidBusinessNameError,
    InvalidCurrencyError,
    InvalidInvoicePrefixError,
)
from app.modules.settings.repositories.settings_repository import (
    SettingsRepository,
)
from app.modules.settings.services.settings_service import (
    SettingsService,
)

from tests.helpers import create_test_session


def create_service() -> SettingsService:

    session = create_test_session()

    repository = SettingsRepository(session)

    return SettingsService(repository)


def test_get_creates_default_settings() -> None:

    service = create_service()

    settings = service.get()

    assert settings.id is not None
    assert settings.key == "default"
    assert settings.currency == "NGN"
    assert settings.invoice_prefix == "INV"


def test_get_returns_existing_settings() -> None:

    service = create_service()

    first = service.get()
    second = service.get()

    assert first.id == second.id


def test_update_settings() -> None:

    service = create_service()

    settings = service.update(
        business_name="Al-Noor Store",
        business_address="Kano",
        business_phone="08000000000",
        business_email="store@example.com",
        currency="NGN",
        invoice_prefix="INV",
        receipt_footer="Thank you for your purchase.",
        low_stock_notifications=True,
    )

    assert settings.business_name == "Al-Noor Store"
    assert settings.business_address == "Kano"
    assert settings.business_phone == "08000000000"
    assert settings.business_email == "store@example.com"
    assert settings.currency == "NGN"
    assert settings.invoice_prefix == "INV"
    assert settings.receipt_footer == (
        "Thank you for your purchase."
    )
    assert settings.low_stock_notifications is True


def test_business_name_cannot_be_empty() -> None:

    service = create_service()

    with pytest.raises(InvalidBusinessNameError):
        service.update(
            business_name="   ",
        )


def test_currency_cannot_be_empty() -> None:

    service = create_service()

    with pytest.raises(InvalidCurrencyError):
        service.update(
            business_name="Al-Noor Store",
            currency="   ",
        )


def test_invoice_prefix_cannot_be_empty() -> None:

    service = create_service()

    with pytest.raises(InvalidInvoicePrefixError):
        service.update(
            business_name="Al-Noor Store",
            invoice_prefix="   ",
        )


def test_currency_is_normalized() -> None:

    service = create_service()

    settings = service.update(
        business_name="Al-Noor Store",
        currency=" ngn ",
    )

    assert settings.currency == "NGN"


def test_invoice_prefix_is_normalized() -> None:

    service = create_service()

    settings = service.update(
        business_name="Al-Noor Store",
        invoice_prefix=" inv ",
    )

    assert settings.invoice_prefix == "INV"