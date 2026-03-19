import sys
import argparse
from datetime import datetime
from pathlib import Path
from PyPDF2 import PdfMerger
from PyPDF2.errors import PdfReadError


def merge_pdf(input_files: list[Path], output_file: Path = None) -> None:
    if not input_files:
        raise ValueError("No input PDF files provided.")

    missing = [Path(pdf_file) for pdf_file in input_files if not Path(pdf_file).is_file()]
    if missing:
        raise FileNotFoundError(
            "Input PDF file(s) not found: " + ", ".join(str(path) for path in missing)
        )

    if output_file is None or output_file.suffix.lower() != ".pdf":
        print("No valid output path provided.")
        print("Merged file will be saved in the directory of the first input file.")

        first_input = Path(input_files[0])
        current_date = datetime.now().strftime("%Y%m%d-%H%M")
        output_filename = f"{current_date}_merged.pdf"

        output_file = first_input.parent / output_filename
        print(f"Merged file will be saved as: {output_file}")

    merger = PdfMerger()
    appended = 0
    for pdf_file in input_files:
        try:
            merger.append(str(pdf_file))
            appended += 1
        except PdfReadError:
            raise PdfReadError(
                f"'{pdf_file}' is not a valid PDF file or is corrupted."
            )
        except Exception as e:
            raise RuntimeError(f"Unexpected error while reading '{pdf_file}': {e}") from e

    if appended == 0:
        merger.close()
        raise ValueError("No valid PDF pages were merged.")
    try:
        merger.write(str(output_file))
        print(f"PDFs merged successfully into '{output_file}'")
    except Exception as e:
        print(f"Error writing output PDF: {e}")
        raise
    finally:
        merger.close()


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into a single PDF."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--input_files", type=Path, nargs="+", help="Input PDF file paths"
    )
    group.add_argument(
        "-d",
        "--input_directory",
        type=Path,
        help="Directory containing PDF files to merge",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output PDF file path"
    )

    args = parser.parse_args()

    if args.input_files:
        input_files = args.input_files
    elif args.input_directory:
        if not args.input_directory.is_dir():
            print(f"Error: '{args.input_directory}' is not a valid directory.")
            sys.exit(1)
        input_files = sorted(args.input_directory.glob("*.pdf"))
        if not input_files:
            print(f"No PDF files found in directory '{args.input_directory}'")
            sys.exit(1)
    else:
        print("Error: Either input files or input directory must be provided.")
        sys.exit(1)

    # Validate that input files exist and are files
    for pdf_file in input_files:
        if not pdf_file.is_file():
            print(f"Error: '{pdf_file}' does not exist or is not a file.")
            sys.exit(1)

    merge_pdf(input_files, args.output)


if __name__ == "__main__":
    main()
