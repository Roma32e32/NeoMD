from PySide6.QtWidgets import QLabel

__all__ = ["MDEditor"]

class MDEditor(QLabel):
    def __del__(self):
        #print("__del__")
        pass