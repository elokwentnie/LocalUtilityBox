from pdf2docx import parse
import sys
import argparse
from pathlib import Path


def pdf_to_docx(input_file: Path, output_file: Path = None) -> None:
    # Determine the output file path
    if output_file is None or output_file.suffix.lower() != ".docx":
        output_file = input_file.with_suffix(".docx")

    try:
        # Convert the PDF file to DOCX
        parse(str(input_file), str(output_file))
        print(f"Conversion successful: {output_file}")
    except Exception as e:
        print(f"Error converting {input_file} to DOCX: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Convert a PDF file to DOCX format.")
    parser.add_argument("input_file", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output DOCX file",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".pdf":
        print(f"Error: {input_file} does not exist or is not a PDF file.")
        sys.exit(1)

    pdf_to_docx(input_file, output_file)


if __name__ == "__main__":
    main()
