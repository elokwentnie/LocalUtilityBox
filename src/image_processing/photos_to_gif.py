import argparse
import sys
from pathlib import Path

from PIL import Image


def photos_to_gif(
    input_files: list[Path],
    output_file: Path | None = None,
    duration_ms: int = 200,
    loop: int = 0,
) -> None:
    """Create an animated GIF from one or more photos."""
    if not input_files:
        raise ValueError("No input images provided.")

    if output_file is None:
        output_file = input_files[0].with_name(f"{input_files[0].stem}-animated.gif")
    elif output_file.suffix.lower() != ".gif":
        output_file = output_file.with_suffix(".gif")

    frames: list[Image.Image] = []
    base_size: tuple[int, int] | None = None

    for file_path in input_files:
        with Image.open(file_path) as img:
            frame = img.convert("RGBA")
            if base_size is None:
                base_size = frame.size
            elif frame.size != base_size:
                frame = frame.resize(base_size, Image.Resampling.LANCZOS)
            frames.append(frame)

    first_frame, *rest_frames = frames
    first_frame.save(
        output_file,
        format="GIF",
        save_all=True,
        append_images=rest_frames,
        duration=duration_ms,
        loop=loop,
        optimize=True,
        disposal=2,
    )
    print(f"GIF created: {output_file} ({len(frames)} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an animated GIF from photos.")
    parser.add_argument(
        "input_files",
        nargs="+",
        type=Path,
        help="Input image files in the order they should appear",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default=None,
        help="Output GIF path (default: first image name + -animated.gif)",
    )
    parser.add_argument(
        "--duration-ms",
        type=int,
        default=200,
        help="Frame duration in milliseconds (default: 200)",
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=0,
        help="Loop count (0 = infinite, default: 0)",
    )
    args = parser.parse_args()

    missing = [p for p in args.input_files if not p.is_file()]
    if missing:
        print(f"Error: missing input files: {', '.join(str(p) for p in missing)}")
        sys.exit(1)

    if args.duration_ms <= 0:
        print("Error: --duration-ms must be a positive integer.")
        sys.exit(1)

    photos_to_gif(args.input_files, args.output_file, args.duration_ms, args.loop)


if __name__ == "__main__":
    main()
