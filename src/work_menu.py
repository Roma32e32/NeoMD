from PySide6.QtWidgets import *

__all__ = ["WorkMenu"]


class WorkMenu(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        upper_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.file_tree = QTreeWidget()
        self.text_edit = QTextEdit()

        content_layout.addWidget(self.file_tree)
        content_layout.addWidget(self.text_edit)

        main_layout.addLayout(upper_layout)
        main_layout.addLayout(content_layout)

        self.btn1 = QPushButton("123")
        self.btn2 = QPushButton("456")
        upper_layout.addWidget(self.btn1)
        upper_layout.addWidget(self.btn2)

    def update_dir(self, dir_path: str):
        pass