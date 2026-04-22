from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from windows.work_window_subwidgets.file_tree import *
from work_window_subwidgets.md_editor import MDEditor

__all__ = ["WorkWindow"]


class WorkWindow(QWidget):
    def __init__(self):
        super().__init__()

        spliter = QSplitter(Qt.Orientation.Horizontal)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)

        self.file_tree = FileTree()

        spliter.addWidget(self.file_tree)
        spliter.addWidget(self.tabs)

        layout = QVBoxLayout()
        layout.addWidget(spliter)
        self.setLayout(layout)

        self.file_tree.md_opened.connect(self.on_md_opened)
        self.tabs.tabCloseRequested.connect(self.on_tab_closed)

    def on_tab_closed(self, index):
        self.tabs.widget(index).deleteLater()
        self.tabs.removeTab(index)

    def on_md_opened(self, path):
        self.tabs.addTab(MDEditor(path), path.split('/')[-1])

    def update_dir(self, dir_path: str):
        self.file_tree.update_dir(dir_path)