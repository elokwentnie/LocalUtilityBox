"""Main GUI Application for LocalUtilityBox."""
import tkinter as tk
from tkinter import ttk, messagebox

from .tabs.image_tab import ImageTab
from .tabs.file_tab import FileTab
from .tabs.video_tab import VideoTab


class LocalUtilityBoxGUI:
    """Main application window."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LocalUtilityBox")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Create menu bar
        self._create_menu()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.image_tab = ImageTab(self.notebook)
        self.notebook.add(self.image_tab, text="Image Processing")
        
        self.file_tab = FileTab(self.notebook)
        self.notebook.add(self.file_tab, text="File Management")
        
        self.video_tab = VideoTab(self.notebook)
        self.notebook.add(self.video_tab, text="Video/Audio")
        
        # Center window on screen
        self._center_window()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """LocalUtilityBox v1.0.0

A versatile utility for image and document processing.

Features:
• Image format conversion (WebP, JPG, PNG, TIFF, HEIC)
• Image processing (resize, greyscale, background removal)
• PDF operations (merge, split, watermark, convert)
• Document conversion (DOC ↔ PDF)
• Data format conversion (CSV ↔ Excel ↔ JSON)
• Audio extraction from video

All processing is done locally - your data stays private!
"""
        tk.messagebox.showinfo("About LocalUtilityBox", about_text)


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = LocalUtilityBoxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
