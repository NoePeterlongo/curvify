from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

os.environ['QT_API'] = 'pyside6'
matplotlib.use('QtAgg')


class PlotWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @Slot()
    def update_data(self, x: np.ndarray, y: np.ndarray, title: str):
        # Clear the current plot
        x_label = self.ax.get_xlabel()
        self.ax.clear()
        # Plot new data
        self.ax.plot(x, y, '.')
        self.ax.set_xlabel(x_label)
        self.ax.set_title(title)
        # Redraw the canvas
        self.canvas.draw()
