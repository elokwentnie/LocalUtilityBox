import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def remove_background(input_files, output_dir=None):
    try:
        import numpy as np
        import rembg
    except ImportError:
        raise ImportError(
            "rembg is required for background removal. "
            "Install it with: pip install rembg[cpu]"
        )

    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_files:
        try:
            image = Image.open(file)
            file_ext = file.suffix.lower()
            if output_dir:
                output_file = output_dir / f"{file.stem}-background-removed{file_ext}"
            else:
                output_file = file.with_stem(f"{file.stem}-background-removed")

            input_array = np.array(image)
            output_array = rembg.remove(input_array)
            output_image = Image.fromarray(output_array)

            if output_image.mode == "RGBA":
                # Remove alpha channel for JPEG or keep it for PNG
                if file_ext in [".jpg", ".jpeg"]:
                    # Convert RGBA to RGB
                    output_image = output_image.convert("RGB")

            output_image.save(output_file, quality=95)
            print(f"Background removal successful: {output_file}")
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file '{file}'. Skipping.")
        except Exception as e:
            print(f"Failed to remove background of '{file}': {e}")


def main():
    parser = argparse.ArgumentParser(description="Remove background from photos.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--input_files", type=Path, nargs="+", help="Input file path(s)"
    )
    group.add_argument(
        "-d", "--input_directory", type=Path, help="Input directory with photos inside"
    )

    args = parser.parse_args()

    if args.input_files:
        input_files = args.input_files
    elif args.input_directory:
        input_directory = args.input_directory
        if not input_directory.is_dir():
            print(f"Error: '{input_directory}' is not a valid directory.")
            sys.exit(1)
        input_files = list(input_directory.glob("*"))
        input_files = [
            file
            for file in input_files
            if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
        ]
        if not input_files:
            print(f"No .jpg or .png files found in directory '{input_directory}'")
            sys.exit(1)
    else:
        print("Error: Either --input_files or --input_directory must be provided.")
        sys.exit(1)

    # Validate input files
    for file in input_files:
        if not file.is_file():
            print(f"Error: '{file}' does not exist or is not a file.")
            sys.exit(1)

    remove_background(input_files)


if __name__ == "__main__":
    main()
