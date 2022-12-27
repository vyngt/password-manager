from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QAbstractItemView,
    QDialog,
    QLineEdit,
    QVBoxLayout,
    QFormLayout,
)
from PyQt6.QtGui import QStandardItemModel

from sqlalchemy import update

from core.db import get_session, Base
from core.db.models import Item

from .base import StandardButton

__all__ = [
    "VaultForm",
    "Vault",
    "VaultItemTableView",
]


class VaultFormSetField:
    def __init__(self) -> None:
        self.name = QLineEdit()
        self.url = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)


class VaultForm(QDialog, StandardButton):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.fields = VaultFormSetField()
        self.initialize()

    def initialize(self):
        self.setWindowTitle("Add Item")
        self.setMinimumSize(200, 200)
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()

        layout.addWidget(self.create_form())
        layout.addWidget(self.create_btn("Save", "Cancel"))
        self.setLayout(layout)

    def create_form(self):
        container = QWidget()

        form = QFormLayout(container)
        form.addRow("Name", self.fields.name)
        form.addRow("URL", self.fields.url)
        form.addRow("Username", self.fields.username)
        form.addRow("Password", self.fields.password)

        return container

    def get_data(self):
        name = self.fields.name.text()
        url = self.fields.url.text()
        username = self.fields.username.text()
        password = self.fields.password.text()

        return name, url, username, password

    def exec(self):
        ok = super().exec()
        if ok:
            data = self.get_data()
        else:
            data = ("", "", "", "")
        return data, ok


class VManager:
    fields: tuple[str, ...]

    def __init__(self, model: Base):
        self.model = model

    def set_fields(self, fields: tuple[str, ...]):
        self.fields = fields

    def select(self):
        with get_session() as session:
            result = session.query(self.model).all()
        return result

    def update(self, id: int | str, **kwargs):
        with get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == id).values(**kwargs)
            )
            session.commit()
            instance = session.query(self.model).get(id)
        return instance

    def insert(self, **kwargs):
        with get_session() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)

        return instance

    def delete(self, id: int | str):
        with get_session() as session:
            instance = session.query(self.model).get(id)
            if instance:
                session.delete(instance)
                session.commit()


class Vault(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.objects = VManager(Item)
        self.objects.set_fields(("ID", "Name", "username", "URL"))
        self.initialize()

    def initialize(self):
        self.setColumnCount(len(self.objects.fields))
        self.setHorizontalHeaderLabels(self.objects.fields)


class VaultItemTableView(QTableView):
    def __init__(self) -> None:
        super().__init__()
        self.initialize()

    def initialize(self):
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.horizontalHeader().setStretchLastSection(True)
