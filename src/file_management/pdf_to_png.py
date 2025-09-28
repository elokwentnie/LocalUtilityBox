import sys
import argparse
from pathlib import Path
from pdf2image import convert_from_path
from zipfile import ZipFile
from io import BytesIO

from utils.error_handling import (
    FileValidationError,
    ConversionError,
    validate_file_exists,
    handle_conversion_error
)
from utils.logging_config import setup_logging, get_logger


def pdf_to_png(input_file: Path, zip_output: bool = False) -> None:
    """Convert PDF pages to PNG images with optional zipping."""
    logger = get_logger(__name__)
    base_name = input_file.stem
    output_dir = input_file.parent

    try:
        # Validate input file
        validate_file_exists(input_file, '.pdf')
        
        # Convert PDF to a list of images
        logger.info(f"Converting PDF to images: {input_file}")
        pages = convert_from_path(str(input_file))
        logger.info(f"Converted {len(pages)} pages from {input_file}.")
        print(f"Converted {len(pages)} pages from {input_file}.")

        if zip_output:
            zip_filename = output_dir / f"{base_name}_images.zip"
            logger.info(f"Creating zip archive: {zip_filename}")
            with ZipFile(zip_filename, "w") as zipf:
                for i, page in enumerate(pages, start=1):
                    # Save image to in-memory bytes buffer
                    img_buffer = BytesIO()
                    page.save(img_buffer, format="PNG")
                    img_buffer.seek(0)

                    # Define the image file name inside the zip
                    image_name = f"{base_name}_page_{i}.png"

                    # Write the image buffer to the zip file
                    zipf.writestr(image_name, img_buffer.read())
                    logger.debug(f"Added {image_name} to zip archive")
                    print(f"Added {image_name} to {zip_filename}.")

            logger.info(f"Successfully created zip archive: {zip_filename}")
            print(f"Successfully zipped images into: {zip_filename}")
        else:
            for i, page in enumerate(pages, start=1):
                output_file = output_dir / f"{base_name}_page_{i}.png"
                page.save(output_file, "PNG")
                logger.debug(f"Created PNG file: {output_file}")
                print(f"Successfully created: {output_file}")

            logger.info("Successfully converted PDF pages to PNG images")
            print("Successfully converted PDF pages to PNG images.")
    except FileValidationError as e:
        logger.error(f"File validation error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        handle_conversion_error(e, input_file)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to individual PNG images, with an option to zip the output."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        help="Zip the output PNG files into a single archive.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        setup_logging(level="DEBUG")
    else:
        setup_logging(level="INFO")

    input_file = args.input_file
    zip_output = args.zip

    pdf_to_png(input_file, zip_output)


if __name__ == "__main__":
    main()
