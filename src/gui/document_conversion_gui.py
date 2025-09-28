"""
Document Conversion GUI for LocalUtilityBox.

This module provides a graphical interface for all document conversion operations.
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

from file_management.csv_to_excel import csv_to_excel
from file_management.excel_to_csv import excel_to_csv
from file_management.csv_to_json import csv_to_json
from file_management.json_to_csv import json_to_csv
from file_management.doc_to_pdf import doc_to_pdf


class DocumentConversionGUI:
    """GUI for document conversion operations."""
    
    def __init__(self, parent, main_app):
        """Initialize the document conversion GUI."""
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
        op_frame = ttk.LabelFrame(parent, text="Document Operations", padding="10")
        op_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Operation selection
        self.operation_var = tk.StringVar()
        
        operations = [
            ("CSV to Excel", "csv_to_excel"),
            ("Excel to CSV", "excel_to_csv"),
            ("CSV to JSON", "csv_to_json"),
            ("JSON to CSV", "json_to_csv"),
            ("DOC to PDF", "doc_to_pdf")
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
        self.operation_var.set("csv_to_excel")
        
    def create_options_section(self, parent):
        """Create the options section."""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # CSV separator
        ttk.Label(options_frame, text="CSV Separator:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.separator_var = tk.StringVar(value=",")
        separator_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.separator_var,
            values=[",", ";", "\t", "|"],
            width=10,
            state="readonly"
        )
        separator_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # JSON formatting
        ttk.Label(options_frame, text="JSON Format:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.json_format_var = tk.StringVar(value="records")
        json_format_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.json_format_var,
            values=["records", "values", "index", "columns"],
            width=15,
            state="readonly"
        )
        json_format_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Include index
        self.include_index_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, 
            text="Include index in output", 
            variable=self.include_index_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
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
            text="Convert Documents", 
            command=self.process_documents,
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
        self.status_label = ttk.Label(progress_frame, text="Ready to convert documents")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
    def add_files(self):
        """Add files to the list."""
        filetypes = [
            ("All supported", "*.csv *.xlsx *.xls *.json *.doc *.docx"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls"),
            ("JSON files", "*.json"),
            ("Word documents", "*.doc *.docx"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select document files",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
                
    def add_folder(self):
        """Add all document files from a folder."""
        folder = filedialog.askdirectory(title="Select folder containing documents")
        if folder:
            folder_path = Path(folder)
            document_extensions = {'.csv', '.xlsx', '.xls', '.json', '.doc', '.docx'}
            
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in document_extensions:
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
Separator: {self.separator_var.get()}
JSON format: {self.json_format_var.get()}
Include index: {self.include_index_var.get()}
        """
        
        messagebox.showinfo("Operation Preview", preview_text)
        
    def reset_form(self):
        """Reset the form to default values."""
        self.clear_files()
        self.output_directory = None
        self.output_var.set("")
        self.operation_var.set("csv_to_excel")
        self.separator_var.set(",")
        self.json_format_var.set("records")
        self.include_index_var.set(False)
        self.progress_bar['value'] = 0
        self.status_label.config(text="Ready to convert documents")
        
    def process_documents(self):
        """Process the selected documents."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select input files first.")
            return
            
        operation = self.operation_var.get()
        
        # Disable process button
        self.process_button.config(state='disabled')
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_documents_thread, args=(operation,))
        thread.daemon = True
        thread.start()
        
    def _process_documents_thread(self, operation):
        """Process documents in a separate thread."""
        try:
            total_files = len(self.input_files)
            processed_files = 0
            
            for i, input_file in enumerate(self.input_files):
                # Update status
                self.parent.after(0, lambda f=input_file: self.status_label.config(
                    text=f"Converting {Path(f).name}... ({i+1}/{total_files})"
                ))
                
                # Update progress
                progress = (i / total_files) * 100
                self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
                
                # Process the file
                self._process_single_file(input_file, operation)
                processed_files += 1
                
            # Complete
            self.parent.after(0, lambda: self.status_label.config(
                text=f"Completed! Converted {processed_files} files successfully."
            ))
            self.parent.after(0, lambda: self.progress_bar.config(value=100))
            self.parent.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Successfully converted {processed_files} files!"
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
            
        # Map operations to functions and output extensions
        operation_map = {
            'csv_to_excel': (csv_to_excel, '.xlsx'),
            'excel_to_csv': (excel_to_csv, '.csv'),
            'csv_to_json': (csv_to_json, '.json'),
            'json_to_csv': (json_to_csv, '.csv'),
            'doc_to_pdf': (doc_to_pdf, '.pdf')
        }
        
        if operation not in operation_map:
            raise ValueError(f"Unknown operation: {operation}")
            
        func, output_ext = operation_map[operation]
        
        # Generate output filename
        output_file = output_dir / f"{input_path.stem}{output_ext}"
        
        # Call the appropriate function
        if operation == 'excel_to_csv':
            # Excel to CSV needs separator parameter
            func(input_path, self.separator_var.get(), output_file)
        elif operation == 'csv_to_json':
            # CSV to JSON needs format parameter
            func(input_path, output_file)
        elif operation == 'json_to_csv':
            # JSON to CSV needs format parameter
            func(input_path, output_file)
        else:
            func(input_path, output_file)
