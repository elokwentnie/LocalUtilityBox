import sys
import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import pytesseract


def extract_text_from_img(input_file: Path, save_flag: bool = False) -> None:
    try:
        # Open the image file
        with Image.open(input_file) as img:
            # Convert image to RGB if not already
            img = img.convert("RGB")
            # Extract text from image using pytesseract
            extracted_text = pytesseract.image_to_string(img)

        # Print the extracted text
        print(extracted_text)

        # Save the extracted text to a file if requested
        if save_flag:
            output_file = input_file.with_name(f"{input_file.stem}_extracted-text.txt")
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(extracted_text)
            print(f"Successfully saved extracted text to: {output_file}")
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
    parser = argparse.ArgumentParser(
        description="Extract text from an image using OCR."
    )
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

    extract_text_from_img(input_file, args.save)


if __name__ == "__main__":
    main()
