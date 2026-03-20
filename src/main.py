import sys
from PySide6.QtWidgets import *
from main_window import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())