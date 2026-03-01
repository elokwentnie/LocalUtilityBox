from docx2pdf import convert
import sys
import argparse
from pathlib import Path


def doc_to_pdf(input_file: Path, output_file: Path = None) -> None:
    # Determine the output file path
    if output_file is None or output_file.suffix.lower() != ".pdf":
        output_file = input_file.with_suffix(".pdf")
    try:
        # Convert the DOC/DOCX file to PDF
        convert(str(input_file), str(output_file))
        print(f"Conversion successful: {output_file}")
    except Exception as e:
        print(f"Error converting {input_file} to PDF: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Convert DOCX/DOC files to PDF.")
    parser.add_argument(
        "input_file", type=Path, help="Path to the input .docx or .doc file"
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output .pdf file",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() not in [".docx", ".doc"]:
        print(f"Error: {input_file} does not exist or is not a DOCX/DOC file.")
        sys.exit(1)

    doc_to_pdf(input_file, output_file)


if __name__ == "__main__":
    main()
