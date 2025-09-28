"""
Image Processing GUI for LocalUtilityBox.

This module provides a graphical interface for all image processing operations.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional, Dict, Any
import threading
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from image_processing.webp_to_png import webp_to_png
from image_processing.webp_to_jpg import webp_to_jpg
from image_processing.jpg_to_png import jpg_to_png
from image_processing.png_to_jpg import png_to_jpg
from image_processing.tiff_to_jpg import tiff_to_jpg
from image_processing.heic_to_jpg import heic_to_jpg
from image_processing.img_to_pdf import img_to_pdf
from image_processing.img_to_greyscale import img_to_greyscale
from image_processing.reduce_img_size import reduce_img_size
from image_processing.remove_background import remove_background
from image_processing.extract_img_metadata import extract_img_metadata
from image_processing.extract_text_from_img import extract_text_from_img


class ImageProcessingGUI:
    """GUI for image processing operations."""
    
    def __init__(self, parent, main_app):
        """Initialize the image processing GUI."""
        self.parent = parent
        self.main_app = main_app
        self.logger = main_app.logger
        
        # File lists
        self.input_files = []
        self.output_directory = None
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        self.create_file_selection_section(main_frame)
        
        # Operation selection section
        self.create_operation_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
    def create_file_selection_section(self, parent):
        """Create the file selection section."""
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Input files
        ttk.Label(file_frame, text="Input Files:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # File list with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=6, selectmode=tk.MULTIPLE)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # File selection buttons
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Add Files", command=self.add_files).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Add Folder", command=self.add_folder).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Clear All", command=self.clear_files).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected).grid(row=0, column=3)
        
        # Output directory
        ttk.Label(file_frame, text="Output Directory:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        output_frame = ttk.Frame(file_frame)
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, state='readonly')
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse", command=self.select_output_directory).grid(row=0, column=1)
        
    def create_operation_section(self, parent):
        """Create the operation selection section."""
        # Operation frame
        op_frame = ttk.LabelFrame(parent, text="Image Operations", padding="10")
        op_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Operation selection
        self.operation_var = tk.StringVar()
        
        operations = [
            ("WebP to PNG", "webp_to_png"),
            ("WebP to JPG", "webp_to_jpg"),
            ("JPG to PNG", "jpg_to_png"),
            ("PNG to JPG", "png_to_jpg"),
            ("TIFF to JPG", "tiff_to_jpg"),
            ("HEIC to JPG", "heic_to_jpg"),
            ("Images to PDF", "img_to_pdf"),
            ("Convert to Greyscale", "img_to_greyscale"),
            ("Reduce Image Size", "reduce_img_size"),
            ("Remove Background", "remove_background"),
            ("Extract Metadata", "extract_img_metadata"),
            ("Extract Text (OCR)", "extract_text_from_img")
        ]
        
        # Create radio buttons in a grid
        for i, (text, value) in enumerate(operations):
            row = i // 3
            col = i % 3
            ttk.Radiobutton(
                op_frame, 
                text=text, 
                variable=self.operation_var, 
                value=value
            ).grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
            
        # Set default selection
        self.operation_var.set("webp_to_png")
        
    def create_options_section(self, parent):
        """Create the options section."""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Quality setting
        ttk.Label(options_frame, text="Quality (1-100):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.quality_var = tk.IntVar(value=95)
        quality_scale = ttk.Scale(
            options_frame, 
            from_=1, 
            to=100, 
            variable=self.quality_var, 
            orient=tk.HORIZONTAL
        )
        quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Quality value label
        self.quality_label = ttk.Label(options_frame, text="95")
        self.quality_label.grid(row=0, column=2, padx=(10, 0), pady=(0, 5))
        
        # Update quality label when scale changes
        quality_scale.config(command=self.update_quality_label)
        
        # Size reduction percentage
        ttk.Label(options_frame, text="Size Reduction (%):").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.size_reduction_var = tk.IntVar(value=50)
        size_scale = ttk.Scale(
            options_frame, 
            from_=10, 
            to=90, 
            variable=self.size_reduction_var, 
            orient=tk.HORIZONTAL
        )
        size_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Size reduction value label
        self.size_label = ttk.Label(options_frame, text="50%")
        self.size_label.grid(row=1, column=2, padx=(10, 0), pady=(0, 5))
        
        # Update size label when scale changes
        size_scale.config(command=self.update_size_label)
        
        # Configure grid weights
        options_frame.columnconfigure(1, weight=1)
        
    def create_action_buttons(self, parent):
        """Create the action buttons."""
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Process button
        self.process_button = ttk.Button(
            button_frame, 
            text="Process Images", 
            command=self.process_images,
            style='Accent.TButton'
        )
        self.process_button.grid(row=0, column=0, padx=(0, 10))
        
        # Preview button
        ttk.Button(
            button_frame, 
            text="Preview", 
            command=self.preview_operation
        ).grid(row=0, column=1, padx=(0, 10))
        
        # Reset button
        ttk.Button(
            button_frame, 
            text="Reset", 
            command=self.reset_form
        ).grid(row=0, column=2)
        
    def create_progress_section(self, parent):
        """Create the progress section."""
        # Progress frame
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=400
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to process images")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
    def update_quality_label(self, value):
        """Update the quality label."""
        self.quality_label.config(text=str(int(float(value))))
        
    def update_size_label(self, value):
        """Update the size reduction label."""
        self.size_label.config(text=f"{int(float(value))}%")
        
    def add_files(self):
        """Add files to the list."""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.webp *.tiff *.tif *.heic *.bmp *.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("WebP files", "*.webp"),
            ("TIFF files", "*.tiff *.tif"),
            ("HEIC files", "*.heic"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select image files",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
                
    def add_folder(self):
        """Add all image files from a folder."""
        folder = filedialog.askdirectory(title="Select folder containing images")
        if folder:
            folder_path = Path(folder)
            image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.tiff', '.tif', '.heic', '.bmp', '.gif'}
            
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    if str(file_path) not in self.input_files:
                        self.input_files.append(str(file_path))
                        self.file_listbox.insert(tk.END, file_path.name)
                        
    def clear_files(self):
        """Clear all files from the list."""
        self.input_files.clear()
        self.file_listbox.delete(0, tk.END)
        
    def remove_selected(self):
        """Remove selected files from the list."""
        selected_indices = self.file_listbox.curselection()
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.input_files[index]
            
    def select_output_directory(self):
        """Select output directory."""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_directory = directory
            self.output_var.set(directory)
            
    def preview_operation(self):
        """Preview the operation without executing."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select input files first.")
            return
            
        operation = self.operation_var.get()
        file_count = len(self.input_files)
        
        preview_text = f"""
Operation: {operation.replace('_', ' ').title()}
Files to process: {file_count}
Output directory: {self.output_directory or 'Same as input files'}
Quality: {self.quality_var.get()}
Size reduction: {self.size_reduction_var.get()}%
        """
        
        messagebox.showinfo("Operation Preview", preview_text)
        
    def reset_form(self):
        """Reset the form to default values."""
        self.clear_files()
        self.output_directory = None
        self.output_var.set("")
        self.operation_var.set("webp_to_png")
        self.quality_var.set(95)
        self.size_reduction_var.set(50)
        self.progress_bar['value'] = 0
        self.status_label.config(text="Ready to process images")
        
    def process_images(self):
        """Process the selected images."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select input files first.")
            return
            
        operation = self.operation_var.get()
        
        # Disable process button
        self.process_button.config(state='disabled')
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_images_thread, args=(operation,))
        thread.daemon = True
        thread.start()
        
    def _process_images_thread(self, operation):
        """Process images in a separate thread."""
        try:
            total_files = len(self.input_files)
            processed_files = 0
            
            for i, input_file in enumerate(self.input_files):
                # Update status
                self.parent.after(0, lambda: self.status_label.config(
                    text=f"Processing {Path(input_file).name}... ({i+1}/{total_files})"
                ))
                
                # Update progress
                progress = (i / total_files) * 100
                self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
                
                # Process the file
                self._process_single_file(input_file, operation)
                processed_files += 1
                
            # Complete
            self.parent.after(0, lambda: self.status_label.config(
                text=f"Completed! Processed {processed_files} files successfully."
            ))
            self.parent.after(0, lambda: self.progress_bar.config(value=100))
            self.parent.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Successfully processed {processed_files} files!"
            ))
            
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            # Re-enable process button
            self.parent.after(0, lambda: self.process_button.config(state='normal'))
            
    def _process_single_file(self, input_file: str, operation: str):
        """Process a single file."""
        input_path = Path(input_file)
        
        # Determine output path
        if self.output_directory:
            output_dir = Path(self.output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = input_path.parent
            
        # Map operations to functions
        operation_map = {
            'webp_to_png': (webp_to_png, '.png'),
            'webp_to_jpg': (webp_to_jpg, '.jpg'),
            'jpg_to_png': (jpg_to_png, '.png'),
            'png_to_jpg': (png_to_jpg, '.jpg'),
            'tiff_to_jpg': (tiff_to_jpg, '.jpg'),
            'heic_to_jpg': (heic_to_jpg, '.jpg'),
            'img_to_pdf': (img_to_pdf, '.pdf'),
            'img_to_greyscale': (img_to_greyscale, input_path.suffix),
            'reduce_img_size': (reduce_img_size, input_path.suffix),
            'remove_background': (remove_background, '.png'),
            'extract_img_metadata': (extract_img_metadata, '.txt'),
            'extract_text_from_img': (extract_text_from_img, '.txt')
        }
        
        if operation not in operation_map:
            raise ValueError(f"Unknown operation: {operation}")
            
        func, output_ext = operation_map[operation]
        
        # Generate output filename
        if operation in ['extract_img_metadata', 'extract_text_from_img']:
            output_file = output_dir / f"{input_path.stem}_metadata{output_ext}"
        else:
            output_file = output_dir / f"{input_path.stem}{output_ext}"
            
        # Call the appropriate function
        if operation == 'reduce_img_size':
            func(input_path, output_file, self.size_reduction_var.get())
        elif operation in ['png_to_jpg', 'webp_to_jpg', 'tiff_to_jpg', 'heic_to_jpg']:
            func(input_path, output_file, self.quality_var.get())
        elif operation == 'extract_img_metadata':
            func(input_path, save_flag=True)
        else:
            func(input_path, output_file)
