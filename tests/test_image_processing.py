"""
Tests for image processing modules.
"""

import pytest
from pathlib import Path
from PIL import Image
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from image_processing.webp_to_png import webp_to_png
from image_processing.jpg_to_png import jpg_to_png
from image_processing.png_to_jpg import png_to_jpg
from image_processing.extract_img_metadata import extract_img_metadata


class TestWebPToPNG:
    """Test WebP to PNG conversion."""
    
    def test_webp_to_png_success(self, sample_webp_image, temp_dir):
        """Test successful WebP to PNG conversion."""
        output_file = temp_dir / "converted.png"
        webp_to_png(sample_webp_image, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.png'
        
        # Verify the image can be opened
        with Image.open(output_file) as img:
            assert img.format == 'PNG'
    
    def test_webp_to_png_default_output(self, sample_webp_image):
        """Test WebP to PNG conversion with default output path."""
        webp_to_png(sample_webp_image)
        
        expected_output = sample_webp_image.with_suffix('.png')
        assert expected_output.exists()
    
    def test_webp_to_png_invalid_input(self, invalid_file):
        """Test WebP to PNG conversion with invalid input."""
        with pytest.raises(Exception):  # Should raise an exception
            webp_to_png(invalid_file)


class TestJPGToPNG:
    """Test JPG to PNG conversion."""
    
    def test_jpg_to_png_success(self, sample_image, temp_dir):
        """Test successful JPG to PNG conversion."""
        output_file = temp_dir / "converted.png"
        jpg_to_png(sample_image, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.png'
        
        # Verify the image can be opened
        with Image.open(output_file) as img:
            assert img.format == 'PNG'


class TestPNGToJPG:
    """Test PNG to JPG conversion."""
    
    def test_png_to_jpg_success(self, sample_png_image, temp_dir):
        """Test successful PNG to JPG conversion."""
        output_file = temp_dir / "converted.jpg"
        png_to_jpg(sample_png_image, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.jpg'
        
        # Verify the image can be opened
        with Image.open(output_file) as img:
            assert img.format == 'JPEG'


class TestExtractImageMetadata:
    """Test image metadata extraction."""
    
    def test_extract_metadata_success(self, sample_image):
        """Test successful metadata extraction."""
        # This should not raise an exception
        extract_img_metadata(sample_image)
    
    def test_extract_metadata_save_to_file(self, sample_image, temp_dir):
        """Test metadata extraction with save option."""
        extract_img_metadata(sample_image, save_flag=True)
        
        expected_output = sample_image.with_name(f"{sample_image.stem}_metadata.txt")
        assert expected_output.exists()
        
        # Check that the file contains metadata
        content = expected_output.read_text()
        assert "Image Name" in content
        assert "Image Size" in content
    
    def test_extract_metadata_invalid_file(self, invalid_file):
        """Test metadata extraction with invalid file."""
        with pytest.raises(Exception):  # Should raise an exception
            extract_img_metadata(invalid_file)
