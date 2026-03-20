from PySide6.QtCore import QStringListModel, QObject, Signal,Slot
from PySide6.QtWidgets import *

__all__ = ["InitMenuView"]


class InitMenuView(QWidget):
    def __init__(self, recent_list_model: QStringListModel):
        super().__init__()

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


class InitMenuPresenter(QObject):
    dir_selected = Signal(str)

    def __init__(self, recent_list_model: QStringListModel):
        super().__init__()

        self.recent_list = []
        self.recent_list_model = recent_list_model

    @Slot()
    def dir_select_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(
            None,
            "Выберите директорию",
            "/home"
        )

        if dir_path:
            self.dir_selected.emit(dir_path)
            self.recent_list.append(dir_path)
            self.recent_list_model.setStringList(self.recent_list)


class InitMenuModel(QObject):
    def __init__(self):
        super().__init__()