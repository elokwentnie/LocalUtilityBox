"""
LocalUtilityBox - File Processing Utilities

A comprehensive toolkit for image, PDF, and document processing.
All operations are performed locally without sharing files on external servers.
"""

__version__ = "0.2.0"
__author__ = "LocalUtilityBox Team"
__description__ = "Don't waste your time searching for web solutions, do it in your terminal."

# Import main utilities
from .utils.error_handling import (
    LocalUtilityBoxError,
    FileValidationError,
    ConversionError,
    ConfigurationError
)
from .utils.logging_config import setup_logging, get_logger

__all__ = [
    "LocalUtilityBoxError",
    "FileValidationError", 
    "ConversionError",
    "ConfigurationError",
    "setup_logging",
    "get_logger"
]