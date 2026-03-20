from PySide6.QtCore import *
from PySide6.QtWidgets import *
from src.init_menu import InitMenu
from work_menu import WorkMenu

__all__ = ["MainWindow"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_menu = InitMenu()
        self.work_menu = WorkMenu()

        self.setWindowTitle("NeoMD")
        self.setGeometry(300, 300, 400, 200)

        stacked_widget = QStackedWidget(self)
        self.setCentralWidget(stacked_widget)

        stacked_widget.addWidget(self.init_menu)
        stacked_widget.addWidget(self.work_menu)

        self.init_menu.dir_selected.connect(lambda a: stacked_widget.setCurrentIndex(1))
        self.init_menu.dir_selected.connect(lambda a: self.work_menu.update_dir(a))
        #self.work_menu.btn.clicked.connect(lambda a: stacked_widget.setCurrentIndex(0))