import sys

from PySide6.QtWidgets import QApplication

from app.modules.inventory.ui.product_form import ProductForm

app = QApplication(sys.argv)

window = ProductForm()
window.show()

sys.exit(app.exec())