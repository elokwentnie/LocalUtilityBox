import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def jpg_to_png(input_file: Path, output_file: Path = None, quality: int = 95) -> None:
    if output_file is None or output_file.suffix.lower() != ".png":
        output_file = input_file.with_suffix(".png")
    try:
        with Image.open(input_file) as im:
            im = im.convert("RGB")
            im.save(output_file, format="PNG", quality=quality)
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
        i = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Quality must be a number.")
    if not 0 <= i <= 100:
        raise argparse.ArgumentTypeError("Quality must be between 0 and 100.")
    return i


def main():
    parser = argparse.ArgumentParser(
        description="Convert a .jpg or .jpeg image to .png format."
    )
    parser.add_argument("input_file", type=Path, help="Input .jpg or .jpeg file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output .png file path"
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=validate_quality,
        default=95,
        help="Quality (0-100), default is 95",
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    quality = args.quality

    # Validate input file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)
    if input_file.suffix.lower() not in [".jpg", ".jpeg"]:
        print(f"Error: Input file '{input_file}' is not a .jpg or .jpeg file.")
        sys.exit(1)

    jpg_to_png(input_file, output_file, quality)


if __name__ == "__main__":
    main()
