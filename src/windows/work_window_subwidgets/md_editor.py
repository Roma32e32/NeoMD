from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QTextBrowser, QTextEdit, QHBoxLayout, QPushButton
from markdown_it import MarkdownIt, presets

md = MarkdownIt()
md.enable('table')
md.options["breaks"] = True

__all__ = ["MDEditor"]

class MDEditor(QWidget):
    def __init__(self, path):
        super().__init__()

        self.path = path

        self.stack = QStackedWidget()
        self.layout = QVBoxLayout()
        self.top_panel = QHBoxLayout()
        self.layout.addLayout(self.top_panel)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        self.text_browser = QTextBrowser()
        self.on_viewer_selected()
        self.stack.addWidget(self.text_browser)

        self.text_edit = QTextEdit()
        self.text_edit.setText(self.text)
        self.stack.addWidget(self.text_edit)

        self.editor_mode_btn = QPushButton("Код")
        self.viewer_mode_btn = QPushButton("Markdown")
        #self.save_btn = QPushButton("Сохранить")
        self.top_panel.addWidget(self.editor_mode_btn)
        self.top_panel.addWidget(self.viewer_mode_btn)
        #self.top_panel.addWidget(self.save_btn)

        self.editor_mode_btn.clicked.connect(self.on_editor_selected)
        self.viewer_mode_btn.clicked.connect(self.on_viewer_selected)

        self.text_edit.textChanged.connect(self.on_text_changed)

    @property
    def text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    @text.setter
    def text(self, text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def on_text_changed(self):
        self.text = self.text_edit.toPlainText()

    def on_editor_selected(self):
        self.stack.setCurrentIndex(1)

    def on_viewer_selected(self):
        self.stack.setCurrentIndex(0)
        html = md.render(self.text)
        self.text_browser.setHtml(html)

    def __del__(self):
        pass