import sys
import argparse
from pathlib import Path
from moviepy import VideoFileClip
import mimetypes


def extract_audio_from_video(
    input_file: Path, audio_format: str = "mp3", output_file: Path = None
) -> None:
    audio_extensions = [
        "mp3",
        "wav",
        "aac",
        "ogg",
        "flac",
        "m4a",
        "wma",
        "alac",
        "aiff",
        "opus",
    ]
    if audio_format not in audio_extensions:
        raise ValueError(f"Unsupported audio format '{audio_format}'.")

    if output_file is None:
        output_file = input_file.with_name(
            f"{input_file.stem}-extracted.{audio_format}"
        )
    else:
        if output_file.suffix.strip(".").lower() not in audio_extensions:
            output_file = output_file.with_suffix(f".{audio_format}")

    try:
        video = VideoFileClip(str(input_file))
        audio = video.audio
        if audio is None:
            raise ValueError(f"No audio stream found in '{input_file}'.")
        audio.write_audiofile(str(output_file))
        print(
            f"Audio has been successfully extracted from '{input_file}' and saved as '{output_file}'"
        )
    except Exception as e:
        print(f"Error during audio extraction: {e}")
        raise


def is_video(file_path: Path) -> bool:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith("video")


def main():
    parser = argparse.ArgumentParser(description="Extract audio from a video file.")
    parser.add_argument("input_file", type=Path, help="Input video file path")
    parser.add_argument(
        "-o", "--output_file", type=Path, default=None, help="Output audio file name"
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="mp3",
        help="Output audio format (e.g., mp3, wav, aac)",
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    audio_format = args.format.lower()

    if not input_file.is_file():
        print(f"Error: '{input_file}' does not exist.")
        sys.exit(1)

    if not is_video(input_file):
        print(f"Error: '{input_file}' is not a valid video file.")
        sys.exit(1)

    extract_audio_from_video(input_file, audio_format, output_file)


if __name__ == "__main__":
    main()
