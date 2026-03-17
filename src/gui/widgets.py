"""Modern GUI widget components using customtkinter."""
import sys
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, StringVar, BooleanVar
from pathlib import Path
from typing import Callable, List, Optional


def _reveal_path(path_str: str) -> None:
    """Open the file or directory in the system file manager."""
    path = Path(path_str)
    try:
        if sys.platform == "darwin":
            if path.is_file():
                subprocess.run(["open", "-R", str(path)], check=False)
            else:
                subprocess.run(["open", str(path)], check=False)
        elif sys.platform == "win32":
            if path.is_file():
                subprocess.run(["explorer", f"/select,{path}"], check=False)
            else:
                subprocess.run(["explorer", str(path)], check=False)
        else:
            target = str(path.parent if path.is_file() else path)
            subprocess.run(["xdg-open", target], check=False)
    except Exception:
        pass


def _reveal_label() -> str:
    if sys.platform == "darwin":
        return "Show in Finder"
    elif sys.platform == "win32":
        return "Show in Explorer"
    return "Open Folder"

try:
    from tkinterdnd2 import DND_FILES
    _HAS_DND = True
except ImportError:
    _HAS_DND = False


def bind_mousewheel(scrollable_frame: ctk.CTkScrollableFrame) -> None:
    """Fix mousewheel scrolling over child widgets inside a CTkScrollableFrame."""
    canvas = scrollable_frame._parent_canvas

    if sys.platform == "darwin":
        def _scroll(event):
            canvas.yview_scroll(-event.delta, "units")
    else:
        def _scroll(event):
            canvas.yview_scroll(-event.delta // 120, "units")

    def _bind_recursive(widget):
        widget.bind("<MouseWheel>", _scroll, add=True)
        for child in widget.winfo_children():
            _bind_recursive(child)

    _bind_recursive(scrollable_frame)


def _parse_drop_paths(drop_data: str) -> List[str]:
    """Parse file paths from a tkinterdnd2 drop event data string."""
    paths = []
    current = []
    in_braces = False
    for char in drop_data:
        if char == '{':
            in_braces = True
        elif char == '}':
            in_braces = False
            paths.append("".join(current))
            current = []
        elif char == ' ' and not in_braces:
            if current:
                paths.append("".join(current))
                current = []
        else:
            current.append(char)
    if current:
        paths.append("".join(current))
    return [p for p in paths if p]


class FileInput(ctk.CTkFrame):
    """Single-file input with browse button and optional drag-and-drop."""

    def __init__(self, parent, label: str, filetypes: list = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.filetypes = filetypes or [("All files", "*.*")]
        self._path = StringVar()

        ctk.CTkLabel(
            self, text=label, font=("", 13, "bold"), anchor="w"
        ).pack(fill="x", pady=(0, 6))

        row = ctk.CTkFrame(self, fg_color="transparent")
        self.entry = ctk.CTkEntry(
            row, textvariable=self._path, placeholder_text="No file selected"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            row, text="Browse", width=90, command=self._browse,
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
        ).pack(side="right")
        row.pack(fill="x")

        self._try_enable_dnd()

    def _try_enable_dnd(self):
        if not _HAS_DND:
            return
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        paths = _parse_drop_paths(event.data)
        if paths:
            self._path.set(paths[0])

    def _browse(self):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self._path.set(path)

    def get(self) -> str:
        return self._path.get().strip()

    def set(self, path: str):
        self._path.set(path)


class DirectoryInput(ctk.CTkFrame):
    """Directory selector with browse button and optional drag-and-drop."""

    def __init__(self, parent, label: str, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._path = StringVar()

        ctk.CTkLabel(
            self, text=label, font=("", 13, "bold"), anchor="w"
        ).pack(fill="x", pady=(0, 6))

        row = ctk.CTkFrame(self, fg_color="transparent")
        self.entry = ctk.CTkEntry(
            row, textvariable=self._path, placeholder_text="No directory selected"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            row, text="Browse", width=90, command=self._browse,
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
        ).pack(side="right")
        row.pack(fill="x")

        self._try_enable_dnd()

    def _try_enable_dnd(self):
        if not _HAS_DND:
            return
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        paths = _parse_drop_paths(event.data)
        if paths:
            p = Path(paths[0])
            self._path.set(str(p if p.is_dir() else p.parent))

    def _browse(self):
        path = filedialog.askdirectory()
        if path:
            self._path.set(path)

    def get(self) -> str:
        return self._path.get().strip()

    def set(self, path: str):
        self._path.set(path)


class MultiFileInput(ctk.CTkFrame):
    """Multi-file selector with file list display and optional drag-and-drop."""

    def __init__(self, parent, label: str, filetypes: list = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.filetypes = filetypes or [("All files", "*.*")]
        self._paths: List[str] = []

        ctk.CTkLabel(
            self, text=label, font=("", 13, "bold"), anchor="w"
        ).pack(fill="x", pady=(0, 6))

        self.textbox = ctk.CTkTextbox(
            self, height=80, state="disabled", font=("", 12), corner_radius=6
        )
        self.textbox.pack(fill="x", pady=(0, 6))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkButton(
            btn_row, text="Add Files", width=100, command=self._add,
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            btn_row, text="Clear All", width=100, command=self._clear,
            fg_color="transparent", hover_color=("gray85", "gray25"),
            text_color=("gray40", "gray60"),
            border_width=1, border_color=("gray70", "gray40"),
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            btn_row, text="0 files", font=("", 12), text_color="gray50"
        )
        self.count_label.pack(side="right")
        btn_row.pack(fill="x")

        self._try_enable_dnd()

    def _try_enable_dnd(self):
        if not _HAS_DND:
            return
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        for p in _parse_drop_paths(event.data):
            if p not in self._paths:
                self._paths.append(p)
        self._refresh()

    def _add(self):
        paths = filedialog.askopenfilenames(filetypes=self.filetypes)
        for p in paths:
            if p not in self._paths:
                self._paths.append(p)
        self._refresh()

    def _clear(self):
        self._paths.clear()
        self._refresh()

    def _refresh(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        for p in self._paths:
            self.textbox.insert("end", Path(p).name + "\n")
        self.textbox.configure(state="disabled")
        n = len(self._paths)
        self.count_label.configure(text=f"{n} file{'s' if n != 1 else ''}")

    def get(self) -> List[str]:
        return self._paths.copy()


class OutputFileInput(ctk.CTkFrame):
    """Optional output file selector with save dialog."""

    def __init__(self, parent, label: str, filetypes: list = None,
                 default_ext: str = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.filetypes = filetypes or [("All files", "*.*")]
        self.default_ext = default_ext
        self._path = StringVar()

        ctk.CTkLabel(
            self, text=label, font=("", 13), anchor="w",
            text_color=("gray40", "gray60"),
        ).pack(fill="x", pady=(0, 6))

        row = ctk.CTkFrame(self, fg_color="transparent")
        self.entry = ctk.CTkEntry(
            row, textvariable=self._path,
            placeholder_text="Auto-generated if empty",
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            row, text="Browse", width=90, command=self._browse,
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
        ).pack(side="right")
        row.pack(fill="x")

    def _browse(self):
        path = filedialog.asksaveasfilename(
            filetypes=self.filetypes, defaultextension=self.default_ext
        )
        if path:
            self._path.set(path)

    def get(self) -> Optional[str]:
        val = self._path.get().strip()
        return val if val else None


class ChoiceInput(ctk.CTkFrame):
    """Dropdown choice selector."""

    def __init__(self, parent, label: str, choices: list,
                 default: str = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._value = StringVar(value=default or (choices[0] if choices else ""))

        ctk.CTkLabel(
            self, text=label, font=("", 13), anchor="w"
        ).pack(side="left", padx=(0, 12))
        ctk.CTkOptionMenu(
            self, variable=self._value, values=choices, width=160
        ).pack(side="left")

    def get(self) -> str:
        return self._value.get()


class NumberInput(ctk.CTkFrame):
    """Numeric input with optional range clamping."""

    def __init__(self, parent, label: str, default: str = "",
                 min_val: float = None, max_val: float = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._value = StringVar(value=default)
        self.min_val = min_val
        self.max_val = max_val

        ctk.CTkLabel(
            self, text=label, font=("", 13), anchor="w"
        ).pack(side="left", padx=(0, 12))
        ctk.CTkEntry(
            self, textvariable=self._value, width=80, justify="center"
        ).pack(side="left")

    def get(self) -> Optional[float]:
        try:
            val = float(self._value.get())
            if self.min_val is not None:
                val = max(val, self.min_val)
            if self.max_val is not None:
                val = min(val, self.max_val)
            return val
        except (ValueError, TypeError):
            return None


class TextInput(ctk.CTkFrame):
    """Text input field."""

    def __init__(self, parent, label: str, placeholder: str = "", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._value = StringVar()

        ctk.CTkLabel(
            self, text=label, font=("", 13), anchor="w"
        ).pack(fill="x", pady=(0, 6))
        self.entry = ctk.CTkEntry(
            self, textvariable=self._value, placeholder_text=placeholder
        )
        self.entry.pack(fill="x")

    def get(self) -> str:
        return self._value.get().strip()


class CheckboxInput(ctk.CTkFrame):
    """Checkbox toggle."""

    def __init__(self, parent, label: str, default: bool = False, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._value = BooleanVar(value=default)
        ctk.CTkCheckBox(
            self, text=label, variable=self._value, font=("", 13)
        ).pack(anchor="w")

    def get(self) -> bool:
        return self._value.get()


class StatusBar(ctk.CTkFrame):
    """Status bar with progress indication and threaded task execution."""

    STATUS_COLORS = {
        "info":     ("gray50", "gray50"),
        "success":  ("#27ae60", "#2ecc71"),
        "error":    ("#c0392b", "#e74c3c"),
        "progress": ("#2980b9", "#3498db"),
    }
    STATUS_ICONS = {"info": "", "success": "\u2713", "error": "\u2717", "progress": "\u27f3"}

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", height=3)

        self._row = ctk.CTkFrame(self, fg_color="transparent")
        self.status_icon = ctk.CTkLabel(self._row, text="", width=20, font=("", 14))
        self.status_icon.pack(side="left", padx=(0, 8))
        self.status_label = ctk.CTkLabel(
            self._row, text="Ready", font=("", 13), anchor="w", text_color="gray50"
        )
        self.status_label.pack(side="left", fill="x", expand=True)

        self._reveal_btn = ctk.CTkButton(
            self._row, text=_reveal_label(), width=120, height=26,
            font=("", 12), corner_radius=6,
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            text_color=("gray10", "gray90"),
        )
        # Packed on demand — hidden until a path is available

        self._row.pack(fill="x")

    def set_status(self, message: str, status_type: str = "info") -> None:
        color = self.STATUS_COLORS.get(status_type, self.STATUS_COLORS["info"])
        icon = self.STATUS_ICONS.get(status_type, "")

        self.status_icon.configure(text=icon, text_color=color)
        self.status_label.configure(text=message, text_color=color)
        self._reveal_btn.pack_forget()

        if status_type == "progress":
            self.progress.pack(fill="x", pady=(0, 8), before=self._row)
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.pack_forget()

    def _set_success_with_path(self, message: str, path: str) -> None:
        self.set_status(message, "success")
        self._reveal_btn.configure(command=lambda p=path: _reveal_path(p))
        self._reveal_btn.pack(side="right", padx=(8, 0))

    def run_task(self, task_fn: Callable, success_msg: str, error_prefix: str = "Error") -> None:
        """Execute task_fn on a background thread with automatic status updates.

        task_fn may return:
        - a string  → used as the status message
        - a (str, path) tuple → status message + clickable "Show in Finder" button
        - None → falls back to success_msg
        """
        self.set_status("Processing...", "progress")

        def wrapper():
            try:
                result = task_fn()
                if isinstance(result, tuple) and len(result) == 2:
                    msg, path = result
                    self.after(0, lambda m=msg, p=str(path): self._set_success_with_path(m, p))
                else:
                    msg = result if isinstance(result, str) else success_msg
                    self.after(0, lambda m=msg: self.set_status(m, "success"))
            except SystemExit as e:
                msg = f"{error_prefix}: process exited with code {e.code}"
                self.after(0, lambda m=msg: self.set_status(m, "error"))
            except Exception as e:
                msg = f"{error_prefix}: {e}"
                self.after(0, lambda m=msg: self.set_status(m, "error"))

        threading.Thread(target=wrapper, daemon=True).start()
