"""
Base converter classes for LocalUtilityBox.

This module provides base classes and common functionality for all file converters.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Any, Dict
import argparse
import logging

from .error_handling import (
    FileValidationError, 
    ConversionError, 
    validate_file_exists,
    safe_operation
)
from .logging_config import get_logger


class BaseConverter(ABC):
    """Base class for all file converters."""
    
    def __init__(
        self, 
        input_file: Path, 
        output_file: Optional[Path] = None,
        **kwargs
    ):
        """
        Initialize the converter.
        
        Args:
            input_file: Path to input file
            output_file: Path to output file (optional)
            **kwargs: Additional converter-specific options
        """
        self.input_file = input_file
        self.output_file = output_file or self._generate_output_path()
        self.options = kwargs
        self.logger = get_logger(self.__class__.__name__)
        
        # Validate input
        self._validate_input()
    
    @abstractmethod
    def convert(self) -> None:
        """Perform the conversion."""
        pass
    
    @abstractmethod
    def _generate_output_path(self) -> Path:
        """Generate default output path based on input file."""
        pass
    
    @property
    @abstractmethod
    def expected_extension(self) -> str:
        """Expected input file extension."""
        pass
    
    def _validate_input(self) -> None:
        """Validate input file."""
        validate_file_exists(self.input_file, self.expected_extension)
        self.logger.info(f"Validated input file: {self.input_file}")
    
    def _validate_output_directory(self) -> None:
        """Ensure output directory exists."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
    
    def execute(self) -> None:
        """Execute the conversion with error handling."""
        try:
            self._validate_output_directory()
            self.convert()
            self.logger.info(f"Successfully converted {self.input_file} to {self.output_file}")
        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            raise ConversionError(f"Failed to convert {self.input_file}: {e}") from e


class ImageConverter(BaseConverter):
    """Base class for image converters."""
    
    @property
    def expected_extension(self) -> str:
        """Image files can have various extensions."""
        return ".jpg"  # Default, should be overridden
    
    def _generate_output_path(self) -> Path:
        """Generate output path by changing extension."""
        return self.input_file.with_suffix(self.output_extension)
    
    @property
    @abstractmethod
    def output_extension(self) -> str:
        """Output file extension."""
        pass


class PDFConverter(BaseConverter):
    """Base class for PDF converters."""
    
    @property
    def expected_extension(self) -> str:
        return ".pdf"
    
    def _generate_output_path(self) -> Path:
        """Generate output path by changing extension."""
        return self.input_file.with_suffix(self.output_extension)
    
    @property
    @abstractmethod
    def output_extension(self) -> str:
        """Output file extension."""
        pass


class DocumentConverter(BaseConverter):
    """Base class for document converters."""
    
    @property
    def expected_extension(self) -> str:
        return ".csv"  # Default, should be overridden
    
    def _generate_output_path(self) -> Path:
        """Generate output path by changing extension."""
        return self.input_file.with_suffix(self.output_extension)
    
    @property
    @abstractmethod
    def output_extension(self) -> str:
        """Output file extension."""
        pass


class BaseCLI:
    """Base class for CLI applications."""
    
    def __init__(self, description: str):
        self.description = description
        self.parser = argparse.ArgumentParser(description=description)
        self.logger = get_logger(self.__class__.__name__)
        self._setup_arguments()
    
    def _setup_arguments(self) -> None:
        """Setup common CLI arguments. Override in subclasses."""
        self.parser.add_argument(
            "input_file", 
            type=Path, 
            help="Path to the input file"
        )
        self.parser.add_argument(
            "-o", "--output", 
            type=Path, 
            default=None,
            help="Path to the output file (optional)"
        )
        self.parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enable verbose logging"
        )
    
    def parse_args(self) -> argparse.Namespace:
        """Parse command line arguments."""
        return self.parser.parse_args()
    
    def run(self) -> None:
        """Run the CLI application."""
        args = self.parse_args()
        
        # Setup logging
        if args.verbose:
            from .logging_config import setup_logging
            setup_logging(level="DEBUG")
        
        # Execute the main functionality
        self._execute(args)
    
    @abstractmethod
    def _execute(self, args: argparse.Namespace) -> None:
        """Execute the main functionality. Override in subclasses."""
        pass


def create_parser(description: str) -> argparse.ArgumentParser:
    """
    Create a standardized argument parser.
    
    Args:
        description: Description of the CLI tool
        
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(description=description)
    
    # Common arguments
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level"
    )
    
    return parser
