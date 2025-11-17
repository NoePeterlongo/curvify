from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtGui import QTextOption

class TextDialog(QDialog):
    def __init__(self, parent, title:str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)

        # Create a QTextEdit widget for multi-line, selectable text
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text
        )
        self.text_edit.setReadOnly(True)  # Make it read-only if you only want selection
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)  # Disable word wrap

        # Create a layout and add the text edit
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        # Optional: Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)