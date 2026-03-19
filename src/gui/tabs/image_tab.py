"""Image Processing Tool definitions."""
import customtkinter as ctk
from pathlib import Path
from PIL import Image

from ..widgets import (
    FileInput, DirectoryInput, MultiFileInput, OutputFileInput,
    ChoiceInput, NumberInput, CheckboxInput,
)
from ..utils import validate_file_path

from image_processing.webp_to_jpg import webp_to_jpg
from image_processing.webp_to_png import webp_to_png
from image_processing.jpg_to_png import jpg_to_png
from image_processing.png_to_jpg import png_to_jpg
from image_processing.tiff_to_jpg import tiff_to_jpg
from image_processing.heic_to_jpg import heic_to_jpg
from image_processing.img_to_pdf import img_to_pdf
from image_processing.img_to_greyscale import img_to_greyscale
from image_processing.reduce_img_size import reduce_img_size
try:
    from image_processing.remove_background import remove_background
    _HAS_REMBG = True
except ImportError:
    _HAS_REMBG = False
from image_processing.long_png_to_pdf import long_png_to_pdf
from image_processing.extract_img_metadata import extract_img_metadata
from image_processing.extract_text_from_img import extract_text_from_img
from image_processing.photos_to_gif import photos_to_gif
try:
    from image_processing.generate_qr import generate_qr
    _HAS_QR = True
except ImportError:
    _HAS_QR = False


# ---------------------------------------------------------------------------
# Unified format conversion helpers
# ---------------------------------------------------------------------------

def _convert_file_to_jpg(file_path: str, quality: int = 95, output_dir=None):
    """Convert a single file to JPG, dispatching to the right function by extension."""
    p = Path(file_path)
    ext = p.suffix.lower()
    out_path = Path(output_dir) / f"{p.stem}.jpg" if output_dir else None

    if ext == ".webp":
        webp_to_jpg(p, output_file=out_path)
    elif ext in (".heic", ".heif"):
        heic_to_jpg([str(p)], output_dir, quality)
    elif ext == ".png":
        png_to_jpg(p, output_file=out_path, quality=quality)
    elif ext in (".tiff", ".tif"):
        tiff_to_jpg(p, output_file=out_path, quality=quality)
    elif ext in (".jpg", ".jpeg"):
        print(f"Skipping '{p.name}': already a JPG")
    else:
        out = out_path or p.with_suffix(".jpg")
        img = Image.open(p)
        if img.mode in ("RGBA", "LA", "PA", "P"):
            img = img.convert("RGB")
        img.save(out, "JPEG", quality=quality)
        print(f"Conversion successful: {out}")


def _convert_file_to_png(file_path: str, quality: int = 95, output_dir=None):
    """Convert a single file to PNG, dispatching to the right function by extension."""
    p = Path(file_path)
    ext = p.suffix.lower()
    out_path = Path(output_dir) / f"{p.stem}.png" if output_dir else None

    if ext == ".webp":
        webp_to_png(p, output_file=out_path)
    elif ext in (".jpg", ".jpeg"):
        jpg_to_png(p, output_file=out_path, quality=quality)
    elif ext == ".png":
        print(f"Skipping '{p.name}': already a PNG")
    else:
        out = out_path or p.with_suffix(".png")
        img = Image.open(p)
        img.save(out, "PNG")
        print(f"Conversion successful: {out}")


# ---------------------------------------------------------------------------
# Build functions — each creates the tool UI inside `parent` and wires up
# execution through `status_bar.run_task()`.
# ---------------------------------------------------------------------------

def build_convert_to_jpg(parent, status_bar):
    files_in = MultiFileInput(
        parent, "Input Image Files", [("All files", "*.*")]
    )
    files_in.pack(fill="x", pady=(0, 12))

    dir_in = DirectoryInput(parent, "Or Select Directory")
    dir_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 16))

    quality = NumberInput(parent, "Quality (1-100)", "95", 1, 100)
    quality.pack(fill="x", pady=(0, 24))

    IMAGE_EXTS = {
        ".webp", ".png", ".heic", ".heif", ".tiff", ".tif",
        ".bmp", ".gif", ".ico", ".webp",
    }

    def execute():
        files = files_in.get()
        directory = dir_in.get()
        if not files and not directory:
            return status_bar.set_status(
                "Please select files or a directory", "error"
            )
        q = int(quality.get() or 95)
        od = out_dir.get() or None

        def task():
            targets = list(files) if files else [
                str(f) for f in Path(directory).iterdir()
                if f.suffix.lower() in IMAGE_EXTS
            ]
            if not targets:
                raise ValueError("No supported image files found")
            if od:
                Path(od).mkdir(parents=True, exist_ok=True)
            for f in targets:
                _convert_file_to_jpg(f, q, output_dir=od)
            dest = od or str(Path(targets[0]).parent)
            return (f"Converted {len(targets)} file(s) to JPG \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully converted to JPG!")

    ctk.CTkButton(
        parent, text="Convert to JPG", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_convert_to_png(parent, status_bar):
    files_in = MultiFileInput(
        parent, "Input Image Files", [("All files", "*.*")]
    )
    files_in.pack(fill="x", pady=(0, 12))

    dir_in = DirectoryInput(parent, "Or Select Directory")
    dir_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 16))

    quality = NumberInput(parent, "Quality (1-100)", "95", 1, 100)
    quality.pack(fill="x", pady=(0, 24))

    IMAGE_EXTS = {
        ".webp", ".jpg", ".jpeg", ".tiff", ".tif",
        ".bmp", ".gif", ".ico", ".heic", ".heif",
    }

    def execute():
        files = files_in.get()
        directory = dir_in.get()
        if not files and not directory:
            return status_bar.set_status(
                "Please select files or a directory", "error"
            )
        q = int(quality.get() or 95)
        od = out_dir.get() or None

        def task():
            targets = list(files) if files else [
                str(f) for f in Path(directory).iterdir()
                if f.suffix.lower() in IMAGE_EXTS
            ]
            if not targets:
                raise ValueError("No supported image files found")
            if od:
                Path(od).mkdir(parents=True, exist_ok=True)
            for f in targets:
                _convert_file_to_png(f, q, output_dir=od)
            dest = od or str(Path(targets[0]).parent)
            return (f"Converted {len(targets)} file(s) to PNG \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully converted to PNG!")

    ctk.CTkButton(
        parent, text="Convert to PNG", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_img_to_pdf(parent, status_bar):
    files_in = MultiFileInput(
        parent, "Input Image Files",
        [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")],
    )
    files_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 24))

    def execute():
        files = files_in.get()
        if not files:
            return status_bar.set_status(
                "Please select at least one image file", "error"
            )
        out = file_out.get()

        def task():
            if len(files) == 1:
                out_path = Path(out) if out else Path(files[0]).with_suffix(".pdf")
                img_to_pdf(Path(files[0]), out_path)
            else:
                import img2pdf
                out_path = Path(out) if out else Path(files[0]).parent / "combined_images.pdf"
                with open(out_path, "wb") as fh:
                    fh.write(img2pdf.convert([str(Path(f)) for f in files]))
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully created PDF from images!")

    ctk.CTkButton(
        parent, text="Convert to PDF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_greyscale(parent, status_bar):
    file_in = FileInput(
        parent, "Input Image File",
        [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")],
    )
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output File (optional)", [("Image files", "*.jpg *.png")]
    )
    file_out.pack(fill="x", pady=(0, 16))

    quality = NumberInput(parent, "Quality (0-100)", "85", 0, 100)
    quality.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        out = file_out.get()
        q = quality.get() or 85
        out_path = Path(out) if out else Path(inp).with_stem(f"{Path(inp).stem}-greyscale")

        def task():
            img_to_greyscale(Path(inp), out_path, int(q))
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully converted to greyscale!")

    ctk.CTkButton(
        parent, text="Convert", height=40, font=("", 14, "bold"), command=execute
    ).pack(fill="x", pady=(8, 0))


def build_long_png_to_pdf(parent, status_bar):
    file_in = FileInput(parent, "Input PNG File", [("PNG files", "*.png")])
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 16))

    page_size = ChoiceInput(parent, "Page Size", ["a4", "letter", "legal"], "a4")
    page_size.pack(fill="x", pady=(0, 8))

    overlap = NumberInput(parent, "Overlap Pixels (0+)", "0", 0)
    overlap.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, [".png"])
        if not valid:
            return status_bar.set_status(err, "error")
        out = file_out.get()
        ov = int(overlap.get() or 0)
        out_path = Path(out) if out else Path(inp).with_suffix(".pdf")

        def task():
            long_png_to_pdf(Path(inp), out_path, page_size.get(), ov)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully split long PNG into multi-page PDF!")

    ctk.CTkButton(
        parent, text="Convert to PDF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_reduce_size(parent, status_bar):
    files_in = MultiFileInput(
        parent, "Input Image Files", [("JPG files", "*.jpg *.jpeg")]
    )
    files_in.pack(fill="x", pady=(0, 12))

    dir_in = DirectoryInput(parent, "Or Select Directory")
    dir_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 16))

    scale = NumberInput(parent, "Scale Percentage (1-100)", "50", 1, 100)
    scale.pack(fill="x", pady=(0, 8))

    quality = NumberInput(parent, "Quality (1-100)", "85", 1, 100)
    quality.pack(fill="x", pady=(0, 24))

    def execute():
        files = files_in.get()
        directory = dir_in.get()
        if not files and not directory:
            return status_bar.set_status(
                "Please select files or a directory", "error"
            )
        s = scale.get() or 50
        q = quality.get() or 85
        od = out_dir.get() or None

        def task():
            if files:
                targets = [Path(f) for f in files]
                reduce_img_size(targets, s / 100, int(q), output_dir=od)
            else:
                p = Path(directory)
                targets = list(p.glob("*.jpg")) + list(p.glob("*.jpeg"))
                if targets:
                    reduce_img_size(targets, s / 100, int(q), output_dir=od)
            dest = od or str(Path(targets[0]).parent) if targets else ""
            return (f"Reduced {len(targets)} file(s) \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully reduced image sizes!")

    ctk.CTkButton(
        parent, text="Reduce Size", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_remove_bg(parent, status_bar):
    if not _HAS_REMBG:
        ctk.CTkLabel(
            parent,
            text="The rembg package is not installed.\n"
                 "Install it with:  pip install rembg[cpu]",
            font=("", 14), text_color="gray50", justify="left",
        ).pack(fill="x", pady=(8, 0))
        return

    files_in = MultiFileInput(
        parent, "Input Image Files",
        [("Image files", "*.jpg *.jpeg *.png")],
    )
    files_in.pack(fill="x", pady=(0, 12))

    dir_in = DirectoryInput(parent, "Or Select Directory")
    dir_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 24))

    def execute():
        files = files_in.get()
        directory = dir_in.get()
        if not files and not directory:
            return status_bar.set_status(
                "Please select files or a directory", "error"
            )
        od = out_dir.get() or None

        def task():
            if files:
                targets = [Path(f) for f in files]
                remove_background(targets, output_dir=od)
            else:
                p = Path(directory)
                targets = (
                    list(p.glob("*.jpg"))
                    + list(p.glob("*.jpeg"))
                    + list(p.glob("*.png"))
                )
                if targets:
                    remove_background(targets, output_dir=od)
            dest = od or str(Path(targets[0]).parent) if targets else ""
            return (f"Removed background from {len(targets)} file(s) \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully removed backgrounds!")

    ctk.CTkButton(
        parent, text="Remove Background", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_extract_metadata(parent, status_bar):
    file_in = FileInput(
        parent, "Input Image File",
        [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")],
    )
    file_in.pack(fill="x", pady=(0, 16))

    save = CheckboxInput(parent, "Save metadata to file")
    save.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        status_bar.run_task(
            lambda: extract_img_metadata(Path(inp), save.get()),
            "Successfully extracted metadata!",
        )

    ctk.CTkButton(
        parent, text="Extract Metadata", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_extract_text(parent, status_bar):
    file_in = FileInput(
        parent, "Input Image File",
        [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")],
    )
    file_in.pack(fill="x", pady=(0, 16))

    save = CheckboxInput(parent, "Save extracted text to file")
    save.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        status_bar.run_task(
            lambda: extract_text_from_img(Path(inp), save.get()),
            "Successfully extracted text!",
        )

    ctk.CTkButton(
        parent, text="Extract Text", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_qr_code(parent, status_bar):
    if not _HAS_QR:
        ctk.CTkLabel(
            parent,
            text="The qrcode package is not installed.\n"
                 "Install it with:  pip install qrcode[pil]",
            font=("", 14), text_color="gray50", justify="left",
        ).pack(fill="x", pady=(8, 0))
        return

    from ..widgets import TextInput

    text_in = TextInput(parent, "Text or URL", placeholder="https://example.com")
    text_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output Image File (optional)",
        [("PNG files", "*.png")], ".png",
    )
    file_out.pack(fill="x", pady=(0, 16))

    size = NumberInput(parent, "Box Size (pixels)", "10", 1, 50)
    size.pack(fill="x", pady=(0, 24))

    def execute():
        data = text_in.get()
        if not data:
            return status_bar.set_status("Please enter text or a URL", "error")
        out = file_out.get()
        s = int(size.get() or 10)

        def task():
            import re
            if out:
                out_path = Path(out)
            else:
                safe = re.sub(r'[^\w\-.]', '_', data)[:50]
                out_path = Path(f"qr_{safe}.png")
            generate_qr(data, out_path, s)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully generated QR code!")

    ctk.CTkButton(
        parent, text="Generate QR Code", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_photos_to_gif(parent, status_bar):
    files_in = MultiFileInput(
        parent, "Input Image Files",
        [("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff *.tif")],
    )
    files_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output GIF File (optional)", [("GIF files", "*.gif")], ".gif"
    )
    file_out.pack(fill="x", pady=(0, 16))

    duration = NumberInput(parent, "Frame Duration (ms)", "200", 1)
    duration.pack(fill="x", pady=(0, 8))

    loop = NumberInput(parent, "Loop Count (0 = infinite)", "0", 0)
    loop.pack(fill="x", pady=(0, 24))

    def execute():
        files = files_in.get()
        if len(files) < 2:
            return status_bar.set_status("Please select at least 2 images", "error")

        out = file_out.get()
        d = int(duration.get() or 200)
        l = int(loop.get() or 0)

        def task():
            paths = [Path(f) for f in files]
            out_path = Path(out) if out else paths[0].with_name(f"{paths[0].stem}-animated.gif")
            photos_to_gif(paths, out_path, d, l)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully created GIF from photos!")

    ctk.CTkButton(
        parent, text="Create GIF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


# ---------------------------------------------------------------------------
# Exported section list consumed by main_gui.py
# ---------------------------------------------------------------------------

IMAGE_SECTIONS = [
    (
        "FORMAT CONVERSION",
        [
            {
                "name": "Convert to JPG",
                "description": "Convert any image (PNG, WebP, HEIC, TIFF, BMP, GIF, ...) to JPG",
                "build_fn": build_convert_to_jpg,
            },
            {
                "name": "Convert to PNG",
                "description": "Convert any image (JPG, WebP, TIFF, BMP, GIF, ...) to PNG",
                "build_fn": build_convert_to_png,
            },
        ],
    ),
    (
        "IMAGE PROCESSING",
        [
            {
                "name": "Image \u2192 PDF",
                "description": "Combine one or more images into a single PDF document",
                "build_fn": build_img_to_pdf,
            },
            {
                "name": "Long PNG \u2192 PDF",
                "description": "Split a long/tall PNG into a paginated multi-page PDF",
                "build_fn": build_long_png_to_pdf,
            },
            {
                "name": "Greyscale",
                "description": "Convert a colour image to greyscale with quality control",
                "build_fn": build_greyscale,
            },
            {
                "name": "Reduce Size",
                "description": "Batch reduce image dimensions and file size",
                "build_fn": build_reduce_size,
            },
            {
                "name": "Remove Background",
                "description": "Automatically remove the background from images (requires rembg)",
                "build_fn": build_remove_bg,
            },
        ],
    ),
    (
        "EXTRACTION",
        [
            {
                "name": "Image Metadata",
                "description": "Extract EXIF and other metadata from an image",
                "build_fn": build_extract_metadata,
            },
            {
                "name": "OCR Text",
                "description": "Extract text from an image using optical character recognition",
                "build_fn": build_extract_text,
            },
        ],
    ),
    (
        "GENERATE",
        [
            {
                "name": "QR Code",
                "description": "Generate a QR code image from text or a URL",
                "build_fn": build_qr_code,
            },
            {
                "name": "Photos -> GIF",
                "description": "Create an animated GIF from multiple photos",
                "build_fn": build_photos_to_gif,
            },
        ],
    ),
]
