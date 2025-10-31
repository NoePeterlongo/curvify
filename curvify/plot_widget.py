from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.axes import Axes  # For typing
from matplotlib.figure import Figure  # For typing
import os
import numpy as np
from .data_holder import DataHolder

os.environ['QT_API'] = 'pyside6'
matplotlib.use('QtAgg')


class PlotWidget(QWidget):
    def __init__(self, parent, data_holder: DataHolder):
        super().__init__(parent)
        self.data_holder = data_holder
        # Create a Matplotlib figure with two subplots
        self.figure: Figure
        self.ax: Axes
        self.ax_res: Axes
        self.figure, (self.ax, self.ax_res) = plt.subplots(
            2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [3, 1]})
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @Slot()
    def update_plot(self):
        # Clear both axes
        self.ax.clear()
        self.ax_res.clear()

        # Plot main data
        self.ax.plot(*self.data_holder.get_selected_data(), '.', label="Data points")
        self.ax.plot(*self.data_holder.get_not_selected_data(),
                     '+', color='lightgray')
        self.ax.plot(*self.data_holder.get_curve_data(),
                     '--', color='red', label="Model")
        self.ax.set_ylabel('Y')
        self.ax.legend()
        self.ax.grid(True)

        # Plot residuals
        x_residuals, y_residuals = self.data_holder.get_residuals()
        if len(x_residuals) > 0:
            self.ax_res.axhline(y=0, color='black',
                                linestyle='--', linewidth=0.7)
            stemline = self.ax_res.stem(
                x_residuals, y_residuals,
                linefmt='black',
                markerfmt='ko',
                basefmt='black',
            )
            stemline.markerline.set_markersize(3)
            self.ax_res.set_xlabel('X')
            self.ax_res.set_ylabel('Residual')
            self.ax_res.set_xlim(self.ax.get_xlim())
            self.ax_res.grid(True)
            # self.ax_res.legend()

        # Redraw the canvas
        self.canvas.draw()
