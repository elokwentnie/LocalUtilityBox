"""Utility functions for GUI."""
import threading
from pathlib import Path
from typing import Callable, Optional


def run_in_thread(func: Callable, callback: Optional[Callable] = None, *args, **kwargs):
    """Run a function in a separate thread to prevent UI freezing."""
    def wrapper():
        try:
            result = func(*args, **kwargs)
            if callback:
                callback(result, None)
        except Exception as e:
            if callback:
                callback(None, e)
    
    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    return thread


def validate_file_path(file_path: str, extensions: list) -> tuple[bool, Optional[str]]:
    """Validate file path and extension."""
    if not file_path:
        return False, "Please select a file."
    
    path = Path(file_path)
    if not path.exists():
        return False, f"File does not exist: {file_path}"
    
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"
    
    if extensions and path.suffix.lower() not in [ext.lower() for ext in extensions]:
        return False, f"File must have one of these extensions: {', '.join(extensions)}"
    
    return True, None


def validate_directory_path(dir_path: str) -> tuple[bool, Optional[str]]:
    """Validate directory path."""
    if not dir_path:
        return False, "Please select a directory."
    
    path = Path(dir_path)
    if not path.exists():
        return False, f"Directory does not exist: {dir_path}"
    
    if not path.is_dir():
        return False, f"Path is not a directory: {dir_path}"
    
    return True, None
