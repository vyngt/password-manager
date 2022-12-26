import functools
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QApplication,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QDockWidget,
    QLayout,
    QInputDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)
from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtCore import Qt

from core.db import get_session
from core.db.models import Item
from conf import settings

__all__ = ["MainWindow"]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initialize()

    def initialize(self):
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(800, 480)
        self.setWindowTitle("V Password Manager")
        self.setWindowIcon(
            QIcon(str(settings.STATIC_ROOT / "images" / "white_fox_lg.png"))
        )
        self.setup_interface()
        self.show()

    def setup_interface(self):
        self.setup_layout()
        self.create_actions()
        self.create_menu()
        self.create_dock_widgets()

    def setup_layout(self):
        self.container = QWidget()
        vbox_layout = QVBoxLayout(self.container)

        self.table = self.create_table_widget()

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

    def create_table_widget(self) -> QTableWidget:
        headers = ("ID", "Name", "username", "URL")

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSortingEnabled(True)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)

        with get_session() as session:
            for item in session.query(Item).all():
                position = table.rowCount()
                table.insertRow(position)
                for c in range(len(headers)):
                    text = str(getattr(item, headers[c].lower()))
                    table.setItem(position, c, QTableWidgetItem(text))

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
        btn_view = QPushButton("View")

        dock_layout = QVBoxLayout()
        dock_layout.addWidget(btn_refresh)
        dock_layout.addWidget(btn_add)
        dock_layout.addWidget(btn_view)

        if end_stretch:
            dock_layout.addStretch(1)

        return dock_layout

    def retrieve_items(self):
        with get_session() as session:
            for item in session.query(Item).all():
                print(item)

    def add_item(self):
        text, ok = QInputDialog.getText(self, "New Item", "Add Item")

    def update_item(self):
        pass

    def delete_item(self):
        pass
