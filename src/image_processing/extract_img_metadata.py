import sys
import argparse
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


def extract_img_metadata(input_file: Path, save_flag: bool = False) -> None:
    try:
        with Image.open(input_file) as img:
            # Basic image information
            info_dict = {
                "Image Name": input_file.name,
                "Image Size": img.size,
                "Image Height": img.height,
                "Image Width": img.width,
                "Image Format": img.format,
                "Image Mode": img.mode,
                "Is Animated": getattr(img, "is_animated", False),
                "Frames in Image": getattr(img, "n_frames", 1),
            }

            metadata_lines = [
                f"{label:25}: {value}" for label, value in info_dict.items()
            ]

            # EXIF data
            exifdata = img.getexif()
            if exifdata:
                metadata_lines.append("\nEXIF Data:")
                for tag_id, data in exifdata.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if isinstance(data, bytes):
                        try:
                            data = data.decode()
                        except UnicodeDecodeError:
                            data = data.decode("latin1", "ignore")
                    metadata_lines.append(f"{tag:25}: {data}")
            else:
                metadata_lines.append("No EXIF data found.")

            for line in metadata_lines:
                print(line)

            if save_flag:
                output_file = input_file.with_name(f"{input_file.stem}_metadata.txt")
                with open(output_file, "w", encoding="utf-8") as file:
                    for line in metadata_lines:
                        file.write(f"{line}\n")
                    print(f"Successfully saved extracted text to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        raise
    except Image.UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{input_file}'.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Extract metadata from an image file.")
    parser.add_argument("input_file", type=Path, help="Path to the input image file")
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save the extracted text to a .txt file",
    )
    args = parser.parse_args()

    input_file = args.input_file

    # Validate the input file
    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)

    extract_img_metadata(input_file, args.save)


if __name__ == "__main__":
    main()
