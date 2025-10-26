import argparse
from .gui import curvify

def main():
    parser = argparse.ArgumentParser(description="Launches Curvify interface.")
    args = parser.parse_args()

    curvify()

if __name__ == "__main__":
    main()