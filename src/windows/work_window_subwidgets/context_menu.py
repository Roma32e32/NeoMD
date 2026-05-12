from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QWidget, QMenu
from PySide6.QtGui import QAction
from os import mkdir, path, rename, remove
from shutil import copytree, copy2, rmtree
from pathlib import Path

__all__ = ['ContextMenu']


class ContextMenu(QMenu):
    def __init__(self, file_path, parent, is_file=None, index=None):
        super().__init__(parent)
        self.file_path = file_path
        self.index = index
        self.parent = parent

        self.is_file = is_file

        open_graph_action= QAction("Граф", self)
        self.addAction(open_graph_action)
        open_graph_action.triggered.connect(self.on_graph_open)
        self.addSeparator()

        if self.is_file:
            open_action = QAction("Открыть", self)
            open_new_action = QAction("Открыть в новой вкладке", self)


            self.addAction(open_action)
            self.addAction(open_new_action)


            open_action.triggered.connect(self.on_open)
            open_new_action.triggered.connect(self.on_new_open)

        else:
            new_file_action = QAction("Новый файл", self)
            self.addAction(new_file_action)
            new_file_action.triggered.connect(self.on_new_file)

            new_dir_action = QAction("Новая папка", self)
            self.addAction(new_dir_action)
            new_dir_action.triggered.connect(self.on_new_dir)

        self.addSeparator()

        paste_action = QAction("Вставить", self)
        paste_action.triggered.connect(self.on_paste)
        self.addAction(paste_action)

        if is_file is not None:
            copy_action = QAction("Копировать", self)

            delete_action = QAction("Удалить", self)
            rename_action = QAction("Переименовать", self)


            copy_action.triggered.connect(self.on_copy)

            delete_action.triggered.connect(self.on_delete)
            rename_action.triggered.connect(self.on_rename)


            self.addAction(copy_action)
            self.addSeparator()
            self.addAction(delete_action)
            self.addAction(rename_action)

    def on_new_file(self, n=False):
        path = f"{self.file_path}//Новый файл{'' if n is False else f' ({n})'}"
        try:
            open(path, 'x').close()
        except FileExistsError:
            self.on_new_file(1 if n is False else n + 1)
        else:
            self.parent.edit(self.parent.file_system.index(path))

    def on_new_dir(self, n=False):
        path = f'{self.file_path}//Новая папка{'' if n is False else f' ({n})'}'
        try:
            mkdir(path)
        except FileExistsError:
            self.on_new_dir(1 if n is False else n+1)
        else:
            self.parent.edit(self.parent.file_system.index(path))

    def on_open(self):
        self.parent.md_opened.emit(self.file_path, True)

    def on_new_open(self):
        self.parent.md_opened.emit(self.file_path, False)

    def on_graph_open(self):
        self.parent.graph_opened.emit(Path(self.file_path))

    def on_copy(self):
        self.parent.copied_path = self.file_path

    def on_paste(self):
        is_src_file = not self.parent.file_system.isDir(self.parent.file_system.index(self.parent.copied_path))

        try:
            if is_src_file:
                copy2(self.parent.copied_path, self.file_path)
            else:
                copytree(self.parent.copied_path, path.join(self.file_path, os.path.basename(self.parent.copied_path)), dirs_exist_ok=True)
        except BaseException:
            pass

    def on_delete(self):
        if self.is_file:
            remove(self.file_path)
        else:
            rmtree(self.file_path)

    def on_rename(self):
        self.parent.edit(self.index)