import sys
import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def rotate_pdf(
    input_file: Path,
    rotation: int,
    pages: list[int] = None,
    output_file: Path = None,
) -> None:
    """Rotate pages in a PDF.

    rotation: degrees clockwise (90, 180, 270).
    pages:    0-based page indices to rotate, or None for all pages.
    """
    if rotation not in (90, 180, 270):
        raise ValueError(f"Rotation must be 90, 180, or 270 (got {rotation})")

    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}-rotated")

    reader = PdfReader(str(input_file))
    writer = PdfWriter()

    target_pages = set(pages) if pages else set(range(len(reader.pages)))

    for i, page in enumerate(reader.pages):
        if i in target_pages:
            page.rotate(rotation)
        writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)

    n = len(target_pages)
    print(f"Rotated {n} page(s) by {rotation}° -> {output_file}")


def reorder_pdf(
    input_file: Path,
    order: list[int],
    output_file: Path = None,
) -> None:
    """Reorder pages of a PDF according to the given index list."""
    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}-reordered")

    reader = PdfReader(str(input_file))
    writer = PdfWriter()

    for idx in order:
        if 0 <= idx < len(reader.pages):
            writer.add_page(reader.pages[idx])
        else:
            print(f"Warning: page index {idx} out of range, skipping")

    with open(output_file, "wb") as f:
        writer.write(f)

    print(f"Reordered {len(order)} pages -> {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Rotate or reorder PDF pages.")
    sub = parser.add_subparsers(dest="command", required=True)

    rot = sub.add_parser("rotate", help="Rotate pages")
    rot.add_argument("input_file", type=Path, help="Input PDF file")
    rot.add_argument(
        "-r", "--rotation", type=int, required=True, choices=[90, 180, 270],
        help="Rotation degrees clockwise",
    )
    rot.add_argument(
        "-p", "--pages", type=int, nargs="+",
        help="0-based page indices (default: all)",
    )
    rot.add_argument("-o", "--output", type=Path, default=None)

    reord = sub.add_parser("reorder", help="Reorder pages")
    reord.add_argument("input_file", type=Path, help="Input PDF file")
    reord.add_argument(
        "-p", "--pages", type=int, nargs="+", required=True,
        help="New page order as 0-based indices",
    )
    reord.add_argument("-o", "--output", type=Path, default=None)

    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"Error: '{args.input_file}' does not exist.")
        sys.exit(1)

    if args.command == "rotate":
        rotate_pdf(args.input_file, args.rotation, args.pages, args.output)
    elif args.command == "reorder":
        reorder_pdf(args.input_file, args.pages, args.output)


if __name__ == "__main__":
    main()
