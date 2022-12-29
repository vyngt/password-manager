import sys
from typing import Any

from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QDockWidget,
    QLayout,
)
from PyQt6.QtGui import QAction, QIcon, QStandardItem
from PyQt6.QtCore import Qt

from conf import settings

from core.encryption import Encryptor
from .vault import VaultItemTableView, Vault, VaultForm, TVault
from .auth import LoginDialog, SetMasterPasswordDialog

__all__ = ["MainWindow"]


class MainWindow(QMainWindow):
    PROFILE = settings.PROFILE

    def __init__(self) -> None:
        super().__init__()
        self.master_pwd: str = ""
        self.initialize()

    def initialize(self):
        self.initializeUI()
        self.authenticate()
        self.start()

    def initializeUI(self):
        self.setMinimumSize(800, 480)
        self.setWindowTitle("V Password Manager")
        self.setWindowIcon(QIcon(str(settings.STATIC_ROOT / "images" / "app_icon.ico")))
        self.setup_interface()
        self.show()

    def setup_interface(self):
        self.setup_layout()
        self.create_dock_widgets()
        self.create_actions()
        self.create_menu()

    def authenticate(self):
        try:
            hashed_master_pwd = ""
            with open(self.PROFILE, "rb") as f:
                hashed_master_pwd = b64decode(f.read()).decode()
                self.login(hashed_master_pwd)

        except FileNotFoundError:
            self.register()

    def login(self, hashed: str):
        dialog = LoginDialog(self, hashed)
        pwd, ok = dialog.exec()
        if not ok or not pwd:
            self.exit()

        self.master_pwd = pwd

    def register(self):
        dialog = SetMasterPasswordDialog(self)
        pwd, ok = dialog.exec()
        if not ok or not pwd:
            self.exit()
        else:
            with open(self.PROFILE, "wb") as f:
                h, p = pwd
                f.write(b64encode(h.encode()))
                self.master_pwd = p

    def start(self):
        self.encryptor = Encryptor(self.master_pwd)
        self.retrieve_items()

    def exit(self):
        self.close()

        # Force exit, temp solution
        sys.exit()

    def setup_layout(self):
        self.container = QWidget()
        vbox_layout = QVBoxLayout(self.container)

        self.table = self.create_table_view()
        vbox_layout.addWidget(self.create_search_widget())
        vbox_layout.addWidget(self.table)

        self.setCentralWidget(self.container)

    def create_search_widget(self) -> QWidget:
        widget = QWidget()
        h_box = QHBoxLayout(widget)
        line_edit = QLineEdit()
        btn_clear = QPushButton("Clear")
        btn_search = QPushButton("Search")

        h_box.addWidget(line_edit)
        h_box.addWidget(btn_clear)
        h_box.addWidget(btn_search)

        return widget

    def create_table_view(self):
        self.model = Vault()
        table = VaultItemTableView()
        table.setModel(self.model)

        return table

    def create_actions(self):
        self.create_file_actions()
        self.create_help_action()

    def create_file_actions(self):
        self.exit_act = QAction("&Exit")
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

    def create_help_action(self):
        self.about_act = QAction("&About")

    def create_menu(self):

        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.exit_act)

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(self.about_act)

    def create_dock_widgets(self):
        left_dock = QDockWidget()
        left_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        left_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        left_dock.setTitleBarWidget(QWidget(None))

        dock_container = QWidget()
        dock_container.setLayout(self.create_dock_btn())
        left_dock.setWidget(dock_container)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

    def create_dock_btn(self, end_stretch: bool = True) -> QLayout:
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.retrieve_items)
        btn_add = QPushButton("Add")
        btn_add.clicked.connect(self.add_item)
        btn_copy = QPushButton("Copy")
        btn_copy.clicked.connect(self.copy_password)
        btn_edit = QPushButton("Edit")
        btn_edit.clicked.connect(self.update_item)
        btn_remove = QPushButton("Remove")
        btn_remove.clicked.connect(self.delete_item)

        for btn in (btn_edit, btn_copy, btn_remove):
            btn.setEnabled(False)

        dock_layout = QVBoxLayout()
        dock_layout.addWidget(btn_refresh)
        dock_layout.addWidget(btn_add)
        dock_layout.addWidget(btn_copy)
        dock_layout.addWidget(btn_edit)
        dock_layout.addWidget(btn_remove)

        if end_stretch:
            dock_layout.addStretch(1)

        def table_select_on_change():
            for btn in (btn_edit, btn_copy, btn_remove):
                btn.setEnabled(bool(self.table.selectionModel().selectedRows()))

        self.table.selectionModel().selectionChanged.connect(table_select_on_change)

        return dock_layout

    def clear_data(self):
        while self.model.rowCount() > 0:
            self.model.removeRow(0)

    def perform_add_row(self, instance: Any):
        position = self.model.rowCount()
        items: list[QStandardItem] = []
        for field in self.model.objects.fields:
            _f = field.lower()
            content = str(getattr(instance, _f))
            if _f != "id":
                content = self.encryptor.decrypt(content)
            items.append(QStandardItem(content))
        self.model.insertRow(position, items)

    def retrieve_items(self):
        self.clear_data()
        for instance in self.model.objects.select():
            self.perform_add_row(instance)

    def add_item(self):
        form = VaultForm(self)
        data, ok = form.exec()
        if ok and data:
            d = {k: self.encryptor.encrypt(v) for k, v in data.items()}  # type: ignore
            instance = self.model.objects.insert(**d)
            self.perform_add_row(instance)

    def copy_password(self):
        _id = self.table.selectedIndexes()[0].data()
        password = self.encryptor.decrypt(self.model.objects.get(_id).password)
        QApplication.clipboard().setText(password)

    def update_item(self):
        row = self.table.selectedIndexes()
        _id = row[0].data()
        instance = self.model.objects.get(_id)

        original = self.encryptor.bulk_decrypt(
            {
                "name": instance.name,
                "url": instance.url,
                "username": instance.username,
                "password": instance.password,
            }
        )

        form = VaultForm(self, data=original)  # type: ignore
        data, ok = form.exec()
        if ok and data:
            enc_data = self.encryptor.bulk_encrypt(data)  # type: ignore
            self.model.objects.update(_id, **enc_data)
            self.retrieve_items()

    def delete_item(self):
        _id_obj = self.table.selectedIndexes()[0]
        self.model.objects.delete(_id_obj.data())
        self.model.removeRow(_id_obj.row())
