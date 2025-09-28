"""
PDF Management GUI for LocalUtilityBox.

This module provides a graphical interface for all PDF management operations.
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

from file_management.merge_pdf import merge_pdf
from file_management.split_pdf import split_pdf
from file_management.pdf_to_png import pdf_to_png
from file_management.pdf_to_jpg import pdf_to_jpg
from file_management.pdf_to_doc import pdf_to_docx as pdf_to_doc
from file_management.add_watermark import add_watermark


class PDFManagementGUI:
    """GUI for PDF management operations."""
    
    def __init__(self, parent, main_app):
        """Initialize the PDF management GUI."""
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
        ttk.Label(file_frame, text="Input PDF Files:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
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
        
        ttk.Button(button_frame, text="Add PDFs", command=self.add_pdfs).grid(row=0, column=0, padx=(0, 5))
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
        op_frame = ttk.LabelFrame(parent, text="PDF Operations", padding="10")
        op_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Operation selection
        self.operation_var = tk.StringVar()
        
        operations = [
            ("Merge PDFs", "merge_pdf"),
            ("Split PDF (Individual Pages)", "split_pdf"),
            ("Split PDF (Custom Parts)", "split_pdf_custom"),
            ("PDF to PNG Images", "pdf_to_png"),
            ("PDF to JPG Images", "pdf_to_jpg"),
            ("PDF to DOCX", "pdf_to_doc"),
            ("Add Watermark", "add_watermark")
        ]
        
        # Create radio buttons in a grid
        for i, (text, value) in enumerate(operations):
            row = i // 2
            col = i % 2
            ttk.Radiobutton(
                op_frame, 
                text=text, 
                variable=self.operation_var, 
                value=value
            ).grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
            
        # Set default selection
        self.operation_var.set("merge_pdf")
        
    def create_options_section(self, parent):
        """Create the options section."""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Split parts option
        ttk.Label(options_frame, text="Number of Parts (for split):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.split_parts_var = tk.IntVar(value=3)
        split_spinbox = ttk.Spinbox(
            options_frame, 
            from_=2, 
            to=20, 
            textvariable=self.split_parts_var,
            width=10
        )
        split_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Image quality
        ttk.Label(options_frame, text="Image Quality (1-100):").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.quality_var = tk.IntVar(value=95)
        quality_scale = ttk.Scale(
            options_frame, 
            from_=1, 
            to=100, 
            variable=self.quality_var, 
            orient=tk.HORIZONTAL
        )
        quality_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Quality value label
        self.quality_label = ttk.Label(options_frame, text="95")
        self.quality_label.grid(row=1, column=2, padx=(10, 0), pady=(0, 5))
        
        # Update quality label when scale changes
        quality_scale.config(command=self.update_quality_label)
        
        # Zip output option
        self.zip_output_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, 
            text="Create ZIP archive for image outputs", 
            variable=self.zip_output_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Watermark text
        ttk.Label(options_frame, text="Watermark Text:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        self.watermark_text_var = tk.StringVar(value="CONFIDENTIAL")
        watermark_entry = ttk.Entry(options_frame, textvariable=self.watermark_text_var, width=30)
        watermark_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 5))
        
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
            text="Process PDFs", 
            command=self.process_pdfs,
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
        self.status_label = ttk.Label(progress_frame, text="Ready to process PDFs")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
    def update_quality_label(self, value):
        """Update the quality label."""
        self.quality_label.config(text=str(int(float(value))))
        
    def add_pdfs(self):
        """Add PDF files to the list."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
                
    def add_folder(self):
        """Add all PDF files from a folder."""
        folder = filedialog.askdirectory(title="Select folder containing PDFs")
        if folder:
            folder_path = Path(folder)
            
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == '.pdf':
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
            messagebox.showwarning("No Files", "Please select input PDF files first.")
            return
            
        operation = self.operation_var.get()
        file_count = len(self.input_files)
        
        preview_text = f"""
Operation: {operation.replace('_', ' ').title()}
Files to process: {file_count}
Output directory: {self.output_directory or 'Same as input files'}
Quality: {self.quality_var.get()}
ZIP output: {self.zip_output_var.get()}
        """
        
        if operation == "add_watermark":
            preview_text += f"\nWatermark text: {self.watermark_text_var.get()}"
        elif operation == "split_pdf_custom":
            preview_text += f"\nSplit into: {self.split_parts_var.get()} parts"
            
        messagebox.showinfo("Operation Preview", preview_text)
        
    def reset_form(self):
        """Reset the form to default values."""
        self.clear_files()
        self.output_directory = None
        self.output_var.set("")
        self.operation_var.set("merge_pdf")
        self.quality_var.set(95)
        self.split_parts_var.set(3)
        self.zip_output_var.set(False)
        self.watermark_text_var.set("CONFIDENTIAL")
        self.progress_bar['value'] = 0
        self.status_label.config(text="Ready to process PDFs")
        
    def process_pdfs(self):
        """Process the selected PDFs."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select input PDF files first.")
            return
            
        operation = self.operation_var.get()
        
        # Validate operation-specific requirements
        if operation == "merge_pdf" and len(self.input_files) < 2:
            messagebox.showwarning("Invalid Selection", "Please select at least 2 PDF files for merging.")
            return
            
        # Disable process button
        self.process_button.config(state='disabled')
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_pdfs_thread, args=(operation,))
        thread.daemon = True
        thread.start()
        
    def _process_pdfs_thread(self, operation):
        """Process PDFs in a separate thread."""
        try:
            if operation == "merge_pdf":
                self._process_merge()
            elif operation == "split_pdf":
                self._process_split_individual()
            elif operation == "split_pdf_custom":
                self._process_split_custom()
            elif operation == "pdf_to_png":
                self._process_pdf_to_png()
            elif operation == "pdf_to_jpg":
                self._process_pdf_to_jpg()
            elif operation == "pdf_to_doc":
                self._process_pdf_to_doc()
            elif operation == "add_watermark":
                self._process_add_watermark()
                
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            # Re-enable process button
            self.parent.after(0, lambda: self.process_button.config(state='normal'))
            
    def _process_merge(self):
        """Process PDF merging."""
        self.parent.after(0, lambda: self.status_label.config(text="Merging PDFs..."))
        self.parent.after(0, lambda: self.progress_bar.config(value=50))
        
        # Determine output file
        if self.output_directory:
            output_dir = Path(self.output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "merged.pdf"
        else:
            output_file = Path(self.input_files[0]).parent / "merged.pdf"
            
        # Merge PDFs
        input_paths = [Path(f) for f in self.input_files]
        merge_pdf(input_paths, output_file)
        
        self.parent.after(0, lambda: self.status_label.config(text="PDFs merged successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"PDFs merged into: {output_file}"))
        
    def _process_split_individual(self):
        """Process PDF splitting into individual pages."""
        total_files = len(self.input_files)
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Splitting {Path(f).name}... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            split_pdf(Path(input_file))
            
        self.parent.after(0, lambda: self.status_label.config(text="PDFs split successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Split {total_files} PDFs into individual pages!"))
        
    def _process_split_custom(self):
        """Process PDF splitting into custom parts."""
        total_files = len(self.input_files)
        parts = self.split_parts_var.get()
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Splitting {Path(f).name} into {parts} parts... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            split_pdf(Path(input_file), parts)
            
        self.parent.after(0, lambda: self.status_label.config(text="PDFs split successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Split {total_files} PDFs into {parts} parts each!"))
        
    def _process_pdf_to_png(self):
        """Process PDF to PNG conversion."""
        total_files = len(self.input_files)
        zip_output = self.zip_output_var.get()
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Converting {Path(f).name} to PNG... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            pdf_to_png(Path(input_file), zip_output)
            
        self.parent.after(0, lambda: self.status_label.config(text="PDFs converted to PNG successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Converted {total_files} PDFs to PNG images!"))
        
    def _process_pdf_to_jpg(self):
        """Process PDF to JPG conversion."""
        total_files = len(self.input_files)
        quality = self.quality_var.get()
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Converting {Path(f).name} to JPG... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            pdf_to_jpg(Path(input_file), quality)
            
        self.parent.after(0, lambda: self.status_label.config(text="PDFs converted to JPG successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Converted {total_files} PDFs to JPG images!"))
        
    def _process_pdf_to_doc(self):
        """Process PDF to DOCX conversion."""
        total_files = len(self.input_files)
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Converting {Path(f).name} to DOCX... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            # Determine output file
            input_path = Path(input_file)
            if self.output_directory:
                output_dir = Path(self.output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / f"{input_path.stem}.docx"
            else:
                output_file = input_path.with_suffix('.docx')
                
            pdf_to_doc(input_path, output_file)
            
        self.parent.after(0, lambda: self.status_label.config(text="PDFs converted to DOCX successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Converted {total_files} PDFs to DOCX files!"))
        
    def _process_add_watermark(self):
        """Process adding watermarks to PDFs."""
        total_files = len(self.input_files)
        watermark_text = self.watermark_text_var.get()
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Adding watermark to {Path(f).name}... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            # Determine output file
            input_path = Path(input_file)
            if self.output_directory:
                output_dir = Path(self.output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / f"{input_path.stem}_watermarked.pdf"
            else:
                output_file = input_path.parent / f"{input_path.stem}_watermarked.pdf"
                
            add_watermark(input_path, output_file, watermark_text)
            
        self.parent.after(0, lambda: self.status_label.config(text="Watermarks added successfully!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Added watermarks to {total_files} PDFs!"))
