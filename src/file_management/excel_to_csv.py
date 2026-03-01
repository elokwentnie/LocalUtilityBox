import pandas as pd
import sys
import argparse
from pathlib import Path


def excel_to_csv(
    input_file: Path, separator: str = ",", output_file: Path = None
) -> None:
    # Determine the output file path
    if output_file is None or output_file.suffix.lower() != ".csv":
        output_file = input_file.with_suffix(".csv")

    try:
        # Read the Excel file
        df = pd.read_excel(input_file)
        # Drop columns that are completely empty
        df_cleaned = df.dropna(axis=1, how="all")
        # Write to CSV
        df_cleaned.to_csv(output_file, index=False, sep=separator)
        print(f"Conversion successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        raise
    except pd.errors.EmptyDataError:
        print(f"Error: The file {input_file} is empty.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def parse_separator_argument(arg: str) -> str:
    """Parse and validate the separator argument."""
    csv_separators = {
        ",": "Comma",
        ";": "Semicolon",
        "\t": "Tab",
        "|": "Pipe",
        " ": "Space",
        "^": "Caret",
        "~": "Tilde",
        ":": "Colon",
        "#": "Hash/Pound",
        "@": "At sign",
        "!": "Exclamation mark",
    }

    if arg not in csv_separators:
        valid_seps = ", ".join(repr(s) for s in csv_separators.keys())
        raise argparse.ArgumentTypeError(
            f"Invalid separator '{arg}'. Must be one of {valid_seps}."
        )
    return arg


def main():
    parser = argparse.ArgumentParser(
        description="Convert an XLSX (Excel) file to a CSV file."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input .xlsx file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output .csv file",
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=parse_separator_argument,
        default=",",
        help="Separator for the output .csv file (default: ',').",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    separator = args.separator

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".xlsx":
        print(f"Error: {input_file} does not exist or is not an XLSX file.")
        sys.exit(1)

    excel_to_csv(input_file, separator, output_file)


if __name__ == "__main__":
    main()
