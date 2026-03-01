"""Shared fixtures for LocalUtilityBox tests."""
import pytest
from PIL import Image


@pytest.fixture
def tmp_image(tmp_path):
    """Create a small test JPEG image and return its path."""
    p = tmp_path / "test.jpg"
    Image.new("RGB", (100, 80), color="red").save(p, "JPEG")
    return p


@pytest.fixture
def tmp_png(tmp_path):
    """Create a small test PNG image and return its path."""
    p = tmp_path / "test.png"
    Image.new("RGBA", (100, 80), color=(0, 128, 255, 255)).save(p, "PNG")
    return p


@pytest.fixture
def tmp_webp(tmp_path):
    """Create a small test WebP image and return its path."""
    p = tmp_path / "test.webp"
    Image.new("RGB", (100, 80), color="green").save(p, "WebP")
    return p


@pytest.fixture
def tmp_pdf(tmp_path):
    """Create a minimal valid PDF and return its path."""
    from PyPDF2 import PdfWriter

    p = tmp_path / "test.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)
    with open(p, "wb") as f:
        writer.write(f)
    return p
