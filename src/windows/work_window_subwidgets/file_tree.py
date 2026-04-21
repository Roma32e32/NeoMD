from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QTreeView, QFileSystemModel

__all__ = ["FileTree"]

class FileTree(QTreeView):
    md_opened = Signal(str)
    graph_opened = Signal(str)
    img_opened = Signal(str)

    def __init__(self):
        super().__init__()

        self.file_system = QFileSystemModel()
        self.setModel(self.file_system)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)

    def update_dir(self, path):
        path = path.replace('\n', '')
        self.file_system.setRootPath(path)
        self.setRootIndex(self.file_system.index(path))

    def mouseDoubleClickEvent(self, event):
        self.md_opened.emit(self.file_system.filePath(self.indexAt(event.pos())))
        super().mouseDoubleClickEvent(event)