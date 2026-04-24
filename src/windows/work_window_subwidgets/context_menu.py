from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QWidget, QMenu
from PySide6.QtGui import QAction

__all__ = ['ContextMenu']


class ContextMenu(QMenu):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.parent = parent

        open_action = QAction("Открыть в новой вкладке", self)
        copy_action = QAction("Копировать путь", self)
        delete_action = QAction("Удалить", self)

        self.addAction(open_action)
        self.addSeparator()
        self.addAction(copy_action)
        self.addAction(delete_action)

        open_action.triggered.connect(self.on_open)
        copy_action.triggered.connect(self.on_copy)
        delete_action.triggered.connect(self.on_delete)

    def on_open(self):
        """Обработчик открытия файла"""
        self.parent.md_opened.emit(self.file_path, False)

    def on_copy(self):
        """Обработчик копирования пути"""
        pass

    def on_delete(self):
        """Обработчик удаления файла"""
        pass