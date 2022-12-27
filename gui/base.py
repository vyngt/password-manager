from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)


class StandardButton:
    def create_btn(self, accept_btn_name: str, reject_btn_name: str):
        btn_accept = QPushButton(accept_btn_name)
        btn_reject = QPushButton(reject_btn_name)

        # For something base on QDialog
        btn_accept.clicked.connect(self.accept)  # type: ignore
        btn_reject.clicked.connect(self.reject)  # type: ignore

        container = QWidget()

        h_box = QHBoxLayout(container)
        h_box.addStretch(1)
        h_box.addWidget(btn_accept)
        h_box.addWidget(btn_reject)
        return container
