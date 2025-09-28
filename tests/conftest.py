"""
Pytest configuration and fixtures for LocalUtilityBox tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import pandas as pd
from PyPDF2 import PdfWriter
import io


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_image(temp_dir):
    """Create a sample image file for testing."""
    image_path = temp_dir / "test_image.jpg"
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img.save(image_path, 'JPEG')
    return image_path


@pytest.fixture
def sample_png_image(temp_dir):
    """Create a sample PNG image file for testing."""
    image_path = temp_dir / "test_image.png"
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
    img.save(image_path, 'PNG')
    return image_path


@pytest.fixture
def sample_webp_image(temp_dir):
    """Create a sample WebP image file for testing."""
    image_path = temp_dir / "test_image.webp"
    img = Image.new('RGB', (100, 100), color='blue')
    img.save(image_path, 'WEBP')
    return image_path


@pytest.fixture
def sample_pdf(temp_dir):
    """Create a sample PDF file for testing."""
    pdf_path = temp_dir / "test_document.pdf"
    
    # Create a simple PDF using PyPDF2
    writer = PdfWriter()
    
    # Add a blank page (PyPDF2 doesn't have easy page creation, so we'll create a minimal PDF)
    # For testing purposes, we'll create a simple text-based PDF
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Test PDF Document")
    c.showPage()
    c.save()
    
    # Write the PDF content
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    return pdf_path


@pytest.fixture
def sample_csv(temp_dir):
    """Create a sample CSV file for testing."""
    csv_path = temp_dir / "test_data.csv"
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_excel(temp_dir):
    """Create a sample Excel file for testing."""
    excel_path = temp_dir / "test_data.xlsx"
    data = {
        'Product': ['Widget A', 'Widget B', 'Widget C'],
        'Price': [10.99, 15.50, 8.75],
        'Quantity': [100, 50, 200]
    }
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    return excel_path


@pytest.fixture
def sample_json(temp_dir):
    """Create a sample JSON file for testing."""
    json_path = temp_dir / "test_data.json"
    import json
    data = [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200},
        {"id": 3, "name": "Item 3", "value": 300}
    ]
    with open(json_path, 'w') as f:
        json.dump(data, f)
    return json_path


@pytest.fixture
def invalid_file(temp_dir):
    """Create an invalid file for testing error handling."""
    invalid_path = temp_dir / "invalid_file.txt"
    invalid_path.write_text("This is not a valid image or PDF file")
    return invalid_path


@pytest.fixture
def non_existent_file(temp_dir):
    """Return a path to a non-existent file."""
    return temp_dir / "non_existent_file.jpg"


# Test data for various file formats
@pytest.fixture
def test_data():
    """Provide test data for various operations."""
    return {
        'image_sizes': [(100, 100), (200, 150), (50, 75)],
        'colors': ['red', 'green', 'blue', 'white', 'black'],
        'csv_columns': ['Name', 'Age', 'City', 'Country'],
        'pdf_pages': 3,
        'json_records': 5
    }
