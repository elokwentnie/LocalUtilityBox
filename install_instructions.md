# LocalUtilityBox Installation Guide

## 🚀 Quick Install (Recommended)

### From PyPI (when published)
```bash
pip install localutilitybox
```

### From GitHub (latest version)
```bash
pip install git+https://github.com/elokwentnie/localutilitybox.git
```

### From local source
```bash
git clone https://github.com/elokwentnie/localutilitybox.git
cd localutilitybox
pip install .
```

## 📦 Alternative Installation Methods

### 1. Using pipx (Isolated Installation)
```bash
# Install pipx if you don't have it
brew install pipx  # macOS
# or
python -m pip install pipx  # Other systems

# Install LocalUtilityBox
pipx install localutilitybox
```

### 2. Using conda (if available)
```bash
conda install -c conda-forge localutilitybox
```

### 3. Direct wheel installation
```bash
# Download the wheel file and install
pip install localutilitybox-0.2.0-py3-none-any.whl
```

## ✅ Verify Installation

After installation, test that the tools work:

```bash
# Test image conversion
png_to_jpg --help

# Test PDF processing
pdf_to_png --help

# Test document conversion
csv_to_excel --help
```

## 🔧 Development Installation

For developers who want to modify the code:

```bash
git clone https://github.com/elokwentnie/localutilitybox.git
cd localutilitybox
pip install -e .
```

## 🐍 Python Version Requirements

- Python 3.8 or higher
- pip package manager

## 🛠️ System Dependencies

Some tools may require additional system libraries:

### macOS
```bash
# For PDF processing
brew install poppler

# For image processing
brew install imagemagick
```

### Ubuntu/Debian
```bash
# For PDF processing
sudo apt-get install poppler-utils

# For image processing
sudo apt-get install imagemagick
```

### Windows
- Install poppler for Windows
- Install ImageMagick for Windows

## 🚨 Troubleshooting

### Command not found
If you get "command not found" errors:
1. Make sure pip installed to a directory in your PATH
2. Try: `python -m localutilitybox.png_to_jpg --help`

### Permission errors
If you get permission errors:
1. Use `pip install --user localutilitybox`
2. Or use a virtual environment: `python -m venv venv && source venv/bin/activate`

### Import errors
If you get import errors:
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.8+)
