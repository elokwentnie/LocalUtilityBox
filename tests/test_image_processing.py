"""Smoke tests for image processing utilities."""
from pathlib import Path

from image_processing.webp_to_jpg import webp_to_jpg
from image_processing.webp_to_png import webp_to_png
from image_processing.jpg_to_png import jpg_to_png
from image_processing.png_to_jpg import png_to_jpg
from image_processing.img_to_pdf import img_to_pdf
from image_processing.img_to_greyscale import img_to_greyscale
from image_processing.reduce_img_size import reduce_img_size


def test_webp_to_jpg(tmp_webp, tmp_path):
    out = tmp_path / "out.jpg"
    webp_to_jpg(tmp_webp, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_webp_to_png(tmp_webp, tmp_path):
    out = tmp_path / "out.png"
    webp_to_png(tmp_webp, out)
    assert out.exists()


def test_jpg_to_png(tmp_image, tmp_path):
    out = tmp_path / "out.png"
    jpg_to_png(tmp_image, out)
    assert out.exists()


def test_png_to_jpg(tmp_png, tmp_path):
    out = tmp_path / "out.jpg"
    png_to_jpg(tmp_png, out)
    assert out.exists()


def test_img_to_pdf(tmp_image, tmp_path):
    out = tmp_path / "out.pdf"
    img_to_pdf(tmp_image, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_img_to_greyscale(tmp_image, tmp_path):
    out = tmp_path / "grey.jpg"
    img_to_greyscale(tmp_image, out)
    assert out.exists()


def test_reduce_img_size(tmp_image, tmp_path):
    out_dir = tmp_path / "reduced"
    out_dir.mkdir()
    reduce_img_size([tmp_image], scale_factor=0.5, quality=80, output_dir=out_dir)
    results = list(out_dir.glob("*.jpg"))
    assert len(results) == 1


def test_reduce_img_size_default_location(tmp_image):
    reduce_img_size([tmp_image], scale_factor=0.5, quality=80)
    out = tmp_image.with_stem(f"{tmp_image.stem}-reduced").with_suffix(".jpg")
    assert out.exists()
