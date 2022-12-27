from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QAbstractItemView,
    QDialog,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt

from core.encryption import hasher

from .base import StandardButton

__all__ = ["LoginDialog", "SetMasterPasswordDialog"]


class LoginDialog(QDialog, StandardButton):
    def __init__(self, parent: QWidget | None, hashed_pwd) -> None:
        super().__init__(parent)
        self.hashed = hashed_pwd
        self.master_password = QLineEdit()
        self.master_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.initialize()

    def initialize(self):
        self.setWindowTitle("Login")
        self.setMinimumSize(200, 100)
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.create_form())
        layout.addWidget(self.message)
        layout.addWidget(self.create_btn("Login", "Quit"))
        self.setLayout(layout)

    def create_form(self):
        container = QWidget()
        form = QFormLayout(container)
        form.addRow("Master Password", self.master_password)

        return container

    def accept(self) -> None:
        if hasher.verify_password(self.hashed, self.master_password.text()):
            return super().accept()
        else:
            self.message.setText("Failed")

    def exec(self):
        ok = super().exec()
        if ok:
            return self.master_password.text(), ok
        else:
            return None, ok


class SetMasterPasswordDialog(QDialog, StandardButton):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.password = QLineEdit()
        self.password2 = QLineEdit()

        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password2.setEchoMode(QLineEdit.EchoMode.Password)

        self.initialize()

    def initialize(self):
        self.setWindowTitle("Register")
        self.setMinimumSize(200, 100)
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.create_form())
        layout.addWidget(self.message)
        layout.addWidget(self.create_btn("OK", "Quit"))
        self.setLayout(layout)

    def create_form(self):
        container = QWidget()
        form = QFormLayout(container)
        form.addRow("Master Password", self.password)
        form.addRow("Retype Password", self.password2)

        return container

    def accept(self) -> None:
        pw1 = self.password.text()
        pw2 = self.password2.text()
        if pw1 and pw2 and pw1 == pw2:
            self.h = hasher.hash_password(pw1)
            if self.h:
                return super().accept()
        self.message.setText("Password not match or empty")

    def exec(self):
        ok = super().exec()
        if ok:
            data = self.h
        else:
            data = None
        return data, ok
