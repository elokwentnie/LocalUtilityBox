"""Master CLI entry point — lists all available localutilitybox tools."""


TOOLS = {
    "Image Processing": [
        ("webp_to_jpg",          "Convert WebP to JPG"),
        ("webp_to_png",          "Convert WebP to PNG"),
        ("jpg_to_png",           "Convert JPG/JPEG to PNG"),
        ("png_to_jpg",           "Convert PNG to JPG"),
        ("tiff_to_jpg",          "Convert TIFF to JPG"),
        ("heic_to_jpg",          "Convert HEIC photos to JPG"),
        ("img_to_pdf",           "Convert an image to PDF"),
        ("long_png_to_pdf",      "Split a long PNG into a multi-page PDF"),
        ("img_to_greyscale",     "Convert an image to greyscale"),
        ("reduce_img_size",      "Reduce image dimensions and file size"),
        ("remove_background",    "Remove background from images (requires rembg)"),
        ("extract_img_metadata", "Extract EXIF metadata from an image"),
        ("extract_text_from_img","OCR — extract text from an image"),
        ("generate_qr",          "Generate a QR code from text or a URL (requires qrcode)"),
        ("photos_to_gif",        "Create an animated GIF from multiple photos"),
    ],
    "PDF Operations": [
        ("merge_pdf",     "Merge multiple PDFs into one"),
        ("split_pdf",     "Split a PDF into parts or individual pages"),
        ("compress_pdf",  "Compress a PDF to reduce file size"),
        ("rotate_pdf",    "Rotate or reorder PDF pages"),
        ("add_watermark", "Add a watermark overlay to PDF pages"),
        ("pdf_to_png",    "Convert PDF pages to PNG images"),
        ("pdf_to_jpg",    "Convert PDF pages to JPG images"),
    ],
    "Document Conversion": [
        ("doc_to_pdf",  "Convert DOC/DOCX to PDF"),
        ("pdf_to_doc",  "Convert PDF to DOCX"),
    ],
    "Data Format Conversion": [
        ("csv_to_excel", "Convert CSV to Excel (.xlsx)"),
        ("excel_to_csv", "Convert Excel to CSV"),
        ("csv_to_json",  "Convert CSV to JSON"),
        ("json_to_csv",  "Convert JSON to CSV"),
    ],
    "Video / Audio": [
        ("extract_audio_from_video", "Extract audio track from a video"),
        ("video_to_gif",             "Convert a video clip to animated GIF"),
    ],
    "GUI": [
        ("localutilitybox-gui", "Launch the desktop GUI (alias: lub-gui)"),
    ],
}


def main():
    print()
    print("  localutilitybox — local file processing tools")
    print("  " + "=" * 47)
    print()
    for category, tools in TOOLS.items():
        print(f"  {category}")
        print(f"  {'-' * len(category)}")
        longest = max(len(name) for name, _ in tools)
        for name, desc in tools:
            print(f"    {name:<{longest}}   {desc}")
        print()
    print("  Run any command with --help for usage details.")
    print()


if __name__ == "__main__":
    main()
