import sys
import math
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


PAGE_SIZES = {
    "a4": (595.28, 841.89),
    "letter": (612, 792),
    "legal": (612, 1008),
}


def long_png_to_pdf(
    input_file: Path,
    output_file: Path = None,
    page_size: str = "a4",
    overlap: int = 0,
) -> None:
    """Split a long/tall PNG into a multi-page PDF.

    The image width is scaled to fit the page width, then the height is
    sliced into page-sized strips.

    Args:
        input_file: Path to the input PNG file.
        output_file: Path for the output PDF. Defaults to same name with .pdf.
        page_size: One of 'a4', 'letter', 'legal'.
        overlap: Pixel overlap between consecutive pages to avoid cutting
                 content at boundaries.
    """
    if output_file is None:
        output_file = input_file.with_suffix(".pdf")

    page_size = page_size.lower()
    if page_size not in PAGE_SIZES:
        raise ValueError(f"Unknown page size '{page_size}'. Choose from: {', '.join(PAGE_SIZES)}.")

    page_w_pt, page_h_pt = PAGE_SIZES[page_size]

    try:
        with Image.open(input_file) as img:
            img = img.convert("RGB")
            img_w, img_h = img.size

            scale = page_w_pt / img_w
            chunk_height = int(page_h_pt / scale)

            step = max(1, chunk_height - overlap)
            num_pages = math.ceil(max(img_h - overlap, 1) / step)

            pages = []
            for i in range(num_pages):
                top = i * step
                bottom = min(top + chunk_height, img_h)
                cropped = img.crop((0, top, img_w, bottom))

                page_img_h = int((bottom - top) * scale)
                page_img_w = int(page_w_pt)
                resized = cropped.resize((page_img_w, page_img_h), Image.LANCZOS)

                if page_img_h < int(page_h_pt):
                    canvas = Image.new("RGB", (page_img_w, int(page_h_pt)), (255, 255, 255))
                    canvas.paste(resized, (0, 0))
                    pages.append(canvas)
                else:
                    pages.append(resized)

            pages[0].save(
                output_file,
                "PDF",
                resolution=72.0,
                save_all=True,
                append_images=pages[1:],
            )
        print(f"Split into {num_pages} page(s): {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        raise
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{input_file}'.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Split a long/tall PNG image into a multi-page PDF."
    )
    parser.add_argument("input_file", type=Path, help="Input PNG file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output PDF file path"
    )
    parser.add_argument(
        "-p",
        "--page-size",
        choices=list(PAGE_SIZES),
        default="a4",
        help="Page size (default: a4)",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=0,
        help="Pixel overlap between pages to avoid cutting content (default: 0)",
    )
    args = parser.parse_args()

    input_file = args.input_file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)
    if input_file.suffix.lower() != ".png":
        print(f"Error: Input file '{input_file}' is not a .png file.")
        sys.exit(1)

    long_png_to_pdf(input_file, args.output_file, args.page_size, args.overlap)


if __name__ == "__main__":
    main()
