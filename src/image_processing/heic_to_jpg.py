from PIL import Image
import pillow_heif
import sys
import argparse
from pathlib import Path


def validate_quality(value):
    """Validate that the quality is an integer between 1 and 100."""
    try:
        ivalue = int(value)
        if not 1 <= ivalue <= 100:
            raise argparse.ArgumentTypeError(
                "Quality must be an integer between 1 and 100."
            )
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Quality must be an integer between 1 and 100."
        )


def heic_to_jpg(input_files, output_directory=None, quality=95):
    if output_directory is None:
        output_directory = Path(input_files[0]).parent
    else:
        output_directory = Path(output_directory)

    for file in input_files:
        try:
            heif_file = pillow_heif.read_heif(file)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            file_path = Path(file)
            output_file = output_directory / (file_path.stem + ".jpg")
            image.save(output_file, "JPEG", quality=quality)
            print(f"Conversion successful: {output_file}")
        except Exception as e:
            print(f"Failed to convert '{file}': {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert .HEIC files to .jpg.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--input_files", type=Path, nargs="+", help="Input .HEIC file paths"
    )
    group.add_argument(
        "-d",
        "--input_directory",
        type=Path,
        help="Directory containing .HEIC files to convert",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output directory"
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=validate_quality,
        default=95,
        help="Output image quality (1-100), default is 95",
    )

    args = parser.parse_args()
    output_directory = args.output
    quality = args.quality

    if args.input_files:
        input_files = args.input_files
    elif args.input_directory:
        if not args.input_directory.is_dir():
            print(f"Error: '{args.input_directory}' is not a valid directory.")
            sys.exit(1)
        input_files = list(args.input_directory.glob("*.heic")) + list(
            args.input_directory.glob("*.HEIC")
        )
        if not input_files:
            print(f"No .HEIC files found in directory '{args.input_directory}'")
            sys.exit(1)
    else:
        print("Error: Either --input_files or --input_directory must be provided.")
        sys.exit(1)

    # Validate that input files exist
    for file in input_files:
        if not file.is_file():
            print(f"Error: '{file}' does not exist or is not a file.")
            sys.exit(1)

    heic_to_jpg([str(file) for file in input_files], output_directory, quality)


if __name__ == "__main__":
    main()
