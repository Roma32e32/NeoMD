from PySide6.QtCore import QStringListModel, QObject, Signal,Slot
from PySide6.QtWidgets import *

__all__ = ["InitWindow"]


class InitWindow(QWidget):
    def __init__(self):
        super().__init__()

        recent_list_model = QStringListModel()

        self.presenter = InitMenuPresenter(recent_list_model)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.dir_dialog_button = QPushButton("Open Directory")

        self.recent_list = QListView()
        self.recent_list.setModel(recent_list_model)
        self.recent_list.setEditTriggers(QListView.EditTrigger.NoEditTriggers)


        layout.addWidget(self.dir_dialog_button)
        layout.addWidget(self.recent_list)

        self.dir_dialog_button.clicked.connect(self.presenter.dir_select_dialog)
        self.dir_selected = self.presenter.dir_selected
        self.recent_list.doubleClicked.connect(lambda i: self.dir_selected.emit(self.presenter.recent_list.stringList()[i.row()]))


class InitMenuPresenter(QObject):
    dir_selected = Signal(str)

    def __init__(self, recent_list: QStringListModel):
        super().__init__()

        self.recent_list_file_path = r"userfiles/recent_dirs"

        self.recent_list = recent_list

        try:
            file = open(self.recent_list_file_path, "r")
        except FileNotFoundError:
            file = open(self.recent_list_file_path, "x")
            file.close()
            file = open(self.recent_list_file_path, "r")


        self.recent_list.setStringList(file.readlines())

        file.close()


    @Slot()
    def dir_select_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(
            None,
            "Выберите директорию",
            "/home"
        )

        if dir_path:
            self.dir_selected.emit(dir_path)
            self.recent_list.setStringList(self.recent_list.stringList() + [dir_path])

            file = open(self.recent_list_file_path, "a")
            file.write(dir_path + "\n")
            file.close()