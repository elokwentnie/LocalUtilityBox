import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def tiff_to_jpg(input_file: Path, output_file: Path = None, quality: int = 95) -> None:
    if output_file is None or output_file.suffix.lower() not in [".jpg", ".jpeg"]:
        output_file = input_file.with_suffix(".jpg")
    try:
        with Image.open(input_file) as img:
            img = img.convert("RGB")
            img.save(output_file, format="JPEG", quality=quality)
        print(f"Conversion successful: {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        raise
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{input_file}'.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def validate_quality(value: str) -> int:
    try:
        quality = int(value)
        if not 0 <= quality <= 100:
            raise argparse.ArgumentTypeError("Quality must be between 0 and 100.")
        return quality
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Quality must be an integer between 0 and 100."
        )


def main():
    parser = argparse.ArgumentParser(description="Convert .tiff to .jpg")
    parser.add_argument("input_file", type=Path, help="Input .tiff file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output .jpg file path"
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=validate_quality,
        default=95,
        help="Quality (0-100), default is 95.",
    )

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    quality = args.quality

    # Validate input file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)
    if input_file.suffix.lower() not in [".tif", ".tiff"]:
        print(f"Error: Input file '{input_file}' is not a .tiff or .tif file.")
        sys.exit(1)

    tiff_to_jpg(input_file, output_file, quality)


if __name__ == "__main__":
    main()
