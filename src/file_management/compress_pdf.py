import sys
import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def compress_pdf(input_file: Path, output_file: Path = None, power: int = 2) -> None:
    """Compress a PDF by rewriting it with compressed streams.

    power levels:
        0 = no extra compression (just rewrite)
        1 = light  (/Flate, remove duplicates)
        2 = medium (above + compress content streams)
        3 = heavy  (above + remove metadata)
    """
    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}-compressed")

    reader = PdfReader(str(input_file))
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    if power >= 3:
        writer.remove_links()

    if reader.metadata and power < 3:
        writer.add_metadata(
            {k: v for k, v in reader.metadata.items() if v}
        )

    with open(output_file, "wb") as f:
        writer.write(f)

    original = input_file.stat().st_size
    compressed = output_file.stat().st_size
    ratio = (1 - compressed / original) * 100 if original > 0 else 0
    print(
        f"Compressed: {original:,} B -> {compressed:,} B "
        f"({ratio:.1f}% reduction) -> {output_file}"
    )


def main():
    parser = argparse.ArgumentParser(description="Compress a PDF file.")
    parser.add_argument("input_file", type=Path, help="Input PDF file path")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output PDF file path"
    )
    parser.add_argument(
        "-p", "--power", type=int, default=2, choices=[0, 1, 2, 3],
        help="Compression level (0=minimal, 3=maximum)",
    )
    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"Error: '{args.input_file}' does not exist or is not a file.")
        sys.exit(1)

    compress_pdf(args.input_file, args.output, args.power)


if __name__ == "__main__":
    main()
