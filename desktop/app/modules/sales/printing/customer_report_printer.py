from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from PySide6.QtCore import QMarginsF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
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


class CustomerReportPrinter:

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        self._parent = parent

    # =========================================================
    # PRINT REPORT
    # =========================================================

    def print_report(
        self,
        customer,
        sales,
        start_date: date,
        end_date: date,
        settings,
        total_sales: Decimal,
        total_paid: Decimal,
        total_balance: Decimal,
        sale_paid: dict[Any, Decimal],
        sale_balance: dict[Any, Decimal],
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

        self._draw_report(
            device=printer,
            customer=customer,
            sales=sales,
            start_date=start_date,
            end_date=end_date,
            settings=settings,
            total_sales=total_sales,
            total_paid=total_paid,
            total_balance=total_balance,
            sale_paid=sale_paid,
            sale_balance=sale_balance,
        )

        return True

    # =========================================================
    # SAVE AS PDF
    # =========================================================

    def save_pdf(
        self,
        customer,
        sales,
        start_date: date,
        end_date: date,
        settings,
        total_sales: Decimal,
        total_paid: Decimal,
        total_balance: Decimal,
        sale_paid: dict[Any, Decimal],
        sale_balance: dict[Any, Decimal],
    ) -> bool:

        default_name = (
            "customer_report_"
            f"{self._safe_filename(customer.name)}.pdf"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self._parent,
            "Save Customer Report as PDF",
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

        self._draw_report(
            device=writer,
            customer=customer,
            sales=sales,
            start_date=start_date,
            end_date=end_date,
            settings=settings,
            total_sales=total_sales,
            total_paid=total_paid,
            total_balance=total_balance,
            sale_paid=sale_paid,
            sale_balance=sale_balance,
        )

        return True

    # =========================================================
    # DRAW REPORT
    # =========================================================

    def _draw_report(
        self,
        device,
        customer,
        sales,
        start_date: date,
        end_date: date,
        settings,
        total_sales: Decimal,
        total_paid: Decimal,
        total_balance: Decimal,
        sale_paid: dict[Any, Decimal],
        sale_balance: dict[Any, Decimal],
    ) -> None:

        painter = QPainter()

        if not painter.begin(device):
            raise RuntimeError(
                "Unable to start customer report printer."
            )

        try:

            resolution = device.resolution()

            if resolution <= 0:
                resolution = 96

            scale = resolution / 72.0

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

            content_width = (
                page_width
                - (margin * 2)
            )

            self._draw_report_page(
                painter=painter,
                customer=customer,
                sales=sales,
                start_date=start_date,
                end_date=end_date,
                settings=settings,
                page_width=page_width,
                page_height=page_height,
                content_left=content_left,
                content_width=content_width,
                total_sales=total_sales,
                total_paid=total_paid,
                total_balance=total_balance,
                sale_paid=sale_paid,
                sale_balance=sale_balance,
            )

        finally:

            painter.end()

    # =========================================================
    # REPORT PAGE
    # =========================================================

    def _draw_report_page(
        self,
        painter: QPainter,
        customer,
        sales,
        start_date: date,
        end_date: date,
        settings,
        page_width: float,
        page_height: float,
        content_left: float,
        content_width: float,
        total_sales: Decimal,
        total_paid: Decimal,
        total_balance: Decimal,
        sale_paid: dict[Any, Decimal],
        sale_balance: dict[Any, Decimal],
    ) -> None:

        # =====================================================
        # FONTS
        # =====================================================

        normal_font = QFont(
            "Noto Sans",
            8,
        )

        small_font = QFont(
            "Noto Sans",
            8,
        )

        label_font = QFont(
            "Noto Sans",
            9,
        )
        label_font.setBold(True)

        business_font = QFont(
            "Noto Sans",
            20,
        )
        business_font.setBold(True)

        title_font = QFont(
            "Noto Sans",
            14,
        )
        title_font.setBold(True)

        header_font = QFont(
            "Noto Sans",
            8,
        )
        header_font.setBold(True)

        value_font = QFont(
            "Noto Sans",
            10,
        )
        value_font.setBold(True)

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
        # SUMMARY VALUES
        # =====================================================

        total_items = 0

        for sale in sales:

            for item in sale.items:
                total_items += item.quantity

        number_of_sales = len(
            sales
        )

        average_sale = (
            total_sales / number_of_sales
            if number_of_sales
            else Decimal("0.00")
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
        # START
        # =====================================================

        y = 35.0

        # =====================================================
        # BUSINESS NAME
        # =====================================================

        painter.setPen(
            QPen(dark)
        )

        painter.setFont(
            business_font
        )

        business_height = self._text_height(
            painter,
            business_name,
            content_width,
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                business_height,
            ),
            Qt.AlignmentFlag.AlignCenter
            | Qt.TextFlag.TextWordWrap,
            business_name,
        )

        y += business_height + 5

        # =====================================================
        # BUSINESS INFORMATION
        # =====================================================

        painter.setFont(
            small_font
        )

        painter.setPen(
            QPen(medium)
        )

        for text in (
            business_address,
            business_phone,
            business_email,
        ):

            if not text:
                continue

            text_height = self._text_height(
                painter,
                text,
                content_width,
            )

            painter.drawText(
                QRectF(
                    content_left,
                    y,
                    content_width,
                    text_height,
                ),
                Qt.AlignmentFlag.AlignCenter
                | Qt.TextFlag.TextWordWrap,
                text,
            )

            y += text_height + 2

        # =====================================================
        # TITLE
        # =====================================================

        y += 10

        painter.setFont(
            title_font
        )

        painter.setPen(
            QPen(dark)
        )

        title_height = 24

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                title_height,
            ),
            Qt.AlignmentFlag.AlignCenter,
            "CUSTOMER SALES REPORT",
        )

        y += title_height + 8

        # =====================================================
        # SEPARATOR
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
        # CUSTOMER INFORMATION
        # =====================================================

        customer_rows = (
            ("Customer", customer.name),
            ("Phone", customer.phone or "-"),
            ("Email", customer.email or "-"),
            ("Address", customer.address or "-"),
        )

        customer_value_width = (
            content_width * 0.75
        )

        row_heights = []

        painter.setFont(
            QFont(
                "Noto Sans",
                9,
            )
        )

        for _, value in customer_rows:

            row_height = max(
                20.0,
                self._text_height(
                    painter,
                    value,
                    customer_value_width - 10,
                ),
            )

            row_heights.append(
                row_height
            )

        info_height = (
            sum(row_heights)
            + 18
        )

        painter.setPen(
            QPen(border)
        )

        painter.setBrush(
            QBrush(
                QColor(soft_background)
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
            QBrush(
                QColor("#FFFFFF")
            )
        )

        info_y = y + 9

        for index, (
            label,
            value,
        ) in enumerate(customer_rows):

            row_height = row_heights[index]

            self._draw_info_row(
                painter,
                label,
                value,
                content_left + 10,
                info_y,
                content_width - 20,
                row_height,
            )

            info_y += row_height

        y += info_height + 16

        # =====================================================
        # REPORT PERIOD
        # =====================================================

        painter.setFont(
            label_font
        )

        painter.setPen(
            QPen(dark)
        )

        period_text = (
            "Report Period: "
            f"{start_date.strftime('%d-%m-%Y')} "
            "to "
            f"{end_date.strftime('%d-%m-%Y')}"
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                20,
            ),
            Qt.AlignmentFlag.AlignLeft,
            period_text,
        )

        y += 25

        # =====================================================
        # SUMMARY
        # =====================================================

        summary_height = 62.0

        column_width = (
            content_width / 4
        )

        painter.setPen(
            QPen(border)
        )

        painter.setBrush(
            QBrush(
                QColor(soft_background)
            )
        )

        painter.drawRoundedRect(
            QRectF(
                content_left,
                y,
                content_width,
                summary_height,
            ),
            5,
            5,
        )

        painter.setBrush(
            QBrush(
                QColor("#FFFFFF")
            )
        )

        summary = (
            (
                "TOTAL",
                f"{currency} "
                f"{self._money(total_sales)}",
            ),
            (
                "PAID",
                f"{currency} "
                f"{self._money(total_paid)}",
            ),
            (
                "BALANCE",
                f"{currency} "
                f"{self._money(total_balance)}",
            ),
            (
                "SALES",
                str(number_of_sales),
            ),
        )

        for index, (
            label,
            value,
        ) in enumerate(summary):

            x = (
                content_left
                + index * column_width
            )

            painter.setFont(
                header_font
            )

            painter.setPen(
                QPen(medium)
            )

            painter.drawText(
                QRectF(
                    x + 6,
                    y + 8,
                    column_width - 12,
                    18,
                ),
                Qt.AlignmentFlag.AlignCenter,
                label,
            )

            painter.setFont(
                value_font
            )

            painter.setPen(
                QPen(dark)
            )

            painter.drawText(
                QRectF(
                    x + 6,
                    y + 29,
                    column_width - 12,
                    24,
                ),
                Qt.AlignmentFlag.AlignCenter,
                value,
            )

        y += summary_height + 8

        # =====================================================
        # SECONDARY SUMMARY
        # =====================================================

        painter.setFont(
            small_font
        )

        painter.setPen(
            QPen(medium)
        )

        secondary_summary = (
            f"Items Purchased: {total_items}"
            "    |    "
            f"Average Sale: {currency} "
            f"{self._money(average_sale)}"
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width,
                20,
            ),
            Qt.AlignmentFlag.AlignCenter,
            secondary_summary,
        )

        y += 25

        # =====================================================
        # SALES TABLE
        # =====================================================

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            border,
        )

        y += 13

        invoice_width = (
            content_width * 0.20
        )

        date_width = (
            content_width * 0.14
        )

        items_width = (
            content_width * 0.09
        )

        total_width = (
            content_width * 0.19
        )

        paid_width = (
            content_width * 0.19
        )

        balance_width = (
            content_width
            - invoice_width
            - date_width
            - items_width
            - total_width
            - paid_width
        )

        invoice_x = content_left

        date_x = (
            invoice_x
            + invoice_width
        )

        items_x = (
            date_x
            + date_width
        )

        total_x = (
            items_x
            + items_width
        )

        paid_x = (
            total_x
            + total_width
        )

        balance_x = (
            paid_x
            + paid_width
        )

        # =====================================================
        # TABLE HEADER
        # =====================================================

        header_height = 22.0

        painter.setFont(
            header_font
        )

        painter.setPen(
            QPen(dark)
        )

        painter.drawText(
            QRectF(
                invoice_x,
                y,
                invoice_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignLeft,
            "INVOICE",
        )

        painter.drawText(
            QRectF(
                date_x,
                y,
                date_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignLeft,
            "DATE",
        )

        painter.drawText(
            QRectF(
                items_x,
                y,
                items_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignRight,
            "ITEMS",
        )

        painter.drawText(
            QRectF(
                total_x,
                y,
                total_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignRight,
            "TOTAL",
        )

        painter.drawText(
            QRectF(
                paid_x,
                y,
                paid_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignRight,
            "PAID",
        )

        painter.drawText(
            QRectF(
                balance_x,
                y,
                balance_width,
                header_height,
            ),
            Qt.AlignmentFlag.AlignRight,
            "BALANCE",
        )

        y += header_height

        self._draw_separator(
            painter,
            content_left,
            content_width,
            y,
            dark,
        )

        y += 8

        # =====================================================
        # TABLE ROWS
        # =====================================================

        painter.setFont(
            normal_font
        )

        painter.setPen(
            QPen(dark)
        )

        for sale in sales:

            total_sale_items = sum(
                item.quantity
                for item in sale.items
            )

            paid = sale_paid.get(
                sale.id,
                Decimal("0.00"),
            )

            balance = sale_balance.get(
                sale.id,
                Decimal("0.00"),
            )

            invoice_text = (
                sale.invoice_number
            )

            total_text = (
                f"{currency} "
                f"{self._money(sale.total_amount)}"
            )

            paid_text = (
                f"{currency} "
                f"{self._money(paid)}"
            )

            balance_text = (
                f"{currency} "
                f"{self._money(balance)}"
            )

            row_height = max(
                24.0,
                self._text_height(
                    painter,
                    invoice_text,
                    invoice_width - 4,
                ),
                self._text_height(
                    painter,
                    total_text,
                    total_width - 4,
                ),
                self._text_height(
                    painter,
                    paid_text,
                    paid_width - 4,
                ),
                self._text_height(
                    painter,
                    balance_text,
                    balance_width - 4,
                ),
            )

            painter.drawText(
                QRectF(
                    invoice_x,
                    y,
                    invoice_width - 4,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignLeft
                | Qt.TextFlag.TextWordWrap,
                invoice_text,
            )

            painter.drawText(
                QRectF(
                    date_x,
                    y,
                    date_width,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignLeft,
                sale.sale_date.strftime(
                    "%Y-%m-%d"
                ),
            )

            painter.drawText(
                QRectF(
                    items_x,
                    y,
                    items_width,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignRight,
                str(total_sale_items),
            )

            painter.drawText(
                QRectF(
                    total_x,
                    y,
                    total_width - 4,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignRight
                | Qt.TextFlag.TextWordWrap,
                total_text,
            )

            painter.drawText(
                QRectF(
                    paid_x,
                    y,
                    paid_width - 4,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignRight
                | Qt.TextFlag.TextWordWrap,
                paid_text,
            )

            painter.drawText(
                QRectF(
                    balance_x,
                    y,
                    balance_width - 4,
                    row_height,
                ),
                Qt.AlignmentFlag.AlignRight
                | Qt.TextFlag.TextWordWrap,
                balance_text,
            )

            y += row_height + 2

        # =====================================================
        # TOTAL
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

        total_height = 44.0

        painter.setPen(
            QPen(dark)
        )

        painter.setBrush(
            QBrush(
                QColor(soft_background)
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
            QBrush(
                QColor("#FFFFFF")
            )
        )

        painter.setFont(
            value_font
        )

        painter.setPen(
            QPen(dark)
        )

        painter.drawText(
            QRectF(
                content_left + 12,
                y + 8,
                content_width * 0.25,
                28,
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.TextFlag.TextSingleLine,
            "TOTAL",
        )

        painter.drawText(
            QRectF(
                content_left
                + content_width * 0.25,
                y + 7,
                content_width * 0.25 - 12,
                30,
            ),
            Qt.AlignmentFlag.AlignRight
            | Qt.TextFlag.TextSingleLine,
            f"{currency} "
            f"{self._money(total_sales)}",
        )

        painter.drawText(
            QRectF(
                content_left
                + content_width * 0.50,
                y + 8,
                content_width * 0.25,
                28,
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.TextFlag.TextSingleLine,
            "PAID",
        )

        painter.drawText(
            QRectF(
                content_left
                + content_width * 0.75,
                y + 7,
                content_width * 0.25 - 12,
                30,
            ),
            Qt.AlignmentFlag.AlignRight
            | Qt.TextFlag.TextSingleLine,
            f"{currency} "
            f"{self._money(total_paid)}",
        )

        y += total_height + 8

        painter.setFont(
            value_font
        )

        painter.setPen(
            QPen(dark)
        )

        painter.drawText(
            QRectF(
                content_left,
                y,
                content_width * 0.50,
                30,
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.TextFlag.TextSingleLine,
            "BALANCE",
        )

        painter.drawText(
            QRectF(
                content_left
                + content_width * 0.50,
                y,
                content_width * 0.50,
                30,
            ),
            Qt.AlignmentFlag.AlignRight
            | Qt.TextFlag.TextSingleLine,
            f"{currency} "
            f"{self._money(total_balance)}",
        )

        y += 38

        # =====================================================
        # FOOTER
        # =====================================================

        footer_height = 65.0

        footer_y = (
            page_height
            - 30.0
            - footer_height
        )

        if footer_y < y + 15.0:

            footer_y = (
                y + 15.0
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
            QPen(medium)
        )

        if footer:

            footer_text_height = (
                self._text_height(
                    painter,
                    footer,
                    content_width,
                )
            )

            painter.drawText(
                QRectF(
                    content_left,
                    footer_y,
                    content_width,
                    footer_text_height,
                ),
                Qt.AlignmentFlag.AlignCenter
                | Qt.TextFlag.TextWordWrap,
                footer,
            )

            footer_y += (
                footer_text_height
                + 8
            )

        painter.setPen(
            QPen(light)
        )

        painter.drawText(
            QRectF(
                content_left,
                footer_y,
                content_width,
                20,
            ),
            Qt.AlignmentFlag.AlignCenter,
            "Customer sales report.",
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
        height: float,
    ) -> None:

        label_width = (
            width * 0.25
        )

        label_font = QFont(
            "Noto Sans",
            8,
        )

        label_font.setBold(True)

        value_font = QFont(
            "Noto Sans",
            9,
        )

        painter.setFont(
            label_font
        )

        painter.setPen(
            QPen("#555555")
        )

        painter.drawText(
            QRectF(
                x,
                y,
                label_width,
                height,
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter,
            f"{label}:",
        )

        painter.setFont(
            value_font
        )

        painter.setPen(
            QPen("#202020")
        )

        painter.drawText(
            QRectF(
                x + label_width,
                y,
                width - label_width,
                height,
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
            | Qt.TextFlag.TextWordWrap,
            value,
        )

    # =========================================================
    # TEXT HEIGHT
    # =========================================================

    @staticmethod
    def _text_height(
        painter: QPainter,
        text: str,
        width: float,
    ) -> float:

        if not text:
            return 18.0

        rectangle = QRectF(
            0,
            0,
            width,
            1000,
        )

        flags = Qt.TextFlag.TextWordWrap

        bounding_rect = (
            painter.boundingRect(
                rectangle,
                flags,
                text,
            )
        )

        return max(
            18.0,
            bounding_rect.height(),
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
    # FORMAT MONEY
    # =========================================================

    @staticmethod
    def _money(
        value: Decimal,
    ) -> str:

        return f"{value:,.2f}"

    # =========================================================
    # SAFE FILENAME
    # =========================================================

    @staticmethod
    def _safe_filename(
        name: str,
    ) -> str:

        invalid = '<>:"/\\|?*'

        safe = "".join(
            "_"
            if character in invalid
            else character
            for character in name
        ).strip()

        return safe or "customer"
