"""Tests for file management utilities."""
import pytest
from PyPDF2 import PdfReader

from file_management.merge_pdf import merge_pdf
from file_management.split_pdf import split_pdf
from file_management.compress_pdf import compress_pdf
from file_management.json_to_csv import json_to_csv
from file_management.rotate_pdf import rotate_pdf, reorder_pdf


# ---------------------------------------------------------------------------
# Happy-path smoke tests
# ---------------------------------------------------------------------------

def test_merge_pdf(tmp_pdf, tmp_path):
    out = tmp_path / "merged.pdf"
    merge_pdf([tmp_pdf], out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_split_pdf_individual_pages(tmp_pdf, tmp_path):
    out_dir = tmp_path / "split"
    out_dir.mkdir()
    split_pdf(tmp_pdf, output_dir=out_dir)
    pages = list(out_dir.glob("*.pdf"))
    assert len(pages) == 2


def test_split_pdf_default_location(tmp_pdf):
    split_pdf(tmp_pdf)
    pages = list(tmp_pdf.parent.glob("*_page_*.pdf"))
    assert len(pages) == 2


def test_compress_pdf(tmp_pdf, tmp_path):
    out = tmp_path / "compressed.pdf"
    compress_pdf(tmp_pdf, out, power=2)
    assert out.exists()
    assert out.stat().st_size > 0


def test_compress_pdf_default_location(tmp_pdf):
    compress_pdf(tmp_pdf)
    out = tmp_pdf.with_stem(f"{tmp_pdf.stem}-compressed")
    assert out.exists()


def test_rotate_pdf(tmp_pdf, tmp_path):
    out = tmp_path / "rotated.pdf"
    rotate_pdf(tmp_pdf, 90, output_file=out)
    assert out.exists()


def test_reorder_pdf(tmp_pdf, tmp_path):
    out = tmp_path / "reordered.pdf"
    reorder_pdf(tmp_pdf, [1, 0], output_file=out)
    assert out.exists()


# ---------------------------------------------------------------------------
# Output integrity — verify pages with PdfReader
# ---------------------------------------------------------------------------

def test_merge_multiple_pdfs_page_count(tmp_pdf, tmp_path):
    """Merging two 2-page PDFs should produce a 4-page PDF."""
    out = tmp_path / "merged.pdf"
    merge_pdf([tmp_pdf, tmp_pdf], out)
    reader = PdfReader(out)
    assert len(reader.pages) == 4


def test_split_pdf_page_count(tmp_pdf, tmp_path):
    """Each split file should be a valid single-page PDF."""
    out_dir = tmp_path / "split"
    out_dir.mkdir()
    split_pdf(tmp_pdf, output_dir=out_dir)
    for page_file in out_dir.glob("*.pdf"):
        reader = PdfReader(page_file)
        assert len(reader.pages) == 1


def test_rotate_pdf_all_angles(tmp_pdf, tmp_path):
    """Rotation should succeed for all standard angles."""
    for angle in (90, 180, 270):
        out = tmp_path / f"rotated_{angle}.pdf"
        rotate_pdf(tmp_pdf, angle, output_file=out)
        assert out.exists()


def test_reorder_pdf_same_order(tmp_pdf, tmp_path):
    """Reordering with unchanged order should still produce a valid PDF."""
    out = tmp_path / "same_order.pdf"
    reorder_pdf(tmp_pdf, [0, 1], output_file=out)
    reader = PdfReader(out)
    assert len(reader.pages) == 2


def test_reorder_pdf_single_page(tmp_path):
    """Reordering a single-page PDF should work without error."""
    from PyPDF2 import PdfWriter
    p = tmp_path / "single.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with open(p, "wb") as f:
        writer.write(f)
    out = tmp_path / "reordered_single.pdf"
    reorder_pdf(p, [0], output_file=out)
    assert out.exists()


def test_json_to_csv_list_of_dicts(tmp_path):
    src = tmp_path / "rows.json"
    src.write_text('[{"a":1,"b":"x"},{"a":2,"b":"y"}]', encoding="utf-8")
    out = tmp_path / "rows.csv"
    json_to_csv(src, out)
    content = out.read_text(encoding="utf-8")
    assert "a,b" in content
    assert "1,x" in content


def test_json_to_csv_single_nested_object(tmp_path):
    src = tmp_path / "nested.json"
    src.write_text('{"user":{"name":"Ana","age":30}}', encoding="utf-8")
    out = tmp_path / "nested.csv"
    json_to_csv(src, out)
    content = out.read_text(encoding="utf-8")
    assert "user.name" in content
    assert "user.age" in content


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

def test_merge_pdf_missing_file(tmp_path):
    missing = tmp_path / "nonexistent.pdf"
    out = tmp_path / "out.pdf"
    with pytest.raises(Exception):
        merge_pdf([missing], out)


def test_split_pdf_corrupt_file(tmp_path):
    bad = tmp_path / "corrupt.pdf"
    bad.write_bytes(b"%PDF-1.4 corrupt content")
    with pytest.raises(Exception):
        split_pdf(bad, output_dir=tmp_path)
