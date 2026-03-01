import sys
import argparse
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError


def reduce_img_size(input_files, scale_factor=0.5, quality=85, output_dir=None):
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    for file in input_files:
        try:
            with Image.open(file) as image:
                original_width, original_height = image.size
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                size = (new_width, new_height)
                if output_dir:
                    output_file = output_dir / f"{file.stem}-reduced.jpg"
                else:
                    output_file = file.with_stem(f"{file.stem}-reduced").with_suffix(".jpg")
                resized_image = ImageOps.contain(image, size)
                resized_image.save(output_file, "JPEG", quality=quality)
                print(
                    f"Reduced size of '{file}' by {int(scale_factor * 100)}% and saved to '{output_file}'"
                )
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file '{file}'. Skipping.")
        except Exception as e:
            print(f"Failed to reduce size of '{file}': {e}")


def validate_percentage(value):
    try:
        f = float(value)
        if not 0 < f <= 100:
            raise argparse.ArgumentTypeError("Percentage must be between 0 and 100.")
        return f
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number.")


def validate_quality(value):
    try:
        i = int(value)
        if not 1 <= i <= 100:
            raise argparse.ArgumentTypeError("Quality must be between 1 and 100.")
        return i
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer between 1 and 100.")


def main():
    parser = argparse.ArgumentParser(description="Reduce the size of .jpg images.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--input_files", type=Path, nargs="+", help="Input .jpg file paths"
    )
    group.add_argument(
        "-d",
        "--input_directory",
        type=Path,
        help="Input directory containing .jpg files",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=validate_percentage,
        default=50,
        help="Percentage to scale images (1-100), default is 50.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=validate_quality,
        default=85,
        help="JPEG quality level (1-100), default is 85.",
    )

    args = parser.parse_args()
    scale_factor = args.scale / 100

    if args.input_files:
        input_files = args.input_files
    elif args.input_directory:
        if not args.input_directory.is_dir():
            print(f"Error: '{args.input_directory}' is not a valid directory.")
            sys.exit(1)
        input_files = list(args.input_directory.glob("*.jpg")) + list(
            args.input_directory.glob("*.jpeg")
        )
        if not input_files:
            print(f"No .jpg or .jpeg files found in directory '{args.input_directory}'")
            sys.exit(1)
    else:
        print("Error: Either --input_files or --input_directory must be provided.")
        sys.exit(1)

    # Validate input files
    for file in input_files:
        if not file.is_file():
            print(f"Error: '{file}' does not exist or is not a file.")
            sys.exit(1)

    reduce_img_size(input_files, scale_factor, args.quality)


if __name__ == "__main__":
    main()
