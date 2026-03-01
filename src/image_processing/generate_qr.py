import argparse
from pathlib import Path

try:
    import qrcode
except ImportError:
    qrcode = None


def generate_qr(
    data: str,
    output_file: Path = None,
    size: int = 10,
    border: int = 4,
) -> None:
    """Generate a QR code image from text or a URL."""
    if qrcode is None:
        raise ImportError(
            "qrcode is required for QR generation. "
            "Install it with: pip install qrcode[pil]"
        )

    if output_file is None:
        safe = "".join(c if c.isalnum() else "_" for c in data[:30])
        output_file = Path(f"qr_{safe}.png")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(output_file))
    print(f"QR code saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate a QR code image.")
    parser.add_argument("data", help="Text or URL to encode")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output image file path"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=10,
        help="Box size in pixels (default: 10)",
    )
    parser.add_argument(
        "-b", "--border", type=int, default=4,
        help="Border width in boxes (default: 4)",
    )
    args = parser.parse_args()

    generate_qr(args.data, args.output, args.size, args.border)


if __name__ == "__main__":
    main()
