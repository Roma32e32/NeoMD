import sys

import qdarkstyle
from qdarkstyle import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from windows.main_window import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
