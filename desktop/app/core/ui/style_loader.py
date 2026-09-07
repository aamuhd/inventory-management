from pathlib import Path

from PySide6.QtWidgets import QApplication


STYLE_DIR = Path(__file__).parent / "styles"


def load_stylesheet(
    app: QApplication,
    *filenames: str,
) -> None:

    stylesheets = []

    for filename in filenames:

        path = STYLE_DIR / filename
        

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            stylesheets.append(
                file.read()
            )

    app.setStyleSheet(
        "\n\n".join(stylesheets)
    )