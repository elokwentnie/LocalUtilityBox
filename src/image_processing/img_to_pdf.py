import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import img2pdf


def img_to_pdf(input_file: Path, output_file: Path = None) -> None:
    if output_file is None:
        output_file = input_file.with_suffix(".pdf")

    with Image.open(input_file) as img:
        if img.mode in ("RGBA", "LA", "PA"):
            img = img.convert("RGB")
            temp_path = input_file.with_stem(f"{input_file.stem}_rgb_tmp")
            img.save(temp_path, "JPEG", quality=95)
            with open(output_file, "wb") as f:
                f.write(img2pdf.convert(str(temp_path)))
            temp_path.unlink()
        else:
            with open(output_file, "wb") as f:
                f.write(img2pdf.convert(str(input_file)))

    print(f"Conversion successful: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert an image file to PDF.")
    parser.add_argument("input_file", type=Path, help="Path to the input image file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output PDF file",
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate the input file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)

    img_to_pdf(input_file, output_file)


if __name__ == "__main__":
    main()
