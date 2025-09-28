#!/usr/bin/env python3
"""
Main GUI application for LocalUtilityBox.

This is the primary graphical interface that provides access to all
LocalUtilityBox tools through a modern, user-friendly interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import queue
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from utils.logging_config import setup_logging, get_logger
from utils.error_handling import LocalUtilityBoxError

# Import GUI modules
from .image_processing_gui import ImageProcessingGUI
from .pdf_management_gui import PDFManagementGUI
from .document_conversion_gui import DocumentConversionGUI
from .audio_video_gui import AudioVideoGUI


class LocalUtilityBoxGUI:
    """Main GUI application for LocalUtilityBox."""
    
    def __init__(self):
        """Initialize the main GUI application."""
        self.root = tk.Tk()
        self.logger = get_logger(__name__)
        self.setup_logging()
        
        # Configure main window
        self.setup_main_window()
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize sub-GUIs
        self.image_gui = None
        self.pdf_gui = None
        self.doc_gui = None
        self.audio_gui = None
        
        # Status tracking
        self.current_operation = None
        self.operation_queue = queue.Queue()
        
    def setup_logging(self):
        """Setup logging for GUI application."""
        setup_logging(level="INFO")
        self.logger.info("LocalUtilityBox GUI started")
        
    def setup_main_window(self):
        """Configure the main window."""
        self.root.title("LocalUtilityBox - File Processing Suite")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Info.TLabel', font=('Arial', 10))
        
        # Center window
        self.center_window()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="LocalUtilityBox", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for different tool categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create tabs
        self.create_image_processing_tab()
        self.create_pdf_management_tab()
        self.create_document_conversion_tab()
        self.create_audio_video_tab()
        self.create_about_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_image_processing_tab(self):
        """Create the image processing tab."""
        image_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(image_frame, text="🖼️ Image Processing")
        
        # Initialize image processing GUI
        self.image_gui = ImageProcessingGUI(image_frame, self)
        
    def create_pdf_management_tab(self):
        """Create the PDF management tab."""
        pdf_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(pdf_frame, text="📄 PDF Management")
        
        # Initialize PDF management GUI
        self.pdf_gui = PDFManagementGUI(pdf_frame, self)
        
    def create_document_conversion_tab(self):
        """Create the document conversion tab."""
        doc_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(doc_frame, text="📊 Document Conversion")
        
        # Initialize document conversion GUI
        self.doc_gui = DocumentConversionGUI(doc_frame, self)
        
    def create_audio_video_tab(self):
        """Create the audio/video processing tab."""
        audio_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(audio_frame, text="🎵 Audio/Video")
        
        # Initialize audio/video GUI
        self.audio_gui = AudioVideoGUI(audio_frame, self)
        
    def create_about_tab(self):
        """Create the about tab."""
        about_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(about_frame, text="ℹ️ About")
        
        # About content
        about_text = """
LocalUtilityBox - File Processing Suite
=====================================

A comprehensive toolkit for image, PDF, and document processing.
All operations are performed locally without sharing files on external servers.

Features:
• Image format conversion (PNG, JPG, WebP, HEIC, TIFF)
• PDF management (merge, split, convert to images)
• Document conversion (CSV, Excel, JSON)
• Audio/video processing
• Batch processing capabilities
• Drag-and-drop support
• Progress tracking

Version: 0.2.0
Author: LocalUtilityBox Team

For command-line usage:
• png_to_jpg input.png output.jpg
• pdf_to_png input.pdf -v
• csv_to_excel data.csv output.xlsx

For more information, visit:
https://github.com/elokwentnie/localutilitybox
        """
        
        about_label = ttk.Label(
            about_frame, 
            text=about_text, 
            style='Info.TLabel',
            justify='left'
        )
        about_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        about_frame.columnconfigure(0, weight=1)
        about_frame.rowconfigure(0, weight=1)
        
    def create_status_bar(self, parent):
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready", style='Info.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame, 
            mode='indeterminate',
            length=200
        )
        self.progress.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        
        # Configure grid weights
        status_frame.columnconfigure(0, weight=1)
        
    def update_status(self, message: str, show_progress: bool = False):
        """Update the status bar."""
        self.status_label.config(text=message)
        if show_progress:
            self.progress.start()
        else:
            self.progress.stop()
        self.root.update_idletasks()
        
    def show_error(self, title: str, message: str):
        """Show an error message."""
        messagebox.showerror(title, message)
        self.logger.error(f"{title}: {message}")
        
    def show_info(self, title: str, message: str):
        """Show an info message."""
        messagebox.showinfo(title, message)
        self.logger.info(f"{title}: {message}")
        
    def show_warning(self, title: str, message: str):
        """Show a warning message."""
        messagebox.showwarning(title, message)
        self.logger.warning(f"{title}: {message}")
        
    def run_operation(self, operation_func, *args, **kwargs):
        """Run an operation in a separate thread."""
        def worker():
            try:
                self.update_status("Processing...", show_progress=True)
                result = operation_func(*args, **kwargs)
                self.root.after(0, lambda: self.operation_completed(result))
            except Exception as e:
                self.root.after(0, lambda: self.operation_failed(e))
                
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def operation_completed(self, result):
        """Handle operation completion."""
        self.update_status("Operation completed successfully")
        if result:
            self.show_info("Success", "Operation completed successfully!")
            
    def operation_failed(self, error):
        """Handle operation failure."""
        self.update_status("Operation failed")
        self.show_error("Error", str(error))
        
    def on_closing(self):
        """Handle window closing."""
        self.logger.info("LocalUtilityBox GUI closing")
        self.root.destroy()
        
    def run(self):
        """Run the GUI application."""
        self.logger.info("Starting LocalUtilityBox GUI")
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    try:
        app = LocalUtilityBoxGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
