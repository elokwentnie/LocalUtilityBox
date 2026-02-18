"""Image Processing Tab."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

from ..widgets import (
    FileSelector, DirectorySelector, MultiFileSelector, OutputFileSelector,
    ParameterInput, ChoiceSelector, StatusDisplay
)
from ..utils import run_in_thread, validate_file_path, validate_directory_path

# Import image processing functions (absolute for installed package)
from image_processing.webp_to_jpg import webp_to_jpg
from image_processing.webp_to_png import webp_to_png
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


class ImageTab(ttk.Frame):
    """Image Processing Tab."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.status = StatusDisplay(self)
        self.status.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for organizing tools
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Format Conversion Tab
        format_frame = ttk.Frame(notebook)
        self._create_format_conversion_section(format_frame)
        notebook.add(format_frame, text="Format Conversion")
        
        # Image Processing Tab
        processing_frame = ttk.Frame(notebook)
        self._create_image_processing_section(processing_frame)
        notebook.add(processing_frame, text="Image Processing")
        
        # Extraction Tab
        extraction_frame = ttk.Frame(notebook)
        self._create_extraction_section(extraction_frame)
        notebook.add(extraction_frame, text="Extraction")
        
        self.status.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_format_conversion_section(self, parent):
        """Create format conversion tools section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # WebP to JPG
        self._create_webp_to_jpg_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # WebP to PNG
        self._create_webp_to_png_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # JPG to PNG
        self._create_jpg_to_png_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # PNG to JPG
        self._create_png_to_jpg_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # TIFF to JPG
        self._create_tiff_to_jpg_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # HEIC to JPG
        self._create_heic_to_jpg_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_image_processing_section(self, parent):
        """Create image processing tools section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Image to PDF
        self._create_img_to_pdf_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Image to Greyscale
        self._create_img_to_greyscale_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Reduce Image Size
        self._create_reduce_img_size_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Remove Background
        self._create_remove_background_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_extraction_section(self, parent):
        """Create extraction tools section."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Extract Metadata
        self._create_extract_metadata_section(scrollable_frame)
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Extract Text from Image
        self._create_extract_text_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_webp_to_jpg_section(self, parent):
        """WebP to JPG converter."""
        frame = ttk.LabelFrame(parent, text="WebP to JPG", padding=10)
        
        file_selector = FileSelector(frame, "Input WebP File:", [("WebP files", "*.webp")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output JPG File (Optional):", 
                                            [("JPG files", "*.jpg")], ".jpg")
        output_selector.pack(fill="x", pady=5)
        
        bg_frame = ttk.Frame(frame)
        bg_choice = ChoiceSelector(bg_frame, "Background Color:", ["black", "white"], "black")
        bg_choice.pack()
        bg_frame.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".webp"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            bg_color = bg_choice.get_value()
            
            def run():
                webp_to_jpg(Path(input_file), Path(output_file) if output_file else None, bg_color)
            
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
    
    def _create_webp_to_png_section(self, parent):
        """WebP to PNG converter."""
        frame = ttk.LabelFrame(parent, text="WebP to PNG", padding=10)
        
        file_selector = FileSelector(frame, "Input WebP File:", [("WebP files", "*.webp")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output PNG File (Optional):",
                                            [("PNG files", "*.png")], ".png")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".webp"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                webp_to_png(Path(input_file), Path(output_file) if output_file else None)
            
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
    
    def _create_jpg_to_png_section(self, parent):
        """JPG to PNG converter."""
        frame = ttk.LabelFrame(parent, text="JPG to PNG", padding=10)
        
        file_selector = FileSelector(frame, "Input JPG File:", 
                                     [("JPG files", "*.jpg *.jpeg")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output PNG File (Optional):",
                                            [("PNG files", "*.png")], ".png")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".jpg", ".jpeg"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                from image_processing.jpg_to_png import jpg_to_png
                jpg_to_png(Path(input_file), Path(output_file) if output_file else None, 95)
            
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
    
    def _create_png_to_jpg_section(self, parent):
        """PNG to JPG converter."""
        frame = ttk.LabelFrame(parent, text="PNG to JPG", padding=10)
        
        file_selector = FileSelector(frame, "Input PNG File:", [("PNG files", "*.png")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output JPG File (Optional):",
                                            [("JPG files", "*.jpg")], ".jpg")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".png"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                png_to_jpg(Path(input_file), Path(output_file) if output_file else None, 95)
            
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
    
    def _create_tiff_to_jpg_section(self, parent):
        """TIFF to JPG converter."""
        frame = ttk.LabelFrame(parent, text="TIFF to JPG", padding=10)
        
        file_selector = FileSelector(frame, "Input TIFF File:", 
                                     [("TIFF files", "*.tiff *.tif")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output JPG File (Optional):",
                                            [("JPG files", "*.jpg")], ".jpg")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            valid, error = validate_file_path(input_file, [".tiff", ".tif"])
            if not valid:
                messagebox.showerror("Error", error)
                return
            
            output_file = output_selector.get_path()
            
            def run():
                tiff_to_jpg(Path(input_file), Path(output_file) if output_file else None)
            
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
    
    def _create_heic_to_jpg_section(self, parent):
        """HEIC to JPG converter."""
        frame = ttk.LabelFrame(parent, text="HEIC to JPG", padding=10)
        
        file_selector = MultiFileSelector(frame, "Input HEIC Files:", 
                                         [("HEIC files", "*.heic *.HEIC")])
        file_selector.pack(fill="x", pady=5)
        
        dir_selector = DirectorySelector(frame, "Or Select Directory:")
        dir_selector.pack(fill="x", pady=5)
        
        quality_input = ParameterInput(frame, "Quality (1-100):", "95", 1, 100)
        quality_input.pack(fill="x", pady=5)
        
        def execute():
            files = file_selector.get_paths()
            directory = dir_selector.get_path()
            
            if not files and not directory:
                messagebox.showerror("Error", "Please select files or a directory.")
                return
            
            quality = quality_input.get_value() or 95
            
            def run():
                if files:
                    heic_to_jpg([str(f) for f in files], None, quality)
                else:
                    from pathlib import Path
                    heic_files = list(Path(directory).glob("*.heic")) + \
                                list(Path(directory).glob("*.HEIC"))
                    if heic_files:
                        heic_to_jpg([str(f) for f in heic_files], None, quality)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully converted HEIC files to JPG")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_img_to_pdf_section(self, parent):
        """Image to PDF converter."""
        frame = ttk.LabelFrame(parent, text="Image to PDF", padding=10)
        
        file_selector = MultiFileSelector(frame, "Input Image Files:",
                                          [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output PDF File (Optional):",
                                            [("PDF files", "*.pdf")], ".pdf")
        output_selector.pack(fill="x", pady=5)
        
        def execute():
            files = file_selector.get_paths()
            if not files:
                messagebox.showerror("Error", "Please select at least one image file.")
                return
            
            output_file = output_selector.get_path()
            
            def run():
                import img2pdf
                from pathlib import Path
                
                # img_to_pdf function only handles single file
                # For multiple files, use img2pdf directly to combine them
                if len(files) == 1:
                    img_to_pdf(Path(files[0]), Path(output_file) if output_file else None)
                else:
                    # Multiple files - combine into one PDF
                    if not output_file:
                        output_file = Path(files[0]).parent / "combined_images.pdf"
                    else:
                        output_file = Path(output_file)
                    
                    with open(output_file, "wb") as f:
                        f.write(img2pdf.convert([str(Path(f)) for f in files]))
                    print(f"Conversion successful: {output_file}")
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully created PDF from images")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_img_to_greyscale_section(self, parent):
        """Image to greyscale converter."""
        frame = ttk.LabelFrame(parent, text="Image to Greyscale", padding=10)
        
        file_selector = FileSelector(frame, "Input Image File:",
                                     [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output File (Optional):",
                                            [("Image files", "*.jpg *.png")])
        output_selector.pack(fill="x", pady=5)
        
        quality_input = ParameterInput(frame, "Quality (0-100):", "85", 0, 100)
        quality_input.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            output_file = output_selector.get_path()
            quality = quality_input.get_value() or 85
            
            def run():
                img_to_greyscale(Path(input_file), 
                               Path(output_file) if output_file else None, 
                               int(quality))
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully converted {input_file} to greyscale")
                    messagebox.showinfo("Success", "Conversion completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Convert", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_reduce_img_size_section(self, parent):
        """Reduce image size."""
        frame = ttk.LabelFrame(parent, text="Reduce Image Size", padding=10)
        
        file_selector = MultiFileSelector(frame, "Input Image Files:",
                                         [("JPG files", "*.jpg *.jpeg")])
        file_selector.pack(fill="x", pady=5)
        
        dir_selector = DirectorySelector(frame, "Or Select Directory:")
        dir_selector.pack(fill="x", pady=5)
        
        scale_input = ParameterInput(frame, "Scale Percentage (1-100):", "50", 1, 100)
        scale_input.pack(fill="x", pady=5)
        
        quality_input = ParameterInput(frame, "Quality (1-100):", "85", 1, 100)
        quality_input.pack(fill="x", pady=5)
        
        def execute():
            files = file_selector.get_paths()
            directory = dir_selector.get_path()
            
            if not files and not directory:
                messagebox.showerror("Error", "Please select files or a directory.")
                return
            
            scale = scale_input.get_value() or 50
            quality = quality_input.get_value() or 85
            
            def run():
                if files:
                    reduce_img_size([Path(f) for f in files], scale / 100, int(quality))
                else:
                    from pathlib import Path
                    jpg_files = list(Path(directory).glob("*.jpg")) + \
                               list(Path(directory).glob("*.jpeg"))
                    if jpg_files:
                        reduce_img_size(jpg_files, scale / 100, int(quality))
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully reduced image sizes")
                    messagebox.showinfo("Success", "Processing completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Reduce Size", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_remove_background_section(self, parent):
        """Remove background from images."""
        frame = ttk.LabelFrame(parent, text="Remove Background", padding=10)
        
        file_selector = MultiFileSelector(frame, "Input Image Files:",
                                         [("Image files", "*.jpg *.jpeg *.png")])
        file_selector.pack(fill="x", pady=5)
        
        dir_selector = DirectorySelector(frame, "Or Select Directory:")
        dir_selector.pack(fill="x", pady=5)
        
        def execute():
            files = file_selector.get_paths()
            directory = dir_selector.get_path()
            
            if not files and not directory:
                messagebox.showerror("Error", "Please select files or a directory.")
                return
            
            def run():
                if files:
                    remove_background([Path(f) for f in files])
                else:
                    from pathlib import Path
                    img_files = list(Path(directory).glob("*.jpg")) + \
                               list(Path(directory).glob("*.jpeg")) + \
                               list(Path(directory).glob("*.png"))
                    if img_files:
                        remove_background(img_files)
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message("Successfully removed backgrounds")
                    messagebox.showinfo("Success", "Processing completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Remove Background", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_extract_metadata_section(self, parent):
        """Extract metadata from image."""
        frame = ttk.LabelFrame(parent, text="Extract Image Metadata", padding=10)
        
        file_selector = FileSelector(frame, "Input Image File:",
                                    [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")])
        file_selector.pack(fill="x", pady=5)
        
        save_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Save to file", variable=save_var).pack(pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            def run():
                extract_img_metadata(Path(input_file), save_var.get())
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully extracted metadata from {input_file}")
                    messagebox.showinfo("Success", "Extraction completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Extract Metadata", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
    
    def _create_extract_text_section(self, parent):
        """Extract text from image (OCR)."""
        frame = ttk.LabelFrame(parent, text="Extract Text from Image (OCR)", padding=10)
        
        file_selector = FileSelector(frame, "Input Image File:",
                                    [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")])
        file_selector.pack(fill="x", pady=5)
        
        save_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Save to file", variable=save_var).pack(pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input file.")
                return
            
            def run():
                extract_text_from_img(Path(input_file), save_var.get())
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully extracted text from {input_file}")
                    messagebox.showinfo("Success", "Extraction completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Extract Text", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=5)
