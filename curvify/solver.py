from scipy.optimize import curve_fit
import numpy as np
import re
import copy
from dataclasses import dataclass

from .models_library import fourier


@dataclass
class Param:
    name: str
    value: float = 1.0
    locked: bool = False
    min_value: float = -float('inf')
    max_value: float = float('inf')
    error: float | None = None

class Solver:
    def __init__(self):
        self.is_valid_ = False
        self.report: str = ""

    def update_model(self, function_str: str):
        # TODO checks : nb of params, execution ?
        # Find params
        param_names: list[str] = re.findall(r'\b([a-wyz]\d*)\b', function_str)
        param_names = list(dict.fromkeys(param_names)) # Makes the params unique

        function_str = "lambda x, " + \
            ", ".join(param_names) + ": " + function_str
        
        try:
            model = eval(function_str)
        except:
            self.is_valid_ = False
            return
        self.model = model
        self.model_str = function_str
        self.is_valid_ = True

        #TODO keep existing parameters ?
        self.params = [Param(name, 1.0) for name in param_names]

    def is_valid(self) -> bool:
        return self.is_valid_

    def get_params(self) -> list[Param]:
        return self.params

    def get_params_dict(self):
        return {
            param.name: param.value for param in self.params
        }

    def evaluate(self, x: float) -> float:
        params_dict = self.get_params_dict()
        # return self.model(x, **params_dict)
        vectorized_model = np.vectorize(lambda xi: self.model(xi, **params_dict))
        return vectorized_model(x)

    def fit(self, x_data: np.ndarray, y_data: np.ndarray) -> tuple[bool, dict]:
        p0 = [param.value for param in self.params]
        upper_bounds = [p.value+1e-15 if p.locked else p.max_value for p in self.params]
        lower_bounds = [p.value if p.locked else p.min_value for p in self.params]
        try:
            params, covariance = curve_fit(self.model, x_data, y_data, p0=p0, bounds=(lower_bounds, upper_bounds))
            error = np.sqrt(np.diag(covariance))
        except (RuntimeError, TypeError) as e:
            print(f"Error during fitting: {e}")
            return False, {}
        
        # Store initial params for report
        initial_params = copy.deepcopy(self.params)

        for i, param in enumerate(self.params):
            param.value = float(params[i])
            param.error = float(error[i])

        results = {}
        results["params"] = self.get_params_dict()
        results["params_error"] = error
        y_pred = self.evaluate(x_data)  
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        results["R2"] = r_squared
        rmse = np.sqrt(np.mean((y_data - y_pred) ** 2))
        results["RMSE"] = rmse

        self.build_report(x_data, y_data, self.model_str, initial_params, results)
        
        return True, results
    
    def build_report(
            self, 
            x_data: np.ndarray, 
            y_data: np.ndarray, 
            model_str: str, 
            initial_params: list[Param], 
            results: dict
        ):

        filled_model = model_str.split(":")[1].strip()
        for name, value in results["params"].items():
            filled_model = re.sub(fr"\b({name})\b", f"{value:.5e}", filled_model)

        self.report = ""
        self.report += "Data :\n"
        self.report += f"\tx_data = [{', '.join(map(lambda x: f"{x:.4e}", x_data))}]\n"
        self.report += f"\ty_data = [{', '.join(map(lambda x: f"{x:.4e}", y_data))}]\n"
        self.report += "\n"
        self.report += "Model :\n"
        self.report += f"\ty = {model_str.split(':')[1]}\n"
        init_values = {p.name: p.value for p in initial_params}
        self.report += f"\tinitial_parameters = {init_values}\n"
        self.report += f"\t locked_parameters = [{', '.join([p.name for p in initial_params if p.locked])}]\n"
        self.report += "\n"
        self.report += "Results :\n"
        self.report += f"\tmodel: y = {filled_model}\n"
        for key, value in results.items():
            self.report += f"\t{key} = {value}\n"


if __name__ == "__main__":
    solver = Solver()
    solver.update_model("a * x + np.sin(b + x) + c")
    print(solver.evaluate(1))

    x_data = np.linspace(0, 10, 100)
    f = lambda x: 2*x + np.sin(1 + x) + 5 + np.random.rand()
    y_data = f(x_data)

    solver.fit(x_data, y_data)
    print(solver.get_params_dict())
    y_hat_data = solver.evaluate(x_data)
    print(y_hat_data - y_data)
