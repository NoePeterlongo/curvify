
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import Qt as Qt
from qtrangeslider import QRangeSlider

import sys
import os
import numpy as np

from pathlib import Path

from data_holder import DataHolder
from plot_widget import PlotWidget
from solver import Solver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.solver = Solver()
        self.data_holder = DataHolder(self.solver)

        # QT
        self.setWindowTitle("Curve Fitter")
        self.setGeometry(100, 100, 900, 600)

        self.plot_widget = PlotWidget(self, self.data_holder)
        self.plot_widget.setMinimumSize(400, 400)
        self.range_selection_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.range_selection_slider.setValue((0, 100))
        self.range_selection_slider.valueChanged.connect(
            self.data_holder.set_selected_range)
        self.range_selection_slider.valueChanged.connect(
            self.update_plot)

        self.function_text_edit = QTextEdit()
        self.function_text_edit.setPlaceholderText("Enter your function here")
        self.function_text_edit.setText("a * x + np.sin(b + x) + c")
        self.function_text_edit.textChanged.connect(self.update_function_text)

        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        main_widget = QWidget()
        right_panel = QWidget()
        left_panel = QWidget()

        main_widget.setLayout(main_layout)
        right_panel.setLayout(right_layout)
        left_panel.setLayout(left_layout)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        left_panel.setFixedWidth(300)

        left_layout.addWidget(self.function_text_edit)

        right_layout.addWidget(self.plot_widget)
        right_layout.addWidget(self.range_selection_slider)

        # Drop event
        right_panel.setAcceptDrops(True)
        right_panel.dragEnterEvent = self.drag_enter_event
        right_panel.dropEvent = self.drop_event

        self.setCentralWidget(main_widget)

    def drag_enter_event(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            n_files = len(event.mimeData().urls())
            if n_files == 1:
                event.accept()
                return
        event.ignore()

    def drop_event(self, event: QtGui.QDropEvent):
        mime = event.mimeData()
        if mime.hasUrls():
            for url in mime.urls():
                path = Path(url.toLocalFile())
                if path.suffix == '.csv':
                    data = np.loadtxt(path, delimiter=',', skiprows=1)
                    x = data[:, 0]
                    y = data[:, 1]
                    self.data_holder.set_data(x, y)
                    title = path.name
                    self.update_plot()

    def update_function_text(self):
        text = self.function_text_edit.toPlainText()
        self.solver.update_model(text)
        self.update_plot()

    def update_plot(self):
        self.data_holder.update_curve()
        self.plot_widget.update_plot()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
