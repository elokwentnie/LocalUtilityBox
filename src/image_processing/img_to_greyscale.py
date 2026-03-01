import sys
import argparse
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError


def img_to_greyscale(
    input_file: Path, output_file: Path = None, quality: int = 85
) -> None:
    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}-greyscale")
    try:
        with Image.open(input_file) as image:
            image_gray = ImageOps.grayscale(image)
            image_gray.save(output_file, quality=quality)
            print(f"Conversion successful: {output_file}")
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{input_file}'.")
        raise
    except Exception as e:
        print(f"Error processing '{input_file}': {e}")
        raise


def validate_quality(value: str) -> int:
    try:
        quality = int(value)
        if not 0 <= quality <= 100:
            raise ValueError
        return quality
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Quality must be an integer between 0 and 100."
        )


def main():
    parser = argparse.ArgumentParser(description="Convert an image file to grayscale.")
    parser.add_argument("input_file", type=Path, help="Path to the input image file")
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Path for the output image file",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=validate_quality,
        default=85,
        help="Output image quality (0-100)",
    )

    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"Error: '{args.input_file}' does not exist or is not a file.")
        sys.exit(1)

    img_to_greyscale(args.input_file, args.output_file, args.quality)


if __name__ == "__main__":
    main()
