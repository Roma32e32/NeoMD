from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QTreeView, QFileSystemModel
from work_window_subwidgets.context_menu import ContextMenu

__all__ = ["FileTree"]

class FileTree(QTreeView):
    md_opened = Signal(str, bool)
    graph_opened = Signal(str, bool)
    img_opened = Signal(str, bool
                        )

    def __init__(self):
        super().__init__()

        self.file_system = QFileSystemModel()
        self.setModel(self.file_system)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)
        self.setExpandsOnDoubleClick(True)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def update_dir(self, path):
        path = path.replace('\n', '')
        self.file_system.setRootPath(path)
        self.setRootIndex(self.file_system.index(path))

    def mouseDoubleClickEvent(self, event):
        #self.md_opened.emit(self.file_system.filePath(self.indexAt(event.pos())), True)
        super().mouseDoubleClickEvent(event)

        if not self.file_system.isDir(self.indexAt(event.pos())) and event.button() == Qt.MouseButton.LeftButton:
            self.md_opened.emit(self.file_system.filePath(self.indexAt(event.pos())), True)

    def show_context_menu(self, position):
        """Показывает контекстное меню при клике ПКМ на файл"""
        index = self.indexAt(position)

        # Проверяем, что клик был по существующему элементу и это файл (не папка)
        if not index.isValid() or self.file_system.isDir(index):
            return

        file_path = self.file_system.filePath(index)

        # Создаем и показываем контекстное меню
        menu = ContextMenu(file_path, self)
        menu.exec(self.viewport().mapToGlobal(position))