from PySide6.QtWidgets import *

__all__ = ["WorkMenu"]


class WorkMenu(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.btn = QPushButton("blue")

        layout.addWidget(self.btn)