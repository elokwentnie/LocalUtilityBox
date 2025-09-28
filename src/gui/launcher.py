#!/usr/bin/env python3
"""
GUI Launcher for LocalUtilityBox.

This script launches the main GUI application with proper error handling
and system requirements checking.
"""

import sys
import os
import tkinter as tk
from pathlib import Path

def check_requirements():
    """Check if all requirements are met for GUI."""
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            print("Error: Python 3.8 or higher is required for GUI.")
            return False
            
        # Check if tkinter is available
        try:
            import tkinter
        except ImportError:
            print("Error: tkinter is not available. Please install python3-tk.")
            return False
            
        # Check if required modules are available
        try:
            from PIL import Image
        except ImportError:
            print("Error: Pillow is not installed. Please run: pip install Pillow")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error checking requirements: {e}")
        return False

def main():
    """Main entry point for GUI launcher."""
    print("🚀 Starting LocalUtilityBox GUI...")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing dependencies.")
        print("\nTo install all dependencies, run:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    try:
        # Add src to path
        src_path = Path(__file__).parent.parent
        sys.path.insert(0, str(src_path))
        
        # Import and run the main GUI
        from gui.main_app import main as run_gui
        run_gui()
        
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("Please make sure you're running from the correct directory.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
