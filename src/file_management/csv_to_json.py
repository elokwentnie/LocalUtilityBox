import pandas as pd
import sys
import argparse
from pathlib import Path


def csv_to_json(input_file: Path, output_file: Path = None) -> None:
    # Determine the output file path
    if output_file is None or output_file.suffix.lower() != ".json":
        output_file = input_file.with_suffix(".json")
    try:
        # Read the CSV file, allowing pandas to infer the separator
        df = pd.read_csv(input_file, sep=None, engine="python")
        # Strip whitespace from column names
        df.rename(columns=lambda x: x.strip(), inplace=True)
        # Write to JSON
        df.to_json(output_file, indent=4, orient="records")
        print(f"Conversion successful: {output_file}")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file {input_file}: {e}")
        raise
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file to a JSON file.")
    parser.add_argument("input_file", type=Path, help="Path to the input .csv file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output .json file",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".csv":
        print(f"Error: {input_file} does not exist or is not a CSV file.")
        sys.exit(1)

    csv_to_json(input_file, output_file)


if __name__ == "__main__":
    main()
