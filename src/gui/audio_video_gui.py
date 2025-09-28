"""
Audio/Video Processing GUI for LocalUtilityBox.

This module provides a graphical interface for audio/video processing operations.
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

from video_audio_manipulation.extract_audio_from_video import extract_audio_from_video


class AudioVideoGUI:
    """GUI for audio/video processing operations."""
    
    def __init__(self, parent, main_app):
        """Initialize the audio/video GUI."""
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
        ttk.Label(file_frame, text="Input Video/Audio Files:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
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
        op_frame = ttk.LabelFrame(parent, text="Audio/Video Operations", padding="10")
        op_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Operation selection
        self.operation_var = tk.StringVar()
        
        operations = [
            ("Extract Audio from Video", "extract_audio"),
            ("Convert Video Format", "convert_video"),
            ("Compress Video", "compress_video"),
            ("Extract Frames", "extract_frames")
        ]
        
        # Create radio buttons
        for i, (text, value) in enumerate(operations):
            ttk.Radiobutton(
                op_frame, 
                text=text, 
                variable=self.operation_var, 
                value=value
            ).grid(row=i, column=0, sticky=tk.W, pady=2)
            
        # Set default selection
        self.operation_var.set("extract_audio")
        
    def create_options_section(self, parent):
        """Create the options section."""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Audio format
        ttk.Label(options_frame, text="Audio Format:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.audio_format_var = tk.StringVar(value="mp3")
        audio_format_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.audio_format_var,
            values=["mp3", "wav", "aac", "flac", "ogg"],
            width=10,
            state="readonly"
        )
        audio_format_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Audio quality
        ttk.Label(options_frame, text="Audio Quality:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.audio_quality_var = tk.StringVar(value="high")
        audio_quality_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.audio_quality_var,
            values=["low", "medium", "high", "lossless"],
            width=10,
            state="readonly"
        )
        audio_quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Video quality
        ttk.Label(options_frame, text="Video Quality:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.video_quality_var = tk.StringVar(value="medium")
        video_quality_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.video_quality_var,
            values=["low", "medium", "high", "ultra"],
            width=10,
            state="readonly"
        )
        video_quality_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Compression level
        ttk.Label(options_frame, text="Compression Level:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.compression_var = tk.IntVar(value=50)
        compression_scale = ttk.Scale(
            options_frame, 
            from_=10, 
            to=90, 
            variable=self.compression_var, 
            orient=tk.HORIZONTAL
        )
        compression_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Compression value label
        self.compression_label = ttk.Label(options_frame, text="50%")
        self.compression_label.grid(row=3, column=2, padx=(10, 0), pady=(0, 5))
        
        # Update compression label when scale changes
        compression_scale.config(command=self.update_compression_label)
        
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
            text="Process Media", 
            command=self.process_media,
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
        self.status_label = ttk.Label(progress_frame, text="Ready to process media files")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
    def update_compression_label(self, value):
        """Update the compression label."""
        self.compression_label.config(text=f"{int(float(value))}%")
        
    def add_files(self):
        """Add files to the list."""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("Audio files", "*.mp3 *.wav *.aac *.flac *.ogg *.m4a *.wma"),
            ("All media files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v *.mp3 *.wav *.aac *.flac *.ogg *.m4a *.wma"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select media files",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
                
    def add_folder(self):
        """Add all media files from a folder."""
        folder = filedialog.askdirectory(title="Select folder containing media files")
        if folder:
            folder_path = Path(folder)
            media_extensions = {
                '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
                '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'
            }
            
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in media_extensions:
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
Audio format: {self.audio_format_var.get()}
Audio quality: {self.audio_quality_var.get()}
Video quality: {self.video_quality_var.get()}
Compression: {self.compression_var.get()}%
        """
        
        messagebox.showinfo("Operation Preview", preview_text)
        
    def reset_form(self):
        """Reset the form to default values."""
        self.clear_files()
        self.output_directory = None
        self.output_var.set("")
        self.operation_var.set("extract_audio")
        self.audio_format_var.set("mp3")
        self.audio_quality_var.set("high")
        self.video_quality_var.set("medium")
        self.compression_var.set(50)
        self.progress_bar['value'] = 0
        self.status_label.config(text="Ready to process media files")
        
    def process_media(self):
        """Process the selected media files."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select input files first.")
            return
            
        operation = self.operation_var.get()
        
        # Disable process button
        self.process_button.config(state='disabled')
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_media_thread, args=(operation,))
        thread.daemon = True
        thread.start()
        
    def _process_media_thread(self, operation):
        """Process media files in a separate thread."""
        try:
            if operation == "extract_audio":
                self._process_extract_audio()
            elif operation == "convert_video":
                self._process_convert_video()
            elif operation == "compress_video":
                self._process_compress_video()
            elif operation == "extract_frames":
                self._process_extract_frames()
                
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            # Re-enable process button
            self.parent.after(0, lambda: self.process_button.config(state='normal'))
            
    def _process_extract_audio(self):
        """Process audio extraction from video."""
        total_files = len(self.input_files)
        audio_format = self.audio_format_var.get()
        
        for i, input_file in enumerate(self.input_files):
            self.parent.after(0, lambda f=input_file: self.status_label.config(
                text=f"Extracting audio from {Path(f).name}... ({i+1}/{total_files})"
            ))
            
            progress = (i / total_files) * 100
            self.parent.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            # Determine output file
            input_path = Path(input_file)
            if self.output_directory:
                output_dir = Path(self.output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / f"{input_path.stem}.{audio_format}"
            else:
                output_file = input_path.parent / f"{input_path.stem}.{audio_format}"
                
            # Extract audio
            extract_audio_from_video(input_path, output_file)
            
        self.parent.after(0, lambda: self.status_label.config(text="Audio extraction completed!"))
        self.parent.after(0, lambda: self.progress_bar.config(value=100))
        self.parent.after(0, lambda: messagebox.showinfo("Success", f"Extracted audio from {total_files} videos!"))
        
    def _process_convert_video(self):
        """Process video format conversion."""
        self.parent.after(0, lambda: self.status_label.config(text="Video conversion not yet implemented"))
        self.parent.after(0, lambda: messagebox.showinfo("Info", "Video conversion feature coming soon!"))
        
    def _process_compress_video(self):
        """Process video compression."""
        self.parent.after(0, lambda: self.status_label.config(text="Video compression not yet implemented"))
        self.parent.after(0, lambda: messagebox.showinfo("Info", "Video compression feature coming soon!"))
        
    def _process_extract_frames(self):
        """Process frame extraction."""
        self.parent.after(0, lambda: self.status_label.config(text="Frame extraction not yet implemented"))
        self.parent.after(0, lambda: messagebox.showinfo("Info", "Frame extraction feature coming soon!"))
