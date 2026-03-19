import sys
import argparse
from pathlib import Path
from moviepy import VideoFileClip


def video_to_gif(
    input_file: Path,
    output_file: Path = None,
    start: float = None,
    end: float = None,
    fps: int = 15,
    width: int = None,
) -> None:
    """Convert a video (or a portion of it) to an animated GIF."""
    if output_file is None:
        output_file = input_file.with_suffix(".gif")
    with VideoFileClip(str(input_file)) as source_clip:
        clip = source_clip
        if start is not None or end is not None:
            clip = clip.subclipped(start or 0, end or clip.duration)

        if width and width < clip.w:
            clip = clip.resized(width=width)

        # ffmpeg backend is usually faster and more memory-efficient.
        clip.write_gif(str(output_file), fps=fps, program="ffmpeg")
        duration = clip.duration

        if clip is not source_clip:
            clip.close()

    print(f"GIF saved: {output_file} ({duration:.1f}s, {fps} fps)")


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
