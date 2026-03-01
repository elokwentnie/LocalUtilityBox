from pathlib import Path
from typing import Union, List
import sys
import argparse

from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.errors import PdfReadError


def add_watermark(
    input_file: Path,
    watermark_pdf: Path,
    page_indices: Union[str, List[int]] = "ALL",
    output_file: Path = None,
) -> None:
    try:
        reader = PdfReader(input_file)
        watermark_reader = PdfReader(watermark_pdf)
    except PdfReadError as e:
        print(f"Error reading PDF files: {e}")
        raise

    if page_indices == "ALL":
        page_indices = list(range(len(reader.pages)))

    if not watermark_reader.pages:
        raise ValueError("The watermark PDF has no pages.")

    watermark_page = watermark_reader.pages[0]

    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}-watermarked")

    writer = PdfWriter()
    for index in page_indices:
        try:
            content_page = reader.pages[index]
        except IndexError:
            print(f"Error: Page index {index} out of range.")
            raise

        # Merge the watermark with the content page
        content_page.merge_page(watermark_page)
        writer.add_page(content_page)

    try:
        with open(output_file, "wb") as fp:
            writer.write(fp)
        print(f"Watermarked PDF saved as: {output_file}")
    except Exception as e:
        print(f"Error writing output PDF: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Add a watermark to a PDF file. The watermark should be a PDF file "
            "with the same dimensions as the input PDF."
        )
    )
    parser.add_argument("input_file", type=Path, help="Input PDF file path")
    parser.add_argument(
        "-w", "--watermark", type=Path, required=True, help="Watermark PDF file path"
    )
    parser.add_argument(
        "-p",
        "--pages",
        nargs="*",
        default="ALL",
        help="Page indices to apply the watermark (zero-based). Default is all pages.",
    )
    args = parser.parse_args()

    if not args.input_file.is_file() or args.input_file.suffix.lower() != ".pdf":
        print(f"Error: {args.input_file} does not exist or is not a PDF file.")
        sys.exit(1)

    if not args.watermark.is_file() or args.watermark.suffix.lower() != ".pdf":
        print(f"Error: {args.watermark} does not exist or is not a PDF file.")
        sys.exit(1)

    add_watermark(args.input_file, args.watermark, args.pages)


if __name__ == "__main__":
    main()
