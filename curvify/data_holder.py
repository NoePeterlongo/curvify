import numpy as np

from .solver import Solver


class DataHolder():
    def __init__(self, solver: Solver):
        self.solver = solver
        self.x = np.zeros((0))
        self.y = np.zeros((0))
        self.selected_mask = np.zeros((0), dtype=bool)  # Store a boolean mask
        self.selected_percent_min = 0
        self.selected_percent_max = 100
        self.update_selected_mask_()

        self.curve_x = np.zeros((0))
        self.curve_y = np.zeros((0))

    def set_data(self, x: np.ndarray, y: np.ndarray):
        if len(x) == 0:
            print(f"Ignoring empty data")
            return
        self.x = x.copy()
        self.y = y.copy()
        self.update_selected_mask_()

    def set_selected_range(self, min_max: tuple[int, int]):
        self.selected_percent_min = min_max[0]
        self.selected_percent_max = min_max[1]
        self.update_selected_mask_()

    def update_selected_mask_(self):
        if len(self.x) == 0:
            return
        # Create a boolean mask
        min_val, max_val = self.x.min(), self.x.max()
        lower_bound = min_val + self.selected_percent_min / \
            99 * (max_val - min_val)
        upper_bound = min_val + self.selected_percent_max / \
            99 * (max_val - min_val)
        self.selected_mask = (self.x >= lower_bound) & (self.x <= upper_bound)

    def update_curve(self):
        if len(self.x) < 2 or not self.solver.is_valid():
            return
        min_selected_x = self.x[self.selected_mask].min()
        max_selected_x = self.x[self.selected_mask].max()
        x_array = np.linspace(min_selected_x, max_selected_x, 50)
        self.curve_x = x_array
        self.curve_y = self.solver.evaluate(x_array)

    def get_selected_data(self) -> tuple[np.ndarray, np.ndarray]:
        return self.x[self.selected_mask].copy(), self.y[self.selected_mask].copy()

    def get_not_selected_data(self) -> tuple[np.ndarray, np.ndarray]:
        if len(self.x) == 0:
            return np.array([]), np.array([])
        return self.x[~self.selected_mask].copy(), self.y[~self.selected_mask].copy()
    
    def get_curve_data(self) -> tuple[np.ndarray, np.ndarray]:
        return self.curve_x.copy(), self.curve_y.copy()

    def __len__(self):
        return len(self.x)
    
    def x_range(self) -> tuple[float, float]:
        if len(self.x) == 0:
            return (0, 0)
        return (self.x.min(), self.x.max())
