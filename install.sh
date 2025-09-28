#!/bin/bash
# LocalUtilityBox Installation Script

set -e

echo "🚀 LocalUtilityBox Installation Script"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Installation options
echo ""
echo "Choose installation method:"
echo "1) Install from PyPI (recommended)"
echo "2) Install from GitHub (latest version)"
echo "3) Install from local wheel file"
echo "4) Install in development mode"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "📦 Installing from PyPI..."
        pip3 install localutilitybox
        ;;
    2)
        echo "📦 Installing from GitHub..."
        pip3 install git+https://github.com/elokwentnie/localutilitybox.git
        ;;
    3)
        echo "📦 Installing from local wheel..."
        if [ ! -f "dist/localutilitybox-0.2.0-py3-none-any.whl" ]; then
            echo "❌ Wheel file not found. Please run 'python3 -m build' first."
            exit 1
        fi
        pip3 install dist/localutilitybox-0.2.0-py3-none-any.whl
        ;;
    4)
        echo "📦 Installing in development mode..."
        pip3 install -e .
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

# Verify installation
echo ""
echo "🔍 Verifying installation..."

if command -v png_to_jpg &> /dev/null; then
    echo "✅ png_to_jpg command found"
else
    echo "❌ png_to_jpg command not found"
    exit 1
fi

if command -v pdf_to_png &> /dev/null; then
    echo "✅ pdf_to_png command found"
else
    echo "❌ pdf_to_png command not found"
    exit 1
fi

# Test help commands
echo ""
echo "🧪 Testing commands..."
png_to_jpg --help > /dev/null 2>&1 && echo "✅ png_to_jpg help works" || echo "❌ png_to_jpg help failed"
pdf_to_png --help > /dev/null 2>&1 && echo "✅ pdf_to_png help works" || echo "❌ pdf_to_png help failed"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Usage examples:"
echo "  png_to_jpg input.png output.jpg"
echo "  pdf_to_png input.pdf -v"
echo "  csv_to_excel data.csv output.xlsx"
echo ""
echo "For more information, visit: https://github.com/elokwentnie/localutilitybox"
