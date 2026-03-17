"""Tests for image processing utilities."""
import pytest
from pathlib import Path
from PIL import Image, UnidentifiedImageError

from image_processing.webp_to_jpg import webp_to_jpg, has_transparency
from image_processing.webp_to_png import webp_to_png
from image_processing.jpg_to_png import jpg_to_png
from image_processing.png_to_jpg import png_to_jpg
from image_processing.img_to_pdf import img_to_pdf
from image_processing.img_to_greyscale import img_to_greyscale
from image_processing.reduce_img_size import reduce_img_size


# ---------------------------------------------------------------------------
# Happy-path smoke tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Output placed next to input when no output path given
# ---------------------------------------------------------------------------

def test_webp_to_jpg_default_output(tmp_webp):
    webp_to_jpg(tmp_webp)
    expected = tmp_webp.with_suffix(".jpg")
    assert expected.exists()


def test_img_to_greyscale_default_output(tmp_image):
    img_to_greyscale(tmp_image)
    expected = tmp_image.with_stem(f"{tmp_image.stem}-greyscale")
    assert expected.exists()


# ---------------------------------------------------------------------------
# Transparency handling
# ---------------------------------------------------------------------------

def test_webp_to_jpg_transparent_white_bg(tmp_path):
    """Transparent WebP should composite onto white when requested."""
    p = tmp_path / "transparent.webp"
    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    img.save(p, "WebP")
    out = tmp_path / "out.jpg"
    webp_to_jpg(p, out, background_color="white")
    assert out.exists()
    result = Image.open(out)
    assert result.mode == "RGB"


def test_webp_to_jpg_transparent_black_bg(tmp_path):
    p = tmp_path / "transparent.webp"
    Image.new("RGBA", (50, 50), (0, 0, 0, 0)).save(p, "WebP")
    out = tmp_path / "out.jpg"
    webp_to_jpg(p, out, background_color="black")
    assert out.exists()


def test_has_transparency_opaque(tmp_webp):
    assert has_transparency(tmp_webp) is False


def test_has_transparency_with_alpha(tmp_path):
    p = tmp_path / "alpha.webp"
    Image.new("RGBA", (10, 10), (100, 100, 100, 0)).save(p, "WebP")
    assert has_transparency(p) is True


# ---------------------------------------------------------------------------
# Output format derived from extension
# ---------------------------------------------------------------------------

def test_webp_to_jpg_non_jpg_extension_falls_back(tmp_webp):
    """If output extension is not .jpg/.jpeg, default to .jpg next to input."""
    out_wrong = tmp_webp.with_suffix(".png")  # wrong extension
    webp_to_jpg(tmp_webp, out_wrong)
    # Function should have saved to <stem>.jpg, not the wrong path
    expected = tmp_webp.with_suffix(".jpg")
    assert expected.exists()


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

def test_webp_to_jpg_missing_file(tmp_path):
    missing = tmp_path / "nonexistent.webp"
    with pytest.raises(FileNotFoundError):
        webp_to_jpg(missing, tmp_path / "out.jpg")


def test_webp_to_jpg_corrupt_file(tmp_path):
    bad = tmp_path / "corrupt.webp"
    bad.write_bytes(b"not an image")
    with pytest.raises(UnidentifiedImageError):
        webp_to_jpg(bad, tmp_path / "out.jpg")


def test_img_to_greyscale_corrupt_file(tmp_path):
    bad = tmp_path / "corrupt.jpg"
    bad.write_bytes(b"not an image")
    with pytest.raises(UnidentifiedImageError):
        img_to_greyscale(bad, tmp_path / "out.jpg")


def test_reduce_img_size_skips_corrupt_file(tmp_path):
    """reduce_img_size should skip unreadable files without raising."""
    bad = tmp_path / "bad.jpg"
    bad.write_bytes(b"not an image")
    # Should not raise — corrupt files are skipped with a printed warning
    reduce_img_size([bad], scale_factor=0.5, quality=80)


def test_reduce_img_size_multiple_files(tmp_image, tmp_path):
    """Multiple input files all get reduced."""
    img2 = tmp_path / "second.jpg"
    Image.new("RGB", (200, 150), color="blue").save(img2, "JPEG")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    reduce_img_size([tmp_image, img2], scale_factor=0.5, quality=80, output_dir=out_dir)
    assert len(list(out_dir.glob("*.jpg"))) == 2
