import sys
import argparse
from pathlib import Path
import shutil
import subprocess


def video_to_gif(
    input_file: Path,
    output_file: Path = None,
    start: float = None,
    end: float = None,
    fps: int = 15,
    width: int = None,
) -> None:
    """Convert a video (or a portion of it) to an animated GIF."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg is required but was not found in PATH. "
            "Install it (macOS: brew install ffmpeg, Ubuntu/Debian: sudo apt install ffmpeg)."
        )

    if output_file is None:
        output_file = input_file.with_suffix(".gif")

    vf_parts = [f"fps={fps}"]
    if width:
        vf_parts.append(f"scale={width}:-1:flags=lanczos")
    vf = ",".join(vf_parts)

    command = ["ffmpeg", "-y"]
    if start is not None:
        command.extend(["-ss", str(start)])
    command.extend(["-i", str(input_file)])
    if end is not None:
        duration = end - (start or 0)
        if duration <= 0:
            raise ValueError("--end must be greater than --start.")
        command.extend(["-t", str(duration)])
    command.extend(["-vf", vf, str(output_file)])

    subprocess.run(command, check=True, capture_output=True, text=True)
    print(f"GIF saved: {output_file} ({fps} fps)")


def main():
    parser = argparse.ArgumentParser(description="Convert a video to an animated GIF.")
    parser.add_argument("input_file", type=Path, help="Input video file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output GIF file path"
    )
    parser.add_argument(
        "--start", type=float, default=None, help="Start time in seconds"
    )
    parser.add_argument(
        "--end", type=float, default=None, help="End time in seconds"
    )
    parser.add_argument(
        "--fps", type=int, default=15, help="Frames per second (default: 15)"
    )
    parser.add_argument(
        "--width", type=int, default=None,
        help="Resize to this width in pixels (preserves aspect ratio)",
    )
    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"Error: '{args.input_file}' does not exist.")
        sys.exit(1)

    video_to_gif(
        args.input_file, args.output,
        args.start, args.end, args.fps, args.width,
    )


if __name__ == "__main__":
    main()
