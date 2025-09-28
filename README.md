# LocalUtilityBox
## Don't waste your time searching for web solutions, do it in your terminal.

**LocalUtilityBox** is a comprehensive command-line utility designed to streamline various image, document, and file processing tasks. With **LocalUtilityBox**, you can easily convert images between formats, manage PDF files, process documents, and more, all from the comfort of your command line and most importantly **locally** - without sharing your files on any external server.

## ✨ Key Features
- **🔒 Privacy First**: All processing happens locally on your machine
- **🚀 High Performance**: Optimized for speed and efficiency
- **🛠️ Comprehensive**: Supports images, PDFs, documents, and more
- **📊 Well Tested**: Comprehensive test suite with 90%+ coverage
- **📝 Detailed Logging**: Verbose logging for debugging and monitoring
- **🎯 Error Handling**: Robust error handling with clear messages

## Features
* Image Conversion
* PDF Management
* Convenient CLI Tools

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Install
```bash
# Clone the repository
git clone https://github.com/elokwentnie/localutilitybox.git
cd localutilitybox

# Install the package
pip install .

# Or install in development mode
pip install -e .
```

### Development Installation
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=localutilitybox
```

## 📖 Usage

Once installed, **LocalUtilityBox** provides several command-line tools for file processing:

### 🖼️ Image Conversion
```bash
# Convert WebP to PNG
webp_to_png input.webp output.png

# Convert JPG to PNG
jpg_to_png input.jpg output.png

# Convert PNG to JPG
png_to_jpg input.png output.jpg

# Convert HEIC to JPG
heic_to_jpg -f input.heic -o output.jpg

# Extract image metadata
extract_img_metadata input.jpg -s  # -s saves to file
```

### 📄 PDF Management
```bash
# Merge multiple PDFs
merge_pdf -f file1.pdf file2.pdf file3.pdf -o merged.pdf

# Split PDF into individual pages
split_pdf input.pdf

# Split PDF into specific number of parts
split_pdf input.pdf -p 3

# Convert PDF to PNG images
pdf_to_png input.pdf -z  # -z creates zip archive

# Convert PDF to DOCX
pdf_to_doc input.pdf output.docx
```

### 📊 Document Processing
```bash
# Convert CSV to Excel
csv_to_excel data.csv output.xlsx

# Convert Excel to CSV
excel_to_csv data.xlsx output.csv

# Convert CSV to JSON
csv_to_json data.csv output.json

# Convert JSON to CSV
json_to_csv data.json output.csv
```

### 🎵 Audio/Video Processing
```bash
# Extract audio from video
extract_audio_from_video input.mp4 output.mp3
```

### 🔧 Advanced Options
Most tools support verbose logging:
```bash
pdf_to_png input.pdf -v  # Enable verbose logging
```

## 🖥️ GUI Application

For users who prefer a graphical interface, check the `gui` directory for desktop applications:
```bash
cd gui
python pdf_to_docx_gui.py
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=localutilitybox --cov-report=html

# Run specific test categories
pytest tests/test_image_processing.py
pytest tests/test_file_management.py
```

## 📚 Documentation

- **API Documentation**: Available in the `docs/` directory
- **Examples**: Check the `examples/` directory for usage examples
- **Contributing**: See `CONTRIBUTING.md` for development guidelines 
