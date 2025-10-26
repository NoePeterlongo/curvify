
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QWidget, QPushButton, QLineEdit, QGridLayout, QLabel
from PySide6.QtCore import Qt as Qt
from qtrangeslider import QRangeSlider

import sys
import os
import numpy as np

from pathlib import Path

from data_holder import DataHolder
from plot_widget import PlotWidget
from solver import Param, Solver


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

        self.function_text_edit = QLineEdit()
        self.function_text_edit.setPlaceholderText("Enter your function here")
        self.function_text_edit.setText("a * x**2 + b*x + c")
        self.solver.update_model("a * x**2 + b*x + c")
        self.function_text_edit.textChanged.connect(self.update_function_text)

        self.fit_button = QPushButton("Fit")
        self.fit_button.clicked.connect(self.fit)
        self.fit_button.setEnabled(False)

        self.parameters_grid_layout = QGridLayout()
        self.parameters_grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        parameters_grid = QWidget()
        parameters_grid.setLayout(self.parameters_grid_layout)
        self.build_parameters_grid()

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
        left_layout.addWidget(parameters_grid)
        left_layout.addWidget(self.fit_button)

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
                    self.check_ready_to_fit()

    def check_ready_to_fit(self):
        self.fit_button.setEnabled(
            self.solver.is_valid() and len(self.data_holder) > 2)

    def update_function_text(self):
        text = self.function_text_edit.text()
        self.solver.update_model(text)
        self.update_plot()
        self.check_ready_to_fit()
        self.build_parameters_grid()

    def update_plot(self):
        self.data_holder.update_curve()  # Data_holder holds the solver
        self.plot_widget.update_plot()

    def fit(self):
        self.solver.fit(*self.data_holder.get_selected_data())
        self.update_plot()
        self.build_parameters_grid()

    def build_parameters_grid(self):
        # Clear layout
        while self.parameters_grid_layout.count():
            item = self.parameters_grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.parameters_grid_layout.addWidget(QLabel("Param"), 0, 0)
        self.parameters_grid_layout.addWidget(QLabel("Value"), 0, 1)

        parameters = self.solver.get_params()
        for i, param in enumerate(parameters):
            self.parameters_grid_layout.addWidget(QLabel(param.name), i+1, 0)
            value_edit = QLineEdit(f"{param.value:.3g}")
            value_edit.setValidator(QtGui.QDoubleValidator())
            value_edit.textChanged.connect(
                lambda value: self.param_value_edited(param, value)
            )
            self.parameters_grid_layout.addWidget(value_edit, i+1, 1)

    def param_value_edited(self, param: Param, value: str):
        try:
            val = float(value)
            param.value = val
            self.update_plot()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
