import sys
import argparse
from pathlib import Path
from typing import List, Optional
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError


def split_pdf(input_file: Path, parts: Optional[List[List[int]]] = None, output_dir: Path = None) -> None:
    base_name = input_file.stem
    if output_dir is None:
        output_dir = input_file.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        reader = PdfReader(str(input_file))
        if not parts:
            # Split into individual pages
            for i, page in enumerate(reader.pages, start=1):
                output_file = output_dir / f"{base_name}_page_{i}.pdf"
                write_pages_to_pdf([page], output_file)
        else:
            # Split into specified parts
            for i, part in enumerate(parts, start=1):
                output_file = output_dir / f"{base_name}_part_{i}.pdf"
                pages_to_write = [reader.pages[page_num] for page_num in part]
                write_pages_to_pdf(pages_to_write, output_file)
        print("Successfully split the PDF into parts.")

    except PdfReadError as e:
        print(f"Error reading PDF file '{input_file}': {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def write_pages_to_pdf(pages: List, output_file: Path) -> None:
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    try:
        with open(output_file, "wb") as file:
            writer.write(file)
        print(f"Successfully created: {output_file}")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")
        raise


def parse_parts_argument(arg: str) -> int:
    """Parse and validate the parts argument."""
    try:
        num_parts = int(arg)
        if num_parts < 1:
            raise argparse.ArgumentTypeError("Number of parts must be greater than 0.")
        return num_parts
    except ValueError:
        raise argparse.ArgumentTypeError("Number of parts must be an integer.")


def get_splitting_parts(pdf_length: int, num_parts: int) -> List[List[int]]:
    """Calculate page ranges for splitting the PDF."""
    pages_per_part = pdf_length // num_parts
    remainder = pdf_length % num_parts

    parts = []
    start = 0
    for i in range(num_parts):
        end = start + pages_per_part + (1 if i < remainder else 0)
        parts.append(list(range(start, end)))
        start = end
    return parts


def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF into individual pages (default) or into a specified number of parts."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "-p",
        "--parts",
        type=parse_parts_argument,
        default=None,
        help="Number of parts to split the PDF into",
    )

    args = parser.parse_args()
    input_file = args.input_file

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".pdf":
        print(f"Error: '{input_file}' does not exist or is not a PDF file.")
        sys.exit(1)

    try:
        reader = PdfReader(str(input_file))
        pdf_length = len(reader.pages)
    except PdfReadError as e:
        print(f"Error reading PDF file '{input_file}': {e}")
        sys.exit(1)

    if args.parts:
        if args.parts > pdf_length:
            print(
                "Number of parts cannot exceed the number of pages. Splitting into individual pages."
            )
            parts = None
        else:
            parts = get_splitting_parts(pdf_length, args.parts)
    else:
        parts = None

    split_pdf(input_file, parts)


if __name__ == "__main__":
    main()
