"""
Error handling utilities for LocalUtilityBox.

This module provides standardized error handling, validation, and logging
for all LocalUtilityBox operations.
"""

import sys
import logging
from pathlib import Path
from typing import NoReturn, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)


class LocalUtilityBoxError(Exception):
    """Base exception for LocalUtilityBox operations."""
    pass


class FileValidationError(LocalUtilityBoxError):
    """Raised when file validation fails."""
    pass


class ConversionError(LocalUtilityBoxError):
    """Raised when file conversion fails."""
    pass


class ConfigurationError(LocalUtilityBoxError):
    """Raised when configuration is invalid."""
    pass


def validate_file_exists(file_path: Path, expected_extension: Optional[str] = None) -> None:
    """
    Validate that a file exists and has the correct extension.
    
    Args:
        file_path: Path to the file to validate
        expected_extension: Expected file extension (e.g., '.pdf', '.jpg')
        
    Raises:
        FileValidationError: If file doesn't exist or has wrong extension
    """
    if not file_path.is_file():
        raise FileValidationError(f"File '{file_path}' does not exist or is not a file")
    
    if expected_extension and file_path.suffix.lower() != expected_extension.lower():
        raise FileValidationError(f"File '{file_path}' is not a {expected_extension} file")


def validate_directory_exists(directory_path: Path) -> None:
    """
    Validate that a directory exists.
    
    Args:
        directory_path: Path to the directory to validate
        
    Raises:
        FileValidationError: If directory doesn't exist
    """
    if not directory_path.is_dir():
        raise FileValidationError(f"Directory '{directory_path}' does not exist or is not a directory")


def handle_error(error: Exception, exit_code: int = 1, log_level: str = "ERROR") -> NoReturn:
    """
    Standardized error handling with logging and exit.
    
    Args:
        error: The exception to handle
        exit_code: Exit code to use (default: 1)
        log_level: Log level for the error message
    """
    level = getattr(logging, log_level.upper(), logging.ERROR)
    logger.log(level, f"Error: {error}")
    print(f"Error: {error}")
    sys.exit(exit_code)


def handle_conversion_error(error: Exception, input_file: Path, output_file: Optional[Path] = None) -> NoReturn:
    """
    Handle conversion-specific errors with detailed logging.
    
    Args:
        error: The conversion error
        input_file: Input file that caused the error
        output_file: Output file (if applicable)
    """
    error_msg = f"Failed to convert '{input_file}'"
    if output_file:
        error_msg += f" to '{output_file}'"
    error_msg += f": {error}"
    
    logger.error(error_msg)
    print(f"Error: {error_msg}")
    sys.exit(1)


def validate_file_size(file_path: Path, max_size_mb: Optional[float] = None) -> None:
    """
    Validate file size is within limits.
    
    Args:
        file_path: Path to the file to validate
        max_size_mb: Maximum file size in MB
        
    Raises:
        FileValidationError: If file is too large
    """
    if max_size_mb is None:
        return
        
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise FileValidationError(
            f"File '{file_path}' is too large ({file_size_mb:.2f}MB). "
            f"Maximum allowed size is {max_size_mb}MB"
        )


def safe_operation(operation_name: str, operation_func, *args, **kwargs):
    """
    Safely execute an operation with error handling.
    
    Args:
        operation_name: Name of the operation for logging
        operation_func: Function to execute
        *args: Arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        Result of the operation
        
    Raises:
        LocalUtilityBoxError: If operation fails
    """
    try:
        logger.info(f"Starting {operation_name}")
        result = operation_func(*args, **kwargs)
        logger.info(f"Completed {operation_name} successfully")
        return result
    except Exception as e:
        logger.error(f"Failed {operation_name}: {e}")
        raise LocalUtilityBoxError(f"{operation_name} failed: {e}") from e
