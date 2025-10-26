import sys
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout,
    QLabel, QComboBox, QPushButton
)
from PySide6.QtCore import Signal


class CSVDialog(QDialog):
    data_selected = Signal(np.ndarray, np.ndarray)  # Signal to return x and y

    def __init__(self, csv_path, parent=None):
        super().__init__(parent)
        self.csv_path = csv_path
        self.setWindowTitle("CSV import")
        self.setup_ui()
        self.load_csv()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Chemin du fichier
        self.path_label = QLabel(f"File: {self.csv_path}")
        layout.addWidget(self.path_label)

        # Sélection du délimiteur
        self.delimiter_combo = QComboBox()
        self.delimiter_combo.addItems([",", ";", "\t", "|"])
        self.delimiter_combo.currentTextChanged.connect(self.load_csv)
        layout.addWidget(QLabel("Delimiter:"))
        layout.addWidget(self.delimiter_combo)

        # Sélection des colonnes X et Y
        self.x_col_combo = QComboBox()
        self.y_col_combo = QComboBox()
        layout.addWidget(QLabel("X column:"))
        layout.addWidget(self.x_col_combo)
        layout.addWidget(QLabel("Y column:"))
        layout.addWidget(self.y_col_combo)

        # Bouton de validation
        self.ok_button = QPushButton("Import data")
        self.ok_button.clicked.connect(self.on_ok)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
        self.adjustSize()

    def load_csv(self):
        delimiter = self.delimiter_combo.currentText()
        try:
            df = pd.read_csv(self.csv_path, delimiter=delimiter)
            self.df = df
            self.x_col_combo.clear()
            self.y_col_combo.clear()
            self.x_col_combo.addItems(df.columns)
            self.y_col_combo.addItems(df.columns)
            self.x_col_combo.setCurrentIndex(0)
            self.y_col_combo.setCurrentIndex(1)
        except Exception as e:
            print(f"Failed to load CSV: {e}")

    def on_ok(self):
        x_col = self.x_col_combo.currentText()
        y_col = self.y_col_combo.currentText()
        try:
            x_ok = pd.api.types.is_numeric_dtype(self.df[x_col])
            y_ok = pd.api.types.is_numeric_dtype(self.df[y_col])
            if not x_ok or not y_ok:
                print("X and Y columns must be numeric")
                self.reject()
                return
            X = self.df[x_col].to_numpy()
            Y = self.df[y_col].to_numpy()
        except Exception as e:
            print(f"Failed to load data")
            self.reject()
            return
        self.data_selected.emit(X, Y)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    csv_path = "random_data.csv"

    dialog = CSVDialog(csv_path)
    dialog.data_selected.connect(lambda x, y: print("X:", x, "\nY:", y))
    dialog.exec()
