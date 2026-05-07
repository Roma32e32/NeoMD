from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QAbstractItemView
from work_window_subwidgets.context_menu import ContextMenu
import shutil
import os

__all__ = ["FileTree"]

class FileTree(QTreeView):
    class FileSystem(QFileSystemModel):
        def flags(self, index):
            return super().flags(index) | Qt.ItemFlag.ItemIsEditable


    #true - open in current page; false - open in new page
    md_opened = Signal(str, bool)

    graph_opened = Signal(str)

    #img_opened = Signal(str, bool)

    def __init__(self):
        super().__init__()

        self.file_system = FileTree.FileSystem()
        self.setModel(self.file_system)

        self.copied_path = ""

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)
        self.setExpandsOnDoubleClick(True)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def update_dir(self, path):
        path = path.replace('\n', '')
        self.file_system.setRootPath(path)
        self.setRootIndex(self.file_system.index(path))

    def mousePressEvent(self, event):
        #self.md_opened.emit(self.file_system.filePath(self.indexAt(event.pos())), True)
        super().mousePressEvent(event)

        if not self.file_system.isDir(self.indexAt(event.pos())) and event.button() == Qt.MouseButton.LeftButton:
            self.md_opened.emit(self.file_system.filePath(self.indexAt(event.pos())), True)

    def show_context_menu(self, position):
        """Показывает контекстное меню при клике ПКМ на файл"""
        index = self.indexAt(position)


        if not index.isValid():
            menu = ContextMenu(self.file_system.rootPath(), self, None, None)
            menu.exec(self.viewport().mapToGlobal(position))

        file_path = self.file_system.filePath(index)

        menu = ContextMenu(file_path, self, not self.file_system.isDir(index), index)
        menu.exec(self.viewport().mapToGlobal(position))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())

        for url in event.mimeData().urls():
            src = url.toLocalFile()
            dst = self.file_system.filePath(index)

            try:
                shutil.move(src, dst)
            except shutil.Error as e:
                pass

        event.acceptProposedAction()