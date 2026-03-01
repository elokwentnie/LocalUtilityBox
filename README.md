# LocalUtilityBox

**Don't waste your time searching for web solutions -- do it in your terminal.**

LocalUtilityBox is a privacy-first suite of file-processing utilities that runs
entirely on your machine. No uploads, no third-party servers, no subscriptions.
Use it from the command line **or** through the modern desktop GUI.

## Features

- **Image Processing** -- convert between WebP, JPG, PNG, TIFF and HEIC; resize
  and compress; remove backgrounds; convert to greyscale; split long PNGs into
  multi-page PDFs; extract EXIF metadata; OCR text from images; generate QR codes.
- **PDF Management** -- merge, split, compress, rotate/reorder and watermark PDFs;
  convert pages to PNG/JPG.
- **Document Conversion** -- DOC/DOCX to PDF and back.
- **Data Format Conversion** -- CSV, Excel and JSON, any direction.
- **Video / Audio** -- extract audio tracks from video files (MP3, WAV, AAC,
  OGG, FLAC, M4A); convert video clips to animated GIFs.
- **Desktop GUI** -- a modern sidebar-based interface with dark/light theme
  support, drag-and-drop file input, and output directory selection, built with
  customtkinter.
- **CLI** -- every tool is also available as a standalone terminal command. Run
  `localutilitybox` (or `lub`) to list them all.

## Requirements

- Python 3.9+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (only for `extract_text_from_img`)
- [Poppler](https://poppler.freedesktop.org/) (only for `pdf_to_png` / `pdf_to_jpg`)
- [LibreOffice](https://www.libreoffice.org/) **or** Microsoft Word (only for `doc_to_pdf`)

## Installation

### pipx (recommended)

[pipx](https://pipx.pypa.io/) installs Python CLI apps in isolated environments
while making the commands available globally.

```bash
brew install pipx          # macOS
# or: sudo apt install pipx  # Debian/Ubuntu
pipx ensurepath

pipx install git+https://github.com/elokwentnie/LocalUtilityBox.git
```

### Optional extras

```bash
# QR code generation
pipx inject localutilitybox 'qrcode[pil]'

# AI background removal (large download)
pipx inject localutilitybox 'rembg[cpu]'
```

### From source

```bash
git clone https://github.com/elokwentnie/LocalUtilityBox.git
cd LocalUtilityBox

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install .

# Optional extras:
pip install 'qrcode[pil]'   # QR code generation
pip install 'rembg[cpu]'    # AI background removal
```

### Verify

```bash
lub                     # list all available tools
heic_to_jpg --help      # test a CLI command
lub-gui                 # launch the GUI
```

### GUI prerequisites

The GUI depends on **tkinter** (required by customtkinter). Install it if your
Python distribution does not bundle it:

```bash
# macOS (Homebrew)
brew install python-tk@3.13

# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Usage

### Desktop GUI

```bash
localutilitybox-gui   # or: lub-gui
```

The GUI provides a sidebar with every tool organised by category. Select a tool,
fill in the inputs, and click the action button. A status bar shows real-time
progress and the output file location. Switch between System, Light and Dark
themes from the bottom of the sidebar.

### Command Line

Every tool ships as its own command. Run `localutilitybox` (or `lub`) to see the
full list. A few examples:

```bash
# Image conversion
webp_to_jpg image.webp -o image.jpg -b white
heic_to_jpg -f photo1.heic photo2.heic
heic_to_jpg -d /path/to/heic/files

# PDF management
merge_pdf -f a.pdf b.pdf c.pdf -o merged.pdf
split_pdf input.pdf -p 3
compress_pdf input.pdf
rotate_pdf input.pdf --rotation 90
add_watermark input.pdf -w watermark.pdf -p 0 1 2

# QR code (requires qrcode[pil])
generate_qr "https://example.com" -o qr.png

# Document conversion
doc_to_pdf report.docx -o report.pdf
pdf_to_doc report.pdf -o report.docx

# Data formats
csv_to_excel data.csv -o data.xlsx
csv_to_json data.csv -o data.json

# Long PNG to paginated PDF
long_png_to_pdf screenshot.png -p a4 --overlap 20

# Video / audio
extract_audio_from_video video.mp4 -f mp3 -o audio.mp3
video_to_gif clip.mp4 --fps 15 --width 480
```

Run any command with `--help` for full usage details.

## Docker

```bash
docker build -t localutilitybox .
docker run -it -v "$(pwd)/files:/data" localutilitybox
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE) -- see the LICENSE file for details.
