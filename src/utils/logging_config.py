"""
Logging configuration for LocalUtilityBox.

This module provides centralized logging configuration for all LocalUtilityBox modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Setup logging configuration for LocalUtilityBox.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file to write logs to
        format_string: Custom format string for log messages
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=format_string,
        handlers=_create_handlers(log_file)
    )
    
    # Set specific loggers
    _configure_module_loggers()


def _create_handlers(log_file: Optional[Path] = None) -> list:
    """Create logging handlers."""
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    return handlers


def _configure_module_loggers() -> None:
    """Configure specific module loggers."""
    # Reduce verbosity for external libraries
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('pdf2image').setLevel(logging.WARNING)
    logging.getLogger('PyPDF2').setLevel(logging.WARNING)
    logging.getLogger('pandas').setLevel(logging.WARNING)
    logging.getLogger('opencv-python').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """
    Change the logging level at runtime.
    
    Args:
        level: New logging level
    """
    logging.getLogger().setLevel(getattr(logging, level.upper(), logging.INFO))
