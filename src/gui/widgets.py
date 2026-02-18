"""Reusable GUI widget components."""
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from typing import Optional, Callable


class FileSelector:
    """Widget for selecting a single file."""
    
    def __init__(self, parent, label_text: str, file_types: list = None, 
                 on_change: Optional[Callable] = None):
        self.frame = ttk.Frame(parent)
        self.file_path = tk.StringVar()
        self.file_types = file_types or [("All files", "*.*")]
        self.on_change = on_change
        
        ttk.Label(self.frame, text=label_text).pack(anchor="w")
        
        entry_frame = ttk.Frame(self.frame)
        self.entry = ttk.Entry(entry_frame, textvariable=self.file_path, width=60)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(entry_frame, text="Browse", command=self.browse_file).pack(side="left")
        entry_frame.pack(fill="x", pady=5)
        
        self.file_path.trace_add("write", self._on_path_change)
    
    def browse_file(self):
        """Open file dialog."""
        file_path = filedialog.askopenfilename(filetypes=self.file_types)
        if file_path:
            self.file_path.set(file_path)
    
    def _on_path_change(self, *args):
        """Handle path change."""
        if self.on_change:
            self.on_change(self.file_path.get())
    
    def get_path(self) -> str:
        """Get selected file path."""
        return self.file_path.get()
    
    def set_path(self, path: str):
        """Set file path."""
        self.file_path.set(path)
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class DirectorySelector:
    """Widget for selecting a directory."""
    
    def __init__(self, parent, label_text: str, on_change: Optional[Callable] = None):
        self.frame = ttk.Frame(parent)
        self.dir_path = tk.StringVar()
        self.on_change = on_change
        
        ttk.Label(self.frame, text=label_text).pack(anchor="w")
        
        entry_frame = ttk.Frame(self.frame)
        self.entry = ttk.Entry(entry_frame, textvariable=self.dir_path, width=60)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(entry_frame, text="Browse", command=self.browse_directory).pack(side="left")
        entry_frame.pack(fill="x", pady=5)
        
        self.dir_path.trace_add("write", self._on_path_change)
    
    def browse_directory(self):
        """Open directory dialog."""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path.set(dir_path)
    
    def _on_path_change(self, *args):
        """Handle path change."""
        if self.on_change:
            self.on_change(self.dir_path.get())
    
    def get_path(self) -> str:
        """Get selected directory path."""
        return self.dir_path.get()
    
    def set_path(self, path: str):
        """Set directory path."""
        self.dir_path.set(path)
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class MultiFileSelector:
    """Widget for selecting multiple files."""
    
    def __init__(self, parent, label_text: str, file_types: list = None,
                 on_change: Optional[Callable] = None):
        self.frame = ttk.Frame(parent)
        self.file_paths = []
        self.file_types = file_types or [("All files", "*.*")]
        self.on_change = on_change
        
        ttk.Label(self.frame, text=label_text).pack(anchor="w")
        
        list_frame = ttk.Frame(self.frame)
        scrollbar = ttk.Scrollbar(list_frame)
        self.listbox = tk.Listbox(list_frame, height=4, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        list_frame.pack(fill="both", expand=True, pady=5)
        
        button_frame = ttk.Frame(self.frame)
        ttk.Button(button_frame, text="Add Files", command=self.add_files).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=2)
        button_frame.pack(pady=5)
    
    def add_files(self):
        """Open file dialog for multiple files."""
        file_paths = filedialog.askopenfilenames(filetypes=self.file_types)
        for file_path in file_paths:
            if file_path not in self.file_paths:
                self.file_paths.append(file_path)
                self.listbox.insert(tk.END, Path(file_path).name)
        if self.on_change:
            self.on_change(self.file_paths)
    
    def remove_selected(self):
        """Remove selected files."""
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            del self.file_paths[index]
        if self.on_change:
            self.on_change(self.file_paths)
    
    def clear_all(self):
        """Clear all files."""
        self.listbox.delete(0, tk.END)
        self.file_paths.clear()
        if self.on_change:
            self.on_change(self.file_paths)
    
    def get_paths(self) -> list:
        """Get selected file paths."""
        return self.file_paths.copy()
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class OutputFileSelector:
    """Widget for selecting output file (optional)."""
    
    def __init__(self, parent, label_text: str, file_types: list = None,
                 default_extension: str = None):
        self.frame = ttk.Frame(parent)
        self.file_path = tk.StringVar()
        self.file_types = file_types or [("All files", "*.*")]
        self.default_extension = default_extension
        
        ttk.Label(self.frame, text=label_text).pack(anchor="w")
        
        entry_frame = ttk.Frame(self.frame)
        self.entry = ttk.Entry(entry_frame, textvariable=self.file_path, width=60)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(entry_frame, text="Browse", command=self.browse_file).pack(side="left")
        entry_frame.pack(fill="x", pady=5)
    
    def browse_file(self):
        """Open save file dialog."""
        file_path = filedialog.asksaveasfilename(
            filetypes=self.file_types,
            defaultextension=self.default_extension
        )
        if file_path:
            self.file_path.set(file_path)
    
    def get_path(self) -> Optional[str]:
        """Get output file path (may be empty)."""
        path = self.file_path.get().strip()
        return path if path else None
    
    def set_path(self, path: str):
        """Set output file path."""
        self.file_path.set(path)
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class ParameterInput:
    """Widget for numeric parameter input."""
    
    def __init__(self, parent, label_text: str, default_value: str = "",
                 min_value: float = None, max_value: float = None):
        self.frame = ttk.Frame(parent)
        self.value = tk.StringVar(value=default_value)
        self.min_value = min_value
        self.max_value = max_value
        
        ttk.Label(self.frame, text=label_text).pack(side="left", padx=(0, 10))
        self.entry = ttk.Entry(self.frame, textvariable=self.value, width=15)
        self.entry.pack(side="left")
    
    def get_value(self):
        """Get parameter value."""
        try:
            value = float(self.value.get())
            if self.min_value is not None and value < self.min_value:
                return self.min_value
            if self.max_value is not None and value > self.max_value:
                return self.max_value
            return value
        except ValueError:
            return None
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class ChoiceSelector:
    """Widget for selecting from choices (dropdown or radio buttons)."""
    
    def __init__(self, parent, label_text: str, choices: list, default: str = None):
        self.frame = ttk.Frame(parent)
        self.value = tk.StringVar(value=default or choices[0] if choices else "")
        self.choices = choices
        
        ttk.Label(self.frame, text=label_text).pack(side="left", padx=(0, 10))
        self.combo = ttk.Combobox(self.frame, textvariable=self.value, 
                                  values=choices, state="readonly", width=20)
        self.combo.pack(side="left")
    
    def get_value(self) -> str:
        """Get selected value."""
        return self.value.get()
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)


class StatusDisplay:
    """Widget for displaying status messages."""
    
    def __init__(self, parent, height: int = 5):
        self.frame = ttk.Frame(parent)
        
        ttk.Label(self.frame, text="Status:").pack(anchor="w")
        
        text_frame = ttk.Frame(self.frame)
        scrollbar = ttk.Scrollbar(text_frame)
        self.text = tk.Text(text_frame, height=height, wrap=tk.WORD,
                            yscrollcommand=scrollbar.set, state=tk.DISABLED)
        scrollbar.config(command=self.text.yview)
        
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        text_frame.pack(fill="both", expand=True, pady=5)
    
    def add_message(self, message: str, is_error: bool = False):
        """Add a status message."""
        self.text.config(state=tk.NORMAL)
        tag = "error" if is_error else "normal"
        self.text.insert(tk.END, message + "\n", tag)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear status messages."""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
