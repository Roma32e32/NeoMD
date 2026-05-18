from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from windows.work_window_subwidgets.file_tree import *
from windows.work_window_subwidgets.md_editor import MDEditor
from windows.work_window_subwidgets.graph import Graph
from pathlib import Path

__all__ = ["WorkWindow"]


class WorkWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.path = ''

        spliter = QSplitter(Qt.Orientation.Horizontal)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)

        self.file_tree = FileTree()

        spliter.addWidget(self.file_tree)
        spliter.addWidget(self.tabs)
        spliter.setSizes([280, 1000])


        layout = QVBoxLayout()
        layout.addWidget(spliter)
        self.setLayout(layout)

        self.file_tree.md_opened.connect(self.on_md_opened)
        self.file_tree.graph_opened.connect(self.on_graph_opened)
        self.tabs.tabCloseRequested.connect(self.on_tab_closed)

    def on_tab_closed(self, index):
        try:
            self.tabs.widget(index).deleteLater()
            self.tabs.removeTab(index)
        except AttributeError:
            pass

    def on_md_opened(self, path, new):
        path = path.replace('\\', '/')
        if not new:
            self.tabs.addTab(MDEditor(self.path, path, self.on_md_opened), path.split('/')[-1])
        else:
            self.tabs.tabCloseRequested.emit(self.tabs.currentIndex())
            self.tabs.addTab(MDEditor(self.path, path, self.on_md_opened), path.split('/')[-1])

    def on_graph_opened(self, path):
        if path.is_file():
            self.tabs.addTab(Graph(self.path, path, self), f"Локальный граф {path}")
        else:
            self.tabs.addTab(Graph(self.path, None, self), "Граф")

    def update_dir(self, dir_path: Path):
        self.file_tree.update_dir(dir_path)
        self.path = dir_path