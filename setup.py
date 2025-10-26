from setuptools import setup, find_packages

setup(
    name="curvify",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "curvify": ["icons/*.png"],
    },
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "pyside6",
        "pyside6_addons",
        "pyside6_essentials",
        "QtRangeSlider",
    ],
    entry_points={
        "console_scripts": [
            "curvify=curvify.cli:main",
        ],
    },
)