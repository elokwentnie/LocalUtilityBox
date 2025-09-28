#!/usr/bin/env python3
"""
Basic usage examples for LocalUtilityBox.

This script demonstrates how to use LocalUtilityBox programmatically.
"""

import tempfile
from pathlib import Path
from PIL import Image
import pandas as pd

# Import LocalUtilityBox modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.logging_config import setup_logging
from image_processing.webp_to_png import webp_to_png
from file_management.csv_to_excel import csv_to_excel
from file_management.merge_pdf import merge_pdf


def create_sample_files():
    """Create sample files for demonstration."""
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create a sample WebP image
    webp_path = temp_dir / "sample.webp"
    img = Image.new('RGB', (100, 100), color='blue')
    img.save(webp_path, 'WEBP')
    
    # Create a sample CSV file
    csv_path = temp_dir / "sample.csv"
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    return temp_dir, webp_path, csv_path


def demonstrate_image_conversion():
    """Demonstrate image conversion functionality."""
    print("🖼️  Image Conversion Demo")
    print("=" * 40)
    
    temp_dir, webp_path, _ = create_sample_files()
    
    try:
        # Convert WebP to PNG
        png_path = temp_dir / "converted.png"
        webp_to_png(webp_path, png_path)
        print(f"✅ Converted {webp_path.name} to {png_path.name}")
        
        # Verify the conversion
        with Image.open(png_path) as img:
            print(f"   Image size: {img.size}")
            print(f"   Image format: {img.format}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def demonstrate_document_conversion():
    """Demonstrate document conversion functionality."""
    print("\n📄 Document Conversion Demo")
    print("=" * 40)
    
    temp_dir, _, csv_path = create_sample_files()
    
    try:
        # Convert CSV to Excel
        excel_path = temp_dir / "converted.xlsx"
        csv_to_excel(csv_path, excel_path)
        print(f"✅ Converted {csv_path.name} to {excel_path.name}")
        
        # Verify the conversion
        df = pd.read_excel(excel_path)
        print(f"   Records: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


def demonstrate_logging():
    """Demonstrate logging functionality."""
    print("\n📝 Logging Demo")
    print("=" * 40)
    
    # Setup logging
    setup_logging(level="DEBUG")
    
    from localutilitybox.utils.logging_config import get_logger
    logger = get_logger("demo")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("✅ Logging demonstration complete")


def main():
    """Main demonstration function."""
    print("🎯 LocalUtilityBox Basic Usage Examples")
    print("=" * 50)
    
    # Demonstrate logging
    demonstrate_logging()
    
    # Demonstrate image conversion
    demonstrate_image_conversion()
    
    # Demonstrate document conversion
    demonstrate_document_conversion()
    
    print("\n🎉 All demonstrations completed!")
    print("\nFor more examples, check the documentation or run individual CLI tools.")


if __name__ == "__main__":
    main()
