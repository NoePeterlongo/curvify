import argparse
from .gui import curvify

def main():
    parser = argparse.ArgumentParser(description="Launches Curvify interface.")
    parser.add_argument("csv", type=str, help="Path to the CSV file")
    args = parser.parse_args()
    if args.csv:
        curvify(csv_file=args.csv)
    else:
        curvify()

if __name__ == "__main__":
    main()