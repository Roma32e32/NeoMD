from PySide6.QtCore import Signal
from PySide6.QtWidgets import *

class FileTree(QWidget):
    file_opened = Signal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.file_system = QFileSystemModel()
        self.file_tree_view = QTreeView()
        self.file_tree_view.setModel(self.file_system)

        self.file_tree_view.hideColumn(1)
        self.file_tree_view.doubleClicked.connect(self.__on_file_double_clicked)

    def update_dir(self, path):
        path = path.replace('\n', '')
        self.file_system.setRootPath(path)
        self.file_tree_view.setRootIndex(self.file_system.index(path))

    def __on_file_double_clicked(self, index):
        if self.file_system.isDir(index):
            return
        else:
            self.file_opened.emit(self.file_system.filePath(index))