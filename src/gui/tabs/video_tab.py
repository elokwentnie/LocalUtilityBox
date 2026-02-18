"""Video/Audio Tab."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from ..widgets import FileSelector, OutputFileSelector, ChoiceSelector, StatusDisplay
from ..utils import run_in_thread, validate_file_path

from video_audio_manipulation.extract_audio_from_video import extract_audio_from_video


class VideoTab(ttk.Frame):
    """Video/Audio Tab."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.status = StatusDisplay(self)
        
        # Extract Audio from Video
        self._create_extract_audio_section()
        
        self.status.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_extract_audio_section(self):
        """Extract audio from video."""
        frame = ttk.LabelFrame(self, text="Extract Audio from Video", padding=10)
        
        file_selector = FileSelector(frame, "Input Video File:",
                                    [("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])
        file_selector.pack(fill="x", pady=5)
        
        output_selector = OutputFileSelector(frame, "Output Audio File (Optional):",
                                            [("Audio files", "*.mp3 *.wav *.aac *.ogg")])
        output_selector.pack(fill="x", pady=5)
        
        format_choice = ChoiceSelector(frame, "Audio Format:",
                                      ["mp3", "wav", "aac", "ogg", "flac", "m4a"],
                                      "mp3")
        format_choice.pack(fill="x", pady=5)
        
        def execute():
            input_file = file_selector.get_path()
            if not input_file:
                messagebox.showerror("Error", "Please select an input video file.")
                return
            
            valid, error = validate_file_path(input_file, [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"])
            if not valid:
                # Try to proceed anyway - video file validation might be more lenient
                pass
            
            output_file = output_selector.get_path()
            audio_format = format_choice.get_value()
            
            def run():
                extract_audio_from_video(
                    Path(input_file),
                    audio_format,
                    Path(output_file) if output_file else None
                )
            
            def callback(result, error):
                if error:
                    self.status.add_message(f"Error: {error}", is_error=True)
                    messagebox.showerror("Error", str(error))
                else:
                    self.status.add_message(f"Successfully extracted audio from {input_file}")
                    messagebox.showinfo("Success", "Extraction completed!")
            
            run_in_thread(run, callback)
        
        ttk.Button(frame, text="Extract Audio", command=execute).pack(pady=10)
        frame.pack(fill="x", padx=10, pady=10)
