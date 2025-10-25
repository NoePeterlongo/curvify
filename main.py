
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt as Qt
from qtrangeslider import QRangeSlider

import sys
import os
import numpy as np

from pathlib import Path

from data_holder import DataHolder
from plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data_holder = DataHolder()

        # QT
        self.setWindowTitle("Curve Fitter")
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = PlotWidget(self, self.data_holder)
        self.range_selection_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.range_selection_slider.setValue((0, 100))
        self.range_selection_slider.valueChanged.connect(self.data_holder.set_selected_range)
        self.range_selection_slider.valueChanged.connect(self.plot_widget.update_plot)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.range_selection_slider)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        central_widget.setAcceptDrops(True)
        central_widget.dragEnterEvent = self.drag_enter_event
        central_widget.dropEvent = self.drop_event

        self.setCentralWidget(central_widget)

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
                    self.plot_widget.update_plot()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
