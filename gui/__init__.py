import sys
from PyQt6.QtWidgets import QApplication
from .windows import MainWindow


def open_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
