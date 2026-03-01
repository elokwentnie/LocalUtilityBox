import pandas as pd
import sys
import argparse
from pathlib import Path


def csv_to_excel(input_file: Path, output_file: Path = None) -> None:
    # Determine the output file path
    if output_file is None or output_file.suffix.lower() != ".xlsx":
        output_file = input_file.with_suffix(".xlsx")

    try:
        # Read the CSV file, allowing pandas to infer the separator
        df = pd.read_csv(input_file, sep=None, engine="python")
        # Write to Excel without the index column
        df.to_excel(output_file, index=False)
        print(f"Conversion successful: {output_file}")
    except Exception as e:
        print(f"Error converting {input_file} to Excel: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to an XLSX (Excel) file."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input .csv file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output .xlsx file",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".csv":
        print(f"Error: {input_file} does not exist or is not a CSV file.")
        sys.exit(1)

    csv_to_excel(input_file, output_file)


if __name__ == "__main__":
    main()
