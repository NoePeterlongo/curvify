
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QCheckBox, QComboBox
from PySide6.QtCore import Qt, QTimer
from qtrangeslider import QRangeSlider

import sys
import os
from pathlib import Path
from functools import partial
import numpy as np

from .csv_dialog import CSVDialog
from .data_holder import DataHolder
from .plot_widget import PlotWidget
from .solver import Param, Solver
from .models_library import models_library, find_model

import importlib.resources


def get_icon():
    with importlib.resources.path("curvify.icons", "app_icon.png") as icon_path:
        return QtGui.QIcon(str(icon_path))


class MainWindow(QMainWindow):
    def __init__(self,
                 x_array: np.ndarray | None,
                 y_array: np.ndarray | None,
                 default_function: str | None,
                 csv_file: str | None):
        super().__init__()

        self.solver = Solver()
        self.data_holder = DataHolder(self.solver)

        # QT
        self.setWindowTitle("Curvify")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(get_icon())

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
        self.function_text_edit.textChanged.connect(self.update_function_text)
        self.model_combo = QComboBox()
        self.model_combo.addItems(models_library.keys())
        self.model_combo.currentTextChanged.connect(
            lambda text: self.function_text_edit.setText(
                models_library[text]) if text != '' else None
        )

        self.fit_button = QPushButton("Fit")
        self.fit_button.clicked.connect(self.fit)
        self.fit_button.setEnabled(False)

        self.parameters_grid_layout = QGridLayout()
        self.parameters_grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        parameters_grid = QWidget()
        parameters_grid.setLayout(self.parameters_grid_layout)

        main_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        main_widget = QWidget()
        h_widget = QWidget()
        right_panel = QWidget()
        left_panel = QWidget()

        main_widget.setLayout(main_layout)
        h_widget.setLayout(h_layout)
        right_panel.setLayout(right_layout)
        left_panel.setLayout(left_layout)

        main_layout.addWidget(self.function_text_edit)
        main_layout.addWidget(h_widget)

        h_layout.addWidget(left_panel)
        h_layout.addWidget(right_panel)

        left_panel.setFixedWidth(300)

        left_layout.addWidget(self.model_combo)
        left_layout.addWidget(parameters_grid)
        left_layout.addWidget(self.fit_button)

        right_layout.addWidget(self.plot_widget)
        right_layout.addWidget(self.range_selection_slider)

        # Drop event
        right_panel.setAcceptDrops(True)
        right_panel.dragEnterEvent = self.drag_enter_event
        right_panel.dropEvent = self.drop_event

        self.setCentralWidget(main_widget)

        self.model_combo.setCurrentIndex(0)
        self.function_text_edit.setText(models_library["Linear"])
        self.solver.update_model(models_library["Linear"])
        self.build_parameters_grid()

        # Initialize with data
        if x_array is not None and y_array is not None:
            self.set_data(x_array, y_array)
        if default_function is not None:
            self.function_text_edit.setText(default_function)
        if csv_file is not None:
            self.load_csv(csv_file)

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
                    self.load_csv(path)

    def load_csv(self, path: str | Path):
        csv_dialog = CSVDialog(path, self)
        csv_dialog.data_selected.connect(self.set_data)
        csv_dialog.exec()

    def set_data(self, x: np.ndarray, y: np.ndarray):
        self.data_holder.set_data(x, y)
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

        # Update combo box selection if the function is known
        model_index = find_model(text)
        self.model_combo.setCurrentIndex(model_index)

    def update_plot(self):
        self.data_holder.update_curve()  # Data_holder holds the solver
        self.plot_widget.update_plot()

    def fit(self):
        ok = self.solver.fit(*self.data_holder.get_selected_data())
        if ok:
            self.update_plot()
            self.build_parameters_grid()
        else:
            self.fit_button.setText("Fit failed")
            self.fit_button.setStyleSheet("background-color: red;color: black")
            # reset text after 2 seconds
            QTimer.singleShot(1000, lambda: (
                self.fit_button.setText("Fit"),
                self.fit_button.setStyleSheet("")
            ))

    def build_parameters_grid(self):
        # Clear layout
        while self.parameters_grid_layout.count():
            item = self.parameters_grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.parameters_grid_layout.addWidget(QLabel("Param"), 0, 0)
        self.parameters_grid_layout.addWidget(QLabel("Value"), 0, 1)
        self.parameters_grid_layout.addWidget(QLabel("Locked"), 0, 2)

        parameters = self.solver.get_params()
        for i, param in enumerate(parameters):
            self.parameters_grid_layout.addWidget(QLabel(param.name), i+1, 0)
            value = param.value if abs(param.value) > 1e-13 else 0.0
            value_edit = QLineEdit(f"{value:.5g}")
            value_edit.setValidator(QtGui.QDoubleValidator())
            value_edit.textChanged.connect(
                partial(self.param_value_edited, param)
            )
            self.parameters_grid_layout.addWidget(value_edit, i+1, 1)

            lock_checkbox = QCheckBox()
            lock_checkbox.setChecked(param.locked)
            lock_checkbox.stateChanged.connect(
                partial(self.param_locked_changed, param)
            )
            self.parameters_grid_layout.addWidget(lock_checkbox, i+1, 2)

    def param_value_edited(self, param: Param, value: str):
        try:
            val = float(value)
            param.value = val
            self.update_plot()
        except:
            pass

    def param_locked_changed(self, param: Param, state: int):
        param.locked = state == Qt.Checked.value


def curvify(
        x_array: np.ndarray | None = None,
        y_array: np.ndarray | None = None,
        default_function: str | None = None,
        csv_file: str | None = None):
    app = QApplication(sys.argv)
    window = MainWindow(x_array, y_array, default_function, csv_file)
    window.show()
    return app.exec()
