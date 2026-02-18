"""File Management Tab."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from ..widgets import (
    FileSelector, DirectorySelector, MultiFileSelector, OutputFileSelector,
    ParameterInput, ChoiceSelector, StatusDisplay
)
from ..utils import run_in_thread, validate_file_path, validate_directory_path

# Import file management functions
from file_management.merge_pdf import merge_pdf
from file_management.split_pdf import split_pdf
from file_management.add_watermark import add_watermark
from file_management.doc_to_pdf import doc_to_pdf
from file_management.pdf_to_doc import pdf_to_docx
from file_management.pdf_to_png import pdf_to_png
from file_management.pdf_to_jpg import pdf_to_jpg
from file_management.csv_to_excel import csv_to_excel
from file_management.excel_to_csv import excel_to_csv
from file_management.csv_to_json import csv_to_json
from file_management.json_to_csv import json_to_csv


class FileTab(ttk.Frame):
    """File Management Tab."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.status = StatusDisplay(self)
        
        # Create notebook for organizing tools
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # PDF Operations Tab
        pdf_frame = ttk.Frame(notebook)
        self._create_pdf_operations_section(pdf_frame)
        notebook.add(pdf_frame, text="PDF Operations")
        
        # Document Conversion Tab
        doc_frame = ttk.Frame(notebook)
        self._create_document_conversion_section(doc_frame)
        notebook.add(doc_frame, text="Document Conversion")
        
        # Data Format Conversion Tab
        data_frame = ttk.Frame(notebook)
        self._create_data_conversion_section(data_frame)
        notebook.add(data_frame, text="Data Format Conversion")
        
        self.status.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_pdf_operations_section(self, parent):
        """Create PDF operations section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Merge PDF
        self._create_merge_pdf_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Split PDF
        self._create_split_pdf_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Add Watermark
        self._create_add_watermark_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # PDF to PNG
        self._create_pdf_to_png_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # PDF to JPG
        self._create_pdf_to_jpg_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_document_conversion_section(self, parent):
        """Create document conversion section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # DOC to PDF
        self._create_doc_to_pdf_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # PDF to DOC
        self._create_pdf_to_doc_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_data_conversion_section(self, parent):
        """Create data format conversion section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # CSV to Excel
        self._create_csv_to_excel_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Excel to CSV
        self._create_excel_to_csv_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # CSV to JSON
        self._create_csv_to_json_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # JSON to CSV
        self._create_json_to_csv_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_merge_pdf_section(self, parent):
        """Merge PDF files."""
        frame = ttk.LabelFrame(parent, text="Merge PDF Files", padding=10)
        
        file_selector = MultiFileSelector(frame, "Input PDF Files:",
                                         [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        dir_selector = DirectorySelector(frame, "Or Select Directory:")
        dir_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output PDF File (Optional):",
                                            [("PDF files", "*.pdf")], ".pdf")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            files = file_selector.get_paths()
            directory = dir_selector.get_path()
            
            if not files and not directory:
                messagebox.showerror("Error", "Please select files or a directory.")
                return
            
            output_file = output_selector.get_path()
            
            def run():
                if files:
                    merge_pdf([Path(f) for f in files], Path(output_file) if output_file else None)
                else:
                    pdf_files = sorted(Path(directory).glob("*.pdf"))
                    if pdf_files:
                        merge_pdf(pdf_files, Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully merged PDF files")
                    messagebox.showinfo("Success", "Merge completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Merge PDFs", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_split_pdf_section(self, parent):
        """Split PDF file."""
        frame = ttk.LabelFrame(parent, text="Split PDF File", padding=10)
        
        file_selector = FileSelector(frame, "Input PDF File:", [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        parts_input = ParameterInput(frame, "Number of Parts (Optional, leave empty for individual pages):", "")
        parts_input.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            parts_value = parts_input.get_value()
            
            def run():
                from file_management.split_pdf import split_pdf, get_splitting_parts
                from PyPDF2 import PdfReader
                
                if parts_value:
                    try:
                        reader = PdfReader(str(input_file))
                        pdf_length = len(reader.pages)
                        num_parts = int(parts_value)
                        if num_parts > pdf_length:
                            parts = None  # Split into individual pages
                        else:
                            parts = get_splitting_parts(pdf_length, num_parts)
                    except Exception as e:
                        parts = None
                else:
                    parts = None
                
                split_pdf(Path(input_file), parts)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully split {input_file}")
                    messagebox.showinfo("Success", "Split completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Split PDF", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_add_watermark_section(self, parent):
        """Add watermark to PDF."""
        frame = ttk.LabelFrame(parent, text="Add Watermark to PDF", padding=10)
        
        file_selector = FileSelector(frame, "Input PDF File:", [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        watermark_selector = FileSelector(frame, "Watermark PDF File:", [("PDF files", "*.pdf")])
        watermark_selector.pack(fill="x", pady=5)
        
        pages_label = ttk.Label(frame, text="Page Indices (comma-separated, leave empty for all pages):")
        pages_label.pack(anchor="w", pady=5)
        pages_entry = ttk.Entry(frame, width=60)
        pages_entry.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            watermark_file = watermark_selector.get_path()
            
            if not input_file or not watermark_file:
                messagebox.showerror("Error", "Please select both input and watermark files.")
                return
            
            valid, error = validate_file_path(input_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", f"Input file: {error}")
                return
            
            valid, error = validate_file_path(watermark_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", f"Watermark file: {error}")
                return
            
            pages_str = pages_entry.get().strip()
            if pages_str:
                try:
                    pages = [int(p.strip()) for p in pages_str.split(",")]
                except ValueError:
                    messagebox.showerror("Error", "Invalid page indices format.")
                    return
            else:
                pages = "ALL"
            
            def run():
                add_watermark(Path(input_file), Path(watermark_file), pages)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully added watermark")
                    messagebox.showinfo("Success", "Watermark added!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Add Watermark", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_pdf_to_png_section(self, parent):
        """Convert PDF to PNG."""
        frame = ttk.LabelFrame(parent, text="PDF to PNG", padding=10)
        
        file_selector = FileSelector(frame, "Input PDF File:", [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        zip_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Zip output files", variable=zip_var).pack(pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            def run():
                pdf_to_png(Path(input_file), zip_var.get())
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to PNG")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_pdf_to_jpg_section(self, parent):
        """Convert PDF to JPG."""
        frame = ttk.LabelFrame(parent, text="PDF to JPG", padding=10)
        
        file_selector = FileSelector(frame, "Input PDF File:", [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        zip_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Zip output files", variable=zip_var).pack(pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            def run():
                from file_management.pdf_to_jpg import pdf_to_jpg
                pdf_to_jpg(Path(input_file), zip_var.get())
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to JPG")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_doc_to_pdf_section(self, parent):
        """Convert DOC to PDF."""
        frame = ttk.LabelFrame(parent, text="DOC to PDF", padding=10)
        
        file_selector = FileSelector(frame, "Input DOC File:", 
                                    [("DOC files", "*.doc *.docx")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output PDF File (Optional):",
                                            [("PDF files", "*.pdf")], ".pdf")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".doc", ".docx"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                doc_to_pdf(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to PDF")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_pdf_to_doc_section(self, parent):
        """Convert PDF to DOC."""
        frame = ttk.LabelFrame(parent, text="PDF to DOC", padding=10)
        
        file_selector = FileSelector(frame, "Input PDF File:", [("PDF files", "*.pdf")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output DOC File (Optional):",
                                            [("DOC files", "*.docx")], ".docx")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".pdf"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                pdf_to_docx(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to DOC")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_csv_to_excel_section(self, parent):
        """Convert CSV to Excel."""
        frame = ttk.LabelFrame(parent, text="CSV to Excel", padding=10)
        
        file_selector = FileSelector(frame, "Input CSV File:", [("CSV files", "*.csv")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output Excel File (Optional):",
                                            [("Excel files", "*.xlsx")], ".xlsx")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".csv"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                csv_to_excel(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to Excel")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_excel_to_csv_section(self, parent):
        """Convert Excel to CSV."""
        frame = ttk.LabelFrame(parent, text="Excel to CSV", padding=10)
        
        file_selector = FileSelector(frame, "Input Excel File:", 
                                    [("Excel files", "*.xlsx *.xls")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output CSV File (Optional):",
                                            [("CSV files", "*.csv")], ".csv")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".xlsx", ".xls"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                from file_management.excel_to_csv import excel_to_csv
                excel_to_csv(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to CSV")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_csv_to_json_section(self, parent):
        """Convert CSV to JSON."""
        frame = ttk.LabelFrame(parent, text="CSV to JSON", padding=10)
        
        file_selector = FileSelector(frame, "Input CSV File:", [("CSV files", "*.csv")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output JSON File (Optional):",
                                            [("JSON files", "*.json")], ".json")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".csv"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                csv_to_json(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to JSON")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_json_to_csv_section(self, parent):
        """Convert JSON to CSV."""
        frame = ttk.LabelFrame(parent, text="JSON to CSV", padding=10)
        
        file_selector = FileSelector(frame, "Input JSON File:", [("JSON files", "*.json")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output CSV File (Optional):",
                                            [("CSV files", "*.csv")], ".csv")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".json"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                from file_management.json_to_csv import json_to_csv
                json_to_csv(Path(input_file), Path(output_file) if output_file else None)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to CSV")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
