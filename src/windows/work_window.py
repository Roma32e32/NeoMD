from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from windows.work_window_subwidgets.file_tree import *

__all__ = ["WorkWindow"]


class WorkWindow(QWidget):
    def __init__(self):
        super().__init__()

        spliter = QSplitter(Qt.Orientation.Horizontal)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)

        self.file_tree = FileTree()

        spliter.addWidget(self.file_tree)
        spliter.addWidget(self.tabs)

        layout = QVBoxLayout()
        layout.addWidget(spliter)
        self.setLayout(layout)

        self.file_tree.file_opened.connect(lambda a: self.tabs.addTab(QLabel(a), a.split('/')[-1]))
        self.tabs.tabCloseRequested.connect(lambda a: self.tabs.removeTab(a))


    def update_dir(self, dir_path: str):
        self.file_tree.update_dir(dir_path)