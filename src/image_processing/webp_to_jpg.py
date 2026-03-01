import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def has_transparency(img_path: Path) -> bool:
    with Image.open(img_path) as img:
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            alpha = img.getchannel("A")
            if any(pixel < 255 for pixel in alpha.getdata()):
                return True
    return False


def webp_to_jpg(
    input_file: Path, output_file: Path = None, background_color: str = "black"
) -> None:
    if output_file is None or output_file.suffix.lower() not in [".jpg", ".jpeg"]:
        output_file = input_file.with_suffix(".jpg")
    try:
        with Image.open(input_file) as im:
            if has_transparency(input_file):
                bg_color = (
                    (255, 255, 255)
                    if background_color.lower() == "white"
                    else (0, 0, 0)
                )
                im = im.convert("RGBA")
                background = Image.new("RGB", im.size, bg_color)
                background.paste(im, (0, 0), im)
                background.save(output_file, "JPEG", quality=95)
            else:
                im = im.convert("RGB")
                im.save(output_file, "JPEG", quality=95)
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
    parser = argparse.ArgumentParser(description="Convert .webp to .jpg")
    parser.add_argument("input_file", type=Path, help="Input .webp file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output .jpg file name"
    )
    parser.add_argument(
        "-b",
        "--background",
        choices=["white", "black"],
        default="black",
        help="Background color for images with transparency (default: black)",
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    background_color = args.background

    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist or is not a file.")
        sys.exit(1)
    if input_file.suffix.lower() != ".webp":
        print(f"Error: Input file '{input_file}' is not a .webp file.")
        sys.exit(1)

    webp_to_jpg(input_file, output_file, background_color)


if __name__ == "__main__":
    main()
