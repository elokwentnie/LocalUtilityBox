"""File Management Tool definitions."""
import customtkinter as ctk
from pathlib import Path

from ..widgets import (
    FileInput, DirectoryInput, MultiFileInput, OutputFileInput,
    ChoiceInput, NumberInput, TextInput, CheckboxInput,
)
from ..utils import validate_file_path

from file_management.merge_pdf import merge_pdf
from file_management.split_pdf import split_pdf
from file_management.add_watermark import add_watermark
from file_management.compress_pdf import compress_pdf
from file_management.rotate_pdf import rotate_pdf
from file_management.doc_to_pdf import doc_to_pdf
from file_management.pdf_to_doc import pdf_to_docx
from file_management.pdf_to_png import pdf_to_png
from file_management.pdf_to_jpg import pdf_to_jpg
from file_management.csv_to_excel import csv_to_excel
from file_management.excel_to_csv import excel_to_csv
from file_management.csv_to_json import csv_to_json
from file_management.json_to_csv import json_to_csv


# ---------------------------------------------------------------------------
# Build functions
# ---------------------------------------------------------------------------

def build_merge_pdf(parent, status_bar):
    files_in = MultiFileInput(parent, "Input PDF Files", [("PDF files", "*.pdf")])
    files_in.pack(fill="x", pady=(0, 12))

    dir_in = DirectoryInput(parent, "Or Select Directory")
    dir_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 24))

    def execute():
        files = files_in.get()
        directory = dir_in.get()
        if not files and not directory:
            return status_bar.set_status(
                "Please select files or a directory", "error"
            )
        out = file_out.get()

        def task():
            if files:
                targets = [Path(f) for f in files]
            else:
                targets = sorted(Path(directory).glob("*.pdf"))
            if not targets:
                raise ValueError("No PDF files found")
            out_path = Path(out) if out else None
            merge_pdf(targets, out_path)
            dest = out_path or Path(targets[0]).parent
            return (f"Merged {len(targets)} PDFs \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully merged PDF files!")

    ctk.CTkButton(
        parent, text="Merge PDFs", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_split_pdf(parent, status_bar):
    file_in = FileInput(parent, "Input PDF File", [("PDF files", "*.pdf")])
    file_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 16))

    parts = NumberInput(
        parent, "Number of Parts (leave empty for individual pages)", ""
    )
    parts.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, [".pdf"])
        if not valid:
            return status_bar.set_status(err, "error")
        parts_val = parts.get()
        od = out_dir.get() or None

        def task():
            from file_management.split_pdf import get_splitting_parts
            from PyPDF2 import PdfReader

            split_parts = None
            if parts_val:
                reader = PdfReader(str(inp))
                pdf_len = len(reader.pages)
                num = int(parts_val)
                if num <= pdf_len:
                    split_parts = get_splitting_parts(pdf_len, num)
            split_pdf(Path(inp), split_parts, output_dir=od)
            dest = od or str(Path(inp).parent)
            return (f"Split PDF \u2192 {dest}", dest)

        status_bar.run_task(task, "Successfully split PDF!")

    ctk.CTkButton(
        parent, text="Split PDF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_watermark(parent, status_bar):
    file_in = FileInput(parent, "Input PDF File", [("PDF files", "*.pdf")])
    file_in.pack(fill="x", pady=(0, 16))

    wm_in = FileInput(parent, "Watermark PDF File", [("PDF files", "*.pdf")])
    wm_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 16))

    pages = TextInput(
        parent, "Page Indices",
        placeholder="Comma-separated (e.g. 0,1,3) \u2014 leave empty for all pages",
    )
    pages.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        wm = wm_in.get()
        if not inp or not wm:
            return status_bar.set_status(
                "Please select both input and watermark files", "error"
            )
        for path, exts, label in [
            (inp, [".pdf"], "Input"),
            (wm, [".pdf"], "Watermark"),
        ]:
            valid, err = validate_file_path(path, exts)
            if not valid:
                return status_bar.set_status(f"{label}: {err}", "error")

        pages_str = pages.get()
        if pages_str:
            try:
                page_list = [int(p.strip()) for p in pages_str.split(",")]
            except ValueError:
                return status_bar.set_status(
                    "Invalid page indices \u2014 use comma-separated numbers", "error"
                )
        else:
            page_list = "ALL"

        out = file_out.get()
        out_path = Path(out) if out else Path(inp).with_stem(f"{Path(inp).stem}-watermarked")

        def task():
            add_watermark(Path(inp), Path(wm), page_list, output_file=out_path)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully added watermark!")

    ctk.CTkButton(
        parent, text="Add Watermark", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def _build_pdf_to_image(parent, status_bar, convert_fn, fmt_upper):
    file_in = FileInput(parent, "Input PDF File", [("PDF files", "*.pdf")])
    file_in.pack(fill="x", pady=(0, 16))

    out_dir = DirectoryInput(parent, "Output Directory (optional)")
    out_dir.pack(fill="x", pady=(0, 16))

    zip_cb = CheckboxInput(parent, "Zip output files")
    zip_cb.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, [".pdf"])
        if not valid:
            return status_bar.set_status(err, "error")
        od = out_dir.get() or None

        def task():
            convert_fn(Path(inp), zip_cb.get(), output_dir=od)
            dest = od or str(Path(inp).parent)
            return (f"Converted PDF to {fmt_upper} \u2192 {dest}", dest)

        status_bar.run_task(task, f"Successfully converted PDF to {fmt_upper}!")

    ctk.CTkButton(
        parent, text="Convert", height=40, font=("", 14, "bold"), command=execute
    ).pack(fill="x", pady=(8, 0))


def build_pdf_to_png(parent, status_bar):
    _build_pdf_to_image(parent, status_bar, pdf_to_png, "PNG")


def build_pdf_to_jpg(parent, status_bar):
    _build_pdf_to_image(parent, status_bar, pdf_to_jpg, "JPG")


def _build_doc_converter(parent, status_bar, label_in, ftypes_in, exts_in,
                          label_out, ftypes_out, ext_out, convert_fn, msg):
    file_in = FileInput(parent, label_in, ftypes_in)
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(parent, label_out, ftypes_out, ext_out)
    file_out.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, exts_in)
        if not valid:
            return status_bar.set_status(err, "error")
        out = file_out.get()
        out_path = Path(out) if out else Path(inp).with_suffix(ext_out)

        def task():
            convert_fn(Path(inp), out_path)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, msg)

    ctk.CTkButton(
        parent, text="Convert", height=40, font=("", 14, "bold"), command=execute
    ).pack(fill="x", pady=(8, 0))


def build_doc_to_pdf(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input DOC/DOCX File", [("Word files", "*.doc *.docx")], [".doc", ".docx"],
        "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf",
        doc_to_pdf, "Successfully converted to PDF!",
    )


def build_pdf_to_doc(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input PDF File", [("PDF files", "*.pdf")], [".pdf"],
        "Output DOCX File (optional)", [("Word files", "*.docx")], ".docx",
        pdf_to_docx, "Successfully converted to DOCX!",
    )


def build_compress_pdf(parent, status_bar):
    file_in = FileInput(parent, "Input PDF File", [("PDF files", "*.pdf")])
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 16))

    power = ChoiceInput(
        parent, "Compression Level",
        ["1 - Light", "2 - Medium", "3 - Maximum"], "2 - Medium",
    )
    power.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, [".pdf"])
        if not valid:
            return status_bar.set_status(err, "error")
        out = file_out.get()
        p = int(power.get()[0])
        out_path = Path(out) if out else Path(inp).with_stem(f"{Path(inp).stem}-compressed")

        def task():
            compress_pdf(Path(inp), out_path, p)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully compressed PDF!")

    ctk.CTkButton(
        parent, text="Compress PDF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_rotate_pdf(parent, status_bar):
    file_in = FileInput(parent, "Input PDF File", [("PDF files", "*.pdf")])
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output PDF File (optional)", [("PDF files", "*.pdf")], ".pdf"
    )
    file_out.pack(fill="x", pady=(0, 16))

    rotation = ChoiceInput(
        parent, "Rotation", ["90°", "180°", "270°"], "90°"
    )
    rotation.pack(fill="x", pady=(0, 8))

    pages_input = TextInput(
        parent, "Pages to Rotate",
        placeholder="Comma-separated 0-based indices (leave empty for all)",
    )
    pages_input.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status("Please select an input file", "error")
        valid, err = validate_file_path(inp, [".pdf"])
        if not valid:
            return status_bar.set_status(err, "error")
        out = file_out.get()
        deg = int(rotation.get().replace("°", ""))
        pages_str = pages_input.get()
        page_list = None
        if pages_str:
            try:
                page_list = [int(p.strip()) for p in pages_str.split(",")]
            except ValueError:
                return status_bar.set_status(
                    "Invalid page indices — use comma-separated numbers", "error"
                )
        out_path = Path(out) if out else Path(inp).with_stem(f"{Path(inp).stem}-rotated")

        def task():
            rotate_pdf(Path(inp), deg, page_list, out_path)
            return (f"Saved to {out_path}", out_path)

        status_bar.run_task(task, "Successfully rotated PDF pages!")

    ctk.CTkButton(
        parent, text="Rotate Pages", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_csv_to_excel(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input CSV File", [("CSV files", "*.csv")], [".csv"],
        "Output Excel File (optional)", [("Excel files", "*.xlsx")], ".xlsx",
        csv_to_excel, "Successfully converted CSV to Excel!",
    )


def build_excel_to_csv(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input Excel File", [("Excel files", "*.xlsx *.xls")], [".xlsx", ".xls"],
        "Output CSV File (optional)", [("CSV files", "*.csv")], ".csv",
        excel_to_csv, "Successfully converted Excel to CSV!",
    )


def build_csv_to_json(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input CSV File", [("CSV files", "*.csv")], [".csv"],
        "Output JSON File (optional)", [("JSON files", "*.json")], ".json",
        csv_to_json, "Successfully converted CSV to JSON!",
    )


def build_json_to_csv(parent, status_bar):
    _build_doc_converter(
        parent, status_bar,
        "Input JSON File", [("JSON files", "*.json")], [".json"],
        "Output CSV File (optional)", [("CSV files", "*.csv")], ".csv",
        json_to_csv, "Successfully converted JSON to CSV!",
    )


# ---------------------------------------------------------------------------
# Exported section list
# ---------------------------------------------------------------------------

FILE_SECTIONS = [
    (
        "PDF OPERATIONS",
        [
            {
                "name": "Merge PDFs",
                "description": "Combine multiple PDF files into a single document",
                "build_fn": build_merge_pdf,
            },
            {
                "name": "Split PDF",
                "description": "Split a PDF into individual pages or equal parts",
                "build_fn": build_split_pdf,
            },
            {
                "name": "Add Watermark",
                "description": "Overlay a watermark PDF onto selected pages",
                "build_fn": build_watermark,
            },
            {
                "name": "Compress PDF",
                "description": "Reduce PDF file size by compressing content streams",
                "build_fn": build_compress_pdf,
            },
            {
                "name": "Rotate Pages",
                "description": "Rotate selected PDF pages by 90°, 180°, or 270°",
                "build_fn": build_rotate_pdf,
            },
            {
                "name": "PDF \u2192 PNG",
                "description": "Convert PDF pages to PNG images",
                "build_fn": build_pdf_to_png,
            },
            {
                "name": "PDF \u2192 JPG",
                "description": "Convert PDF pages to JPG images",
                "build_fn": build_pdf_to_jpg,
            },
        ],
    ),
    (
        "DOCUMENTS",
        [
            {
                "name": "DOC \u2192 PDF",
                "description": "Convert Word documents to PDF format",
                "build_fn": build_doc_to_pdf,
            },
            {
                "name": "PDF \u2192 DOC",
                "description": "Convert PDF documents to editable Word format",
                "build_fn": build_pdf_to_doc,
            },
        ],
    ),
    (
        "DATA FORMATS",
        [
            {
                "name": "CSV \u2192 Excel",
                "description": "Convert CSV files to Excel spreadsheet format",
                "build_fn": build_csv_to_excel,
            },
            {
                "name": "Excel \u2192 CSV",
                "description": "Convert Excel spreadsheets to CSV format",
                "build_fn": build_excel_to_csv,
            },
            {
                "name": "CSV \u2192 JSON",
                "description": "Convert CSV data to JSON format",
                "build_fn": build_csv_to_json,
            },
            {
                "name": "JSON \u2192 CSV",
                "description": "Convert JSON data to CSV tabular format",
                "build_fn": build_json_to_csv,
            },
        ],
    ),
]
