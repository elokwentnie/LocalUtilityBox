"""
Tests for utility modules.
"""

import pytest
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.error_handling import (
    FileValidationError,
    ConversionError,
    validate_file_exists,
    validate_directory_exists,
    handle_error,
    validate_file_size
)
from utils.logging_config import setup_logging, get_logger


class TestErrorHandling:
    """Test error handling utilities."""
    
    def test_validate_file_exists_success(self, sample_image):
        """Test successful file validation."""
        validate_file_exists(sample_image, '.jpg')
        # Should not raise any exception
    
    def test_validate_file_exists_file_not_found(self, non_existent_file):
        """Test file validation with non-existent file."""
        with pytest.raises(FileValidationError, match="does not exist"):
            validate_file_exists(non_existent_file)
    
    def test_validate_file_exists_wrong_extension(self, sample_image):
        """Test file validation with wrong extension."""
        with pytest.raises(FileValidationError, match="is not a .pdf file"):
            validate_file_exists(sample_image, '.pdf')
    
    def test_validate_directory_exists_success(self, temp_dir):
        """Test successful directory validation."""
        validate_directory_exists(temp_dir)
        # Should not raise any exception
    
    def test_validate_directory_exists_not_found(self, non_existent_file):
        """Test directory validation with non-existent directory."""
        with pytest.raises(FileValidationError, match="does not exist"):
            validate_directory_exists(non_existent_file)
    
    def test_validate_file_size_success(self, sample_image):
        """Test file size validation with valid size."""
        validate_file_size(sample_image, max_size_mb=1.0)
        # Should not raise any exception
    
    def test_validate_file_size_too_large(self, sample_image):
        """Test file size validation with file too large."""
        with pytest.raises(FileValidationError, match="too large"):
            validate_file_size(sample_image, max_size_mb=0.001)  # Very small limit
    
    def test_validate_file_size_no_limit(self, sample_image):
        """Test file size validation with no limit."""
        validate_file_size(sample_image)
        # Should not raise any exception


class TestLoggingConfig:
    """Test logging configuration."""
    
    def test_setup_logging(self):
        """Test logging setup."""
        setup_logging(level="DEBUG")
        logger = get_logger("test_logger")
        assert logger.level <= 10  # DEBUG level
    
    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test_module")
        assert logger.name == "test_module"
    
    def test_setup_logging_with_file(self, temp_dir):
        """Test logging setup with log file."""
        log_file = temp_dir / "test.log"
        setup_logging(level="INFO", log_file=log_file)
        logger = get_logger("test_logger")
        logger.info("Test message")
        
        # Check if log file was created and contains the message
        assert log_file.exists()
        assert "Test message" in log_file.read_text()
