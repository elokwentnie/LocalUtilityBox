# LocalUtilityBox
## Don't waste your time searching for web solutions, do it in your terminal.

**LocalUtilityBox** is a versatile command-line utility designed to simplify your image and document processing tasks. With LocalUtilityBox, you can:
* Work locally, keeping your data private and secure.
* Avoid online tools that share your files on external servers.
* Enjoy efficient processing directly from your terminal.

## Features
**LocalUtilityBox** comes packed with tools to make your life easier:
* **Image Processing**
   * Convert images between formats (WebP, JPG, PNG, TIFF, HEIC).
   * Resize and compress images.
   * Remove backgrounds from images.
   * Convert images to greyscale.
   * Extract metadata and text (OCR) from images.
   * Batch-process entire folders.
* **PDF Management**
   * Split, merge, and add watermarks to PDFs.
   * Convert PDFs to image files (PNG/JPG).
   * Extract text or images from PDFs.
* **Document Conversion**
   * Convert DOC/DOCX to PDF and vice versa.
* **Data Format Conversion**
   * Convert between CSV, Excel, and JSON formats.
* **Video/Audio**
   * Extract audio from video files.
* **Convenient Access**
   * User-friendly command-line commands for all operations.
   * **Unified GUI application** with tabbed interface for easy access to all tools.


## Installation

### Method 1: Install from Git Repository (Recommended)

Install directly from the repository:

```bash
pip install --user git+https://github.com/elokwentnie/LocalUtilityBox.git
```

Or from a specific branch:
```bash
pip install --user git+https://github.com/elokwentnie/LocalUtilityBox.git@main
```

### Method 2: Install from Source

1. Clone the Repository
```bash
git clone https://github.com/elokwentnie/LocalUtilityBox.git
cd LocalUtilityBox
```

2. Install Package Globally (No Virtual Environment Needed)
```bash
# User installation (recommended - no sudo needed)
pip install --user .

# OR system-wide installation (requires permissions)
pip install .
```

**Note:** After installation with `--user`, ensure `~/.local/bin` is in your PATH:
```bash
# Linux/Mac - add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Method 3: Install Distribution Package

If you have a `.whl` file, install it directly:
```bash
pip install --user LocalUtilityBox-1.0.0-py3-none-any.whl
```

### Verify Installation

After installation, verify that commands work:
```bash
# Test CLI command
heic_to_jpg --help

# Launch GUI
localutilitybox-gui
# Or use the shorter alias:
lub-gui
```

**Important:** After installation, all CLI commands (`heic_to_jpg`, `merge_pdf`, etc.) and the GUI (`localutilitybox-gui`) are available globally - no need to activate a Python environment!

## Usage

### Using the GUI

**From the terminal:**
```bash
localutilitybox-gui
# Or use the shorter alias:
lub-gui
```

**From an icon (macOS):**  
Double-click **LocalUtilityBox.app** in the project folder to open the GUI like any other app. You can drag it to the Dock, move it to Applications, or keep it in the project—it will use your installed package or run from the project if needed.

The GUI provides a tabbed interface with all tools organized by category:
- **Image Processing**: Format conversions, resizing, background removal, metadata extraction, OCR
- **File Management**: PDF operations, document conversions, data format conversions
- **Video/Audio**: Audio extraction from video

### Using Command Line

Once installed, **LocalUtilityBox** provides a set of simple commands for various tasks. Here are a few examples:

**Image Conversion:**
```bash
# Convert WebP to JPG
webp_to_jpg [-h] [-o OUTPUT_FILE] [-b {white,black}] input_file

# Convert HEIC to JPG
heic_to_jpg -f image1.heic image2.heic
heic_to_jpg -d /path/to/heic/files

# Remove background from image
remove_background -f image1.jpg image2.png
remove_background -d /path/to/images
```

**PDF Management:**
```bash
# Merge PDFs
merge_pdf -f file1.pdf file2.pdf file3.pdf -o merged.pdf
merge_pdf -d /path/to/pdfs -o merged.pdf

# Split PDF
split_pdf input.pdf              # Split into individual pages
split_pdf input.pdf -p 3         # Split into 3 parts

# Add watermark
add_watermark input.pdf -w watermark.pdf -p 0 1 2
```

**Document Conversion:**
```bash
# Convert DOC to PDF
doc_to_pdf input.docx -o output.pdf

# Convert PDF to DOC
pdf_to_doc input.pdf -o output.docx
```

**Data Format Conversion:**
```bash
# CSV to Excel
csv_to_excel data.csv -o data.xlsx

# Excel to CSV
excel_to_csv data.xlsx -o data.csv

# CSV to JSON
csv_to_json data.csv -o data.json
```

**Extraction:**
```bash
# Extract text from image (OCR)
extract_text_from_img image.png -s

# Extract audio from video
extract_audio_from_video video.mp4 -f mp3 -o audio.mp3
```

For help on any command, use the `-h` or `--help` flag:
```bash
heic_to_jpg --help
```

## Contribute
Have ideas or improvements? Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

Let me know if there’s anything more you’d like to include or refine!
