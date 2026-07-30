import sys

from PySide6.QtWidgets import QApplication

from app.modules.inventory.ui.category_form import CategoryForm

app = QApplication(sys.argv)

window = CategoryForm()
window.show()

sys.exit(app.exec())