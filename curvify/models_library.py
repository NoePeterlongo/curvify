models_library: dict[str, str] = {
    # Polynomial models
    "Linear": "a * x + b",  # Simple linear model
    "Quadratic": "a * x**2 + b * x + c",  # Second-degree polynomial
    "Cubic": "a * x**3 + b * x**2 + c * x + d",  # Third-degree polynomial

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
        "a0 + a1 * np.cos(b * x + c1) + a2 * np.cos(2 * b * x + c2) + "
        "d1 * np.sin(b * x + e1) + d2 * np.sin(2 * b * x + e2)"
    ),  # Fourier series (2 harmonics)
}
