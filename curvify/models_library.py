import numpy as np

models_library: dict[str, str] = {
    # Polynomial models
    "Linear": "a * x + b",  # Simple linear model
    "Quadratic": "a * x**2 + b * x + c",  # Second-degree polynomial
    "Cubic": "a * x**3 + b * x**2 + c * x + d",  # Third-degree polynomial
    "Polynomial": "np.polyval([a, b, c, d, e], x)",  # General polynomial of degree 4

    # Exponential and logarithmic models
    "Exponential": "a * np.exp(b * x) + c",  # Exponential growth/decay
    "Exponential with offset": "a * np.exp(b * (x - c)) + d",  # With horizontal and vertical shift
    "Logarithmic": "a * np.log(b * x + c) + d",  # Logarithmic model with shift
    "Power Law": "a * x**b + c",  # Power law (logarithmic scale)

    # Trigonometric models
    "Sine": "a * np.sin(b * x + c) + d",  # Sine wave with amplitude, frequency, phase, and offset
    "Damped Sine": "a * np.exp(-c * x) * np.sin(b * x + d) + e",  # Exponentially damped sine wave

    # Rational models
    "Hyperbola": "a / (x + b) + c",  # Simple hyperbola
    "Rational": "(a * x + b) / (c * x + d)",  # Linear/linear rational function

    # Sigmoid models (S-shaped curves)
    "Logistic": "a / (1 + np.exp(-b * (x - c))) + d",  # Logistic curve (logistic regression)
    "Gompertz": "a * np.exp(-b * np.exp(-c * x)) + d",  # Gompertz model (asymmetric sigmoid growth)

    # Custom/advanced models
    "Gaussian": "a * np.exp(-((x - b)**2) / (2 * c**2)) + d",  # Bell curve (Gaussian)
    "Lorentzian": "a / (1 + ((x - b) / c)**2) + d",  # Lorentz curve (symmetric peak)
    "Weibull": "a * np.exp(-((x - b) / c)**d)",  # Weibull model (reliability, survival analysis)

    # Advanced periodic models
    "Fourier Series (n=2)": (
        "a0 + "
        "a1 * np.cos(f0 * x) + b1 * np.sin(f0 * x) + "
        "a2 * np.cos(2 * f0 * x) + b2 * np.sin(2 * f0 * x)"
    ),
    "Fourier (general)": "fourier(x, f0, [a0, a1, b1, a2, b2, a3, b3, a4, b4, a5, b5])"
}

# This function tries to recognize a known model. 
# If it does, it returns the index of the model in the list.
# If not, returns -1
def find_model(model: str) -> int:
    for i, (_, known_model) in enumerate(models_library.items()):
        if known_model.replace(" ", "") == model.replace(" ", ""):
            return i
    return -1

def fourier(x, f0, coefs: list[float]):
    n = len(coefs) // 2
    w0 = 2 * np.pi * f0
    result = coefs[0]
    for i in range(1, n + 1):
        result += coefs[2 * i - 1] * np.cos(i * w0 * x) + coefs[2 * i] * np.sin(i * w0 * x)
    return result