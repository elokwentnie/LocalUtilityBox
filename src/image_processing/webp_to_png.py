import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def webp_to_png(input_file: Path, output_file: Path = None) -> None:
    if output_file is None or output_file.suffix.lower() != ".png":
        output_file = input_file.with_suffix(".png")
    try:
        with Image.open(input_file) as im:
            im = im.convert("RGBA")
            im.save(output_file, format="PNG")
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


def main():
    parser = argparse.ArgumentParser(description="Convert .webp to .png")
    parser.add_argument("input_file", type=Path, help="Input .webp file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output .png file name"
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # Validate input file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)
    if input_file.suffix.lower() != ".webp":
        print(f"Error: Input file '{input_file}' is not a .webp file.")
        sys.exit(1)

    webp_to_png(input_file, output_file)


if __name__ == "__main__":
    main()
