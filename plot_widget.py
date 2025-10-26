from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
import matplotlib
import os

from data_holder import DataHolder

os.environ['QT_API'] = 'pyside6'
matplotlib.use('QtAgg')


class PlotWidget(QWidget):
    def __init__(self, parent, data_holder: DataHolder):
        super().__init__(parent)
        self.data_holder = data_holder

        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @Slot()
    def update_plot(self):
        # Clear the current plot
        self.ax.clear()
        # Plot new data
        self.ax.plot(*self.data_holder.get_selected_data(), '.')
        self.ax.plot(*self.data_holder.get_not_selected_data(), '+', color='lightgray')
        self.ax.plot(*self.data_holder.get_curve_data(), '--', color='red')
        # self.ax.set_title(title)
        # Redraw the canvas
        self.canvas.draw()
