import sys
import argparse
from pathlib import Path
from pdf2image import convert_from_path
from zipfile import ZipFile
from io import BytesIO


def pdf_to_jpg(input_file: Path, zip_output: bool = False, output_dir: Path = None) -> None:
    base_name = input_file.stem
    if output_dir is None:
        output_dir = input_file.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Convert PDF to a list of images
        pages = convert_from_path(str(input_file))
        print(f"Converted {len(pages)} pages from {input_file}.")

        if zip_output:
            zip_filename = output_dir / f"{base_name}_images.zip"
            with ZipFile(zip_filename, "w") as zipf:
                for i, page in enumerate(pages, start=1):
                    # Save image to in-memory bytes buffer
                    img_buffer = BytesIO()
                    page.save(img_buffer, format="JPEG")
                    img_buffer.seek(0)

                    # Define the image file name inside the zip
                    image_name = f"{base_name}_page_{i}.jpg"

                    # Write the image buffer to the zip file
                    zipf.writestr(image_name, img_buffer.read())
                    print(f"Added {image_name} to {zip_filename}.")

            print(f"Successfully zipped images into: {zip_filename}")
        else:
            for i, page in enumerate(pages, start=1):
                output_file = output_dir / f"{base_name}_page_{i}.jpg"
                page.save(output_file, "JPEG")
                print(f"Successfully created: {output_file}")

            print("Successfully converted PDF pages to JPG images.")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to individual JPG images, with an option to zip the output."
    )
    parser.add_argument("input_file", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        help="Zip the output JPG files into a single archive.",
    )

    args = parser.parse_args()

    input_file = args.input_file
    zip_output = args.zip

    # Validate the input file
    if not input_file.is_file() or input_file.suffix.lower() != ".pdf":
        print(f"Error: '{input_file}' does not exist or is not a PDF file.")
        sys.exit(1)

    pdf_to_jpg(input_file, zip_output)


if __name__ == "__main__":
    main()
