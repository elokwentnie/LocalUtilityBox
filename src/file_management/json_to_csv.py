import pandas as pd
import sys
import argparse
from pathlib import Path
import json


def json_to_csv(input_file: Path, output_file: Path = None) -> None:
    if output_file is None or output_file.suffix.lower() != ".csv":
        output_file = input_file.with_suffix(".csv")
    try:
        with open(input_file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        # Fast paths for common JSON shapes to avoid expensive deep normalization.
        if isinstance(data, list):
            if data and all(isinstance(item, dict) for item in data):
                df = pd.DataFrame.from_records(data)
            else:
                df = pd.DataFrame({"value": data})
        elif isinstance(data, dict):
            list_of_dicts_keys = [
                key for key, value in data.items()
                if isinstance(value, list)
                and (not value or all(isinstance(item, dict) for item in value))
            ]
            if len(list_of_dicts_keys) == 1 and len(data) == 1:
                df = pd.DataFrame.from_records(data[list_of_dicts_keys[0]])
            else:
                df = pd.json_normalize(data, sep=".")
        else:
            df = pd.DataFrame({"value": [data]})

        # Write DataFrame to CSV without the index
        df.to_csv(output_file, index=False)
        print(f"Conversion successful: {output_file}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_file}: {e}")
        raise
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Convert a JSON file to a CSV file.")
    parser.add_argument("input_file", type=Path, help="Path to the input .json file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output .csv file",
    )

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".json":
        print(f"Error: {input_file} does not exist or is not a JSON file.")
        sys.exit(1)

    json_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
