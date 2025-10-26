from scipy.optimize import curve_fit
import numpy as np
import re
from dataclasses import dataclass


@dataclass
class Param:
    name: str
    value: float = 1.0
    locked: bool = False

class Solver:
    def __init__(self):
        self.is_valid_ = False

    def update_model(self, function_str: str):
        # TODO checks : nb of params, execution ?
        # Find params
        param_names: list[str] = re.findall(r'\b([a-wyz])\b', function_str)

        function_str = "lambda x, " + \
            ", ".join(param_names) + ": " + function_str
        
        try:
            model = eval(function_str)
        except:
            self.is_valid_ = False
            return
        self.model = model
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

    def fit(self, x_data: np.ndarray, y_data: np.ndarray) -> dict:
        # TODO: check the nb of points vs the number of parmaeters
        p0 = [param.value for param in self.params]
        params, covariance = curve_fit(self.model, x_data, y_data, p0=p0)
        for i, param in enumerate(self.params):
            param.value = float(params[i])


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
