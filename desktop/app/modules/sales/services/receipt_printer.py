from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from PySide6.QtCore import QMarginsF, QRectF
from PySide6.QtGui import (
    QFont,
    QPageLayout,
    QPageSize,
    QPainter,
    QPdfWriter,
    QPen,
)
from PySide6.QtPrintSupport import (
    QPrintDialog,
    QPrinter,
)
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QWidget,
)

from app.modules.sales.models.sale import Sale
from app.modules.sales.services.payment_service import (
    PaymentService,
)


class ReceiptPrinter:

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        self._parent = parent

    # =========================================================
    # PRINT RECEIPT
    # =========================================================

    def print_receipt(
        self,
        sale: Sale,
        settings,
        payment_service: PaymentService | None = None,
    ) -> bool:

        printer = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        printer.setPageMargins(
            QMarginsF(
                5,
                5,
                5,
                5,
            )
        )

        dialog = QPrintDialog(
            printer,
            self._parent,
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return False

        self._draw_receipt(
            device=printer,
            sale=sale,
            settings=settings,
            payment_service=payment_service,
        )

        return True

    # =========================================================
    # SAVE AS PDF
    # =========================================================

    def save_pdf(
        self,
        sale: Sale,
        settings,
        payment_service: PaymentService | None = None,
    ) -> bool:

        default_name = (
            f"{sale.invoice_number}.pdf"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self._parent,
            "Save Receipt as PDF",
            str(
                Path.home()
                / default_name
            ),
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return False

        if not file_path.lower().endswith(
            ".pdf"
        ):
            file_path += ".pdf"

        writer = QPdfWriter(
            file_path
        )

        writer.setResolution(
            96
        )

        writer.setPageLayout(
            QPageLayout(
                QPageSize(
                    QPageSize.PageSizeId.A4
                ),
                QPageLayout.Orientation.Portrait,
                QMarginsF(
                    10,
                    10,
                    10,
                    10,
                ),
                QPageLayout.Unit.Millimeter,
            )
        )

        self._draw_receipt(
            device=writer,
            sale=sale,
            settings=settings,
            payment_service=payment_service,
        )

        return True

    # =========================================================
    # DRAW RECEIPT
    # =========================================================

    def _draw_receipt(
        self,
        device,
        sale: Sale,
        settings,
        payment_service: PaymentService | None = None,
    ) -> None:

        painter = QPainter()

        if not painter.begin(device):
            raise RuntimeError(
                "Unable to start receipt printer."
            )

        try:

            resolution = device.resolution()

            if resolution <= 0:
                resolution = 96

            scale = (
                resolution
                / 72.0
            )

            painter.scale(
                scale,
                scale,
            )

            page_width = (
                device.width()
                / scale
            )

            page_height = (
                device.height()
                / scale
            )

            margin = 30.0

            content_left = margin

            content_right = (
                page_width
                - margin
            )

            content_width = (
                content_right
                - content_left
            )

            self._draw_receipt_page(
                painter=painter,
                sale=sale,
                settings=settings,
                payment_service=payment_service,
                page_width=page_width,
                page_height=page_height,
                content_left=content_left,
                content_width=content_width,
            )

        finally:

            painter.end()

    # =========================================================
    # DRAW RECEIPT PAGE
    # =========================================================

    def _draw_receipt_page(
        self,
        painter: QPainter,
        sale: Sale,
        settings,
        payment_service: PaymentService | None,
        page_width: float,
        page_height: float,
        content_left: float,
        content_width: float,
    ) -> None:

        # =====================================================
        # FONTS
        # =====================================================

        normal_font = QFont(
            "Noto Sans",
            9,
        )

        small_font = QFont(
            "Noto Sans",
            8,
        )

        label_font = QFont(
            "Noto Sans",
            9,
        )

        label_font.setBold(
            True
        )

        business_font = QFont(
            "Noto Sans",
            20,
        )

        business_font.setBold(
            True
        )

        title_font = QFont(
            "Noto Sans",
            13,
        )

        title_font.setBold(
            True
        )

        header_font = QFont(
            "Noto Sans",
            9,
        )

        header_font.setBold(
            True
        )

        total_label_font = QFont(
            "Noto Sans",
            11,
        )

        total_label_font.setBold(
            True
        )

        total_value_font = QFont(
            "Noto Sans",
            13,
        )

        total_value_font.setBold(
            True
        )

        payment_label_font = QFont(
            "Noto Sans",
            10,
        )

        payment_label_font.setBold(
            True
        )

        payment_value_font = QFont(
            "Noto Sans",
            10,
        )

        payment_value_font.setBold(
            True
        )

        # =====================================================
        # SETTINGS
        # =====================================================

        business_name = (
            settings.business_name
            or "Business"
        )

        business_address = (
            settings.business_address
            or ""
        )

        business_phone = (
            settings.business_phone
            or ""
        )

        business_email = (
            settings.business_email
            or ""
        )

        currency = (
            settings.currency
            or ""
        )

        footer = (
            settings.receipt_footer
            or ""
        )

        # =====================================================
        # COLORS
        # =====================================================

        dark = "#202020"
        medium = "#555555"
        light = "#999999"
        border = "#CFCFCF"
        soft_background = "#F5F5F5"

        # =====================================================
        # PAYMENT INFORMATION
        # =====================================================

        paid = Decimal("0.00")

        if (
            payment_service is not None
            and sale.id is not None
        ):

            paid = (
                payment_service.get_total_paid(
                    sale.id
                )
            )

        balance = (
            sale.total_amount - paid
        )

        if balance < Decimal("0.00"):
            balance = Decimal("0.00")

        # =====================================================
        # START POSITION
        # =====================================================

        y = 35.0

        # =====================================================
        # BUSINESS NAME
        # =====================================================

        painter.setPen(
            QPen(
                dark
            )
        )

        painter.setFont(
            business_font
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                30,
            ),
            0x0004,
            business_name,
        )

        y += 27

        # =====================================================
        # BUSINESS INFORMATION
        # =====================================================

        painter.setFont(
            small_font
        )

        painter.setPen(
            QPen(
                medium
            )
        )

        if business_address:

            painter.drawText(
                QRectF(
                    content_left,
                    y,
                    content_width,
                    18,
                ),
                0x0004,
                business_address,
            )

            y += 14

        if business_phone:

            painter.drawText(
                QRectF(
                    content_left,
                    y,
                    content_width,
                    18,
                ),
                0x0004,
                business_phone,
            )

            y += 14

        if business_email:

            painter.drawText(
                QRectF(
                    content_left,
                    y,
                    content_width,
                    18,
                ),
                0x0004,
                business_email,
            )

            y += 14

        # =====================================================
        # RECEIPT TITLE
        # =====================================================

        y += 10

        painter.setPen(
            QPen(
                dark
            )
        )

        painter.setFont(
            title_font
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                25,
            ),
            0x0004,
            "SALES RECEIPT",
        )

        y += 30

        # =====================================================
        # TOP SEPARATOR
        # =====================================================

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            border,
        )

        y += 14

        # =====================================================
        # SALE INFORMATION BOX
        # =====================================================

        info_height = 76

        painter.setPen(
            QPen(
                border
            )
        )

        painter.setBrush(
            self._brush(
                soft_background
            )
        )

        painter.drawRoundedRect(
            QRectF(
                content_left,
                y,
                content_width,
                info_height,
            ),
            5,
            5,
        )

        painter.setBrush(
            self._brush(
                "#FFFFFF"
            )
        )

        info_y = y + 9

        painter.setFont(
            label_font
        )

        painter.setPen(
            QPen(
                dark
            )
        )

        self._draw_info_row(
            painter,
            "Invoice",
            sale.invoice_number,
            content_left + 10,
            info_y,
            content_width - 20,
        )

        info_y += 20

        self._draw_info_row(
            painter,
            "Date",
            sale.sale_date.strftime(
                "%d-%m-%Y"
            ),
            content_left + 10,
            info_y,
            content_width - 20,
        )

        info_y += 20

        customer = sale.customer

        customer_name = (
            "Walk-in Customer"
        )

        if customer is not None:
            customer_name = customer.name

        self._draw_info_row(
            painter,
            "Customer",
            customer_name,
            content_left + 10,
            info_y,
            content_width - 20,
        )

        y += info_height + 16

        # =====================================================
        # CUSTOMER EXTRA INFORMATION
        # =====================================================

        if customer is not None:

            customer_phone = (
                customer.phone
                or ""
            )

            customer_address = (
                customer.address
                or ""
            )

            if customer_phone:

                painter.setFont(
                    small_font
                )

                painter.setPen(
                    QPen(
                        medium
                    )
                )

                painter.drawText(
                    QRectF(
                        content_left,
                        y,
                        content_width,
                        18,
                    ),
                    0,
                    f"Phone: {customer_phone}",
                )

                y += 16

            if customer_address:

                painter.drawText(
                    QRectF(
                        content_left,
                        y,
                        content_width,
                        18,
                    ),
                    0,
                    f"Address: {customer_address}",
                )

                y += 16

            if customer_phone or customer_address:
                y += 5

        # =====================================================
        # ITEMS TABLE
        # =====================================================

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            border,
        )

        y += 13

        # =====================================================
        # COLUMN WIDTHS
        # =====================================================

        item_width = (
            content_width * 0.43
        )

        qty_width = (
            content_width * 0.12
        )

        price_width = (
            content_width * 0.21
        )

        amount_width = (
            content_width
            - item_width
            - qty_width
            - price_width
        )

        item_x = content_left

        qty_x = (
            item_x
            + item_width
        )

        price_x = (
            qty_x
            + qty_width
        )

        amount_x = (
            price_x
            + price_width
        )

        # =====================================================
        # TABLE HEADER
        # =====================================================

        painter.setFont(
            header_font
        )

        painter.setPen(
            QPen(
                dark
            )
        )

        header_height = 22

        painter.drawText(
            QRectF(
                item_x,
                y,
                item_width,
                header_height,
            ),
            0,
            "ITEM",
        )

        painter.drawText(
            QRectF(
                qty_x,
                y,
                qty_width,
                header_height,
            ),
            0x0002,
            "QTY",
        )

        painter.drawText(
            QRectF(
                price_x,
                y,
                price_width,
                header_height,
            ),
            0x0002,
            "PRICE",
        )

        painter.drawText(
            QRectF(
                amount_x,
                y,
                amount_width,
                header_height,
            ),
            0x0002,
            "AMOUNT",
        )

        y += header_height

        # =====================================================
        # HEADER LINE
        # =====================================================

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            dark,
        )

        y += 8

        # =====================================================
        # ITEMS
        # =====================================================

        painter.setFont(
            normal_font
        )

        painter.setPen(
            QPen(
                dark
            )
        )

        for item in sale.items:

            variant = (
                item.product_variant
            )

            product_name = (
                variant.product.name
            )

            length = getattr(
                variant,
                "length",
                None,
            )

            if length is not None:

                item_text = (
                    f"{product_name}"
                    f" ({length} yards)"
                )

            else:

                item_text = (
                    product_name
                )

            quantity = (
                item.quantity
            )

            unit_price = (
                item.unit_price
            )

            line_total = (
                Decimal(quantity)
                * unit_price
            )

            row_height = 25

            painter.drawText(
                QRectF(
                    item_x,
                    y,
                    item_width,
                    row_height,
                ),
                0,
                item_text,
            )

            painter.drawText(
                QRectF(
                    qty_x,
                    y,
                    qty_width,
                    row_height,
                ),
                0x0002,
                str(quantity),
            )

            painter.drawText(
                QRectF(
                    price_x,
                    y,
                    price_width,
                    row_height,
                ),
                0x0002,
                self._money(
                    unit_price
                ),
            )

            painter.drawText(
                QRectF(
                    amount_x,
                    y,
                    amount_width,
                    row_height,
                ),
                0x0002,
                self._money(
                    line_total
                ),
            )

            y += row_height

        # =====================================================
        # TOTAL SEPARATOR
        # =====================================================

        y += 5

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            dark,
        )

        y += 14

        # =====================================================
        # TOTAL BOX
        # =====================================================

        total_height = 42

        painter.setPen(
            QPen(
                dark
            )
        )

        painter.setBrush(
            self._brush(
                soft_background
            )
        )

        painter.drawRoundedRect(
            QRectF(
                content_left,
                y,
                content_width,
                total_height,
            ),
            5,
            5,
        )

        painter.setBrush(
            self._brush(
                "#FFFFFF"
            )
        )

        painter.setFont(
            total_label_font
        )

        painter.setPen(
            QPen(
                dark
            )
        )

        painter.drawText(
            QRectF(
                content_left + 12,
                y + 8,
                content_width * 0.50,
                26,
            ),
            0,
            "TOTAL",
        )

        total_text = (
            f"{currency} "
            f"{self._money(sale.total_amount)}"
        )

        painter.setFont(
            total_value_font
        )

        painter.drawText(
            QRectF(
                content_left
                + content_width * 0.50,
                y + 7,
                content_width * 0.50 - 12,
                28,
            ),
            0x0002,
            total_text,
        )

        y += total_height + 12

        # =====================================================
        # PAYMENT SUMMARY
        # =====================================================

        payment_height = 84

        painter.setPen(
            QPen(
                border
            )
        )

        painter.setBrush(
            self._brush(
                "#FFFFFF"
            )
        )

        painter.drawRoundedRect(
            QRectF(
                content_left,
                y,
                content_width,
                payment_height,
            ),
            5,
            5,
        )

        painter.setBrush(
            self._brush(
                "#FFFFFF"
            )
        )

        payment_x = (
            content_left + 12
        )

        payment_width = (
            content_width - 24
        )

        painter.setFont(
            payment_label_font
        )

        painter.setPen(
            QPen(
                dark
            )
        )

        painter.drawText(
            QRectF(
                payment_x,
                y + 9,
                payment_width * 0.50,
                20,
            ),
            0,
            "TOTAL",
        )

        painter.drawText(
            QRectF(
                payment_x,
                y + 31,
                payment_width * 0.50,
                20,
            ),
            0,
            "PAID",
        )

        painter.drawText(
            QRectF(
                payment_x,
                y + 53,
                payment_width * 0.50,
                20,
            ),
            0,
            "BALANCE DUE",
        )

        painter.setFont(
            payment_value_font
        )

        painter.drawText(
            QRectF(
                payment_x
                + payment_width * 0.50,
                y + 9,
                payment_width * 0.50,
                20,
            ),
            0x0002,
            f"{currency} {self._money(sale.total_amount)}",
        )

        painter.drawText(
            QRectF(
                payment_x
                + payment_width * 0.50,
                y + 31,
                payment_width * 0.50,
                20,
            ),
            0x0002,
            f"{currency} {self._money(paid)}",
        )

        painter.drawText(
            QRectF(
                payment_x
                + payment_width * 0.50,
                y + 53,
                payment_width * 0.50,
                20,
            ),
            0x0002,
            f"{currency} {self._money(balance)}",
        )

        y += payment_height + 20

        # =====================================================
        # FOOTER
        # =====================================================

        footer_height = 55.0

        footer_y = (
            page_height
            - 30.0
            - footer_height
        )

        minimum_footer_y = (
            y + 15.0
        )

        if footer_y < minimum_footer_y:

            footer_y = (
                minimum_footer_y
            )

        self._draw_separator(
            painter,
            content_left,
            content_width,
            footer_y,
            border,
        )

        footer_y += 10

        painter.setFont(
            small_font
        )

        painter.setPen(
            QPen(
                medium
            )
        )

        if footer:

            painter.drawText(
                QRectF(
                    content_left,
                    footer_y,
                    content_width,
                    25,
                ),
                0x0004,
                footer,
            )

            footer_y += 25

        painter.setFont(
            small_font
        )

        painter.setPen(
            QPen(
                light
            )
        )

        painter.drawText(
            QRectF(
                content_left,
                footer_y,
                content_width,
                20,
            ),
            0x0004,
            "Thank you for your business.",
        )

    # =========================================================
    # INFO ROW
    # =========================================================

    @staticmethod
    def _draw_info_row(
        painter: QPainter,
        label: str,
        value: str,
        x: float,
        y: float,
        width: float,
    ) -> None:

        label_width = (
            width * 0.25
        )

        label_font = QFont(
            "Noto Sans",
            8,
        )

        label_font.setBold(
            True
        )

        value_font = QFont(
            "Noto Sans",
            9,
        )

        painter.setFont(
            label_font
        )

        painter.setPen(
            QPen(
                "#555555"
            )
        )

        painter.drawText(
            QRectF(
                x,
                y,
                label_width,
                18,
            ),
            0,
            f"{label}:",
        )

        painter.setFont(
            value_font
        )

        painter.setPen(
            QPen(
                "#202020"
            )
        )

        painter.drawText(
            QRectF(
                x + label_width,
                y,
                width - label_width,
                18,
            ),
            0,
            value,
        )

    # =========================================================
    # SEPARATOR
    # =========================================================

    @staticmethod
    def _draw_separator(
        painter: QPainter,
        x: float,
        width: float,
        y: float,
        color: str,
    ) -> None:

        pen = QPen()

        pen.setColor(
            color
        )

        pen.setWidth(
            1
        )

        painter.setPen(
            pen
        )

        painter.drawLine(
            int(x),
            int(y),
            int(x + width),
            int(y),
        )

    # =========================================================
    # BRUSH
    # =========================================================

    @staticmethod
    def _brush(
        color: str,
    ):
        from PySide6.QtGui import (
            QColor,
            QBrush,
        )

        return QBrush(
            QColor(color)
        )

    # =========================================================
    # FORMAT MONEY
    # =========================================================

    @staticmethod
    def _money(
        value: Decimal,
    ) -> str:

        return f"{value:,.2f}"
