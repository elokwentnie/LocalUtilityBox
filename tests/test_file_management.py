"""Smoke tests for file management utilities."""
from pathlib import Path

from file_management.merge_pdf import merge_pdf
from file_management.split_pdf import split_pdf
from file_management.compress_pdf import compress_pdf
from file_management.rotate_pdf import rotate_pdf, reorder_pdf


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
