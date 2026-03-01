"""Video / Audio Tool definitions."""
import customtkinter as ctk
from pathlib import Path

from ..widgets import FileInput, OutputFileInput, ChoiceInput, NumberInput

from video_audio_manipulation.extract_audio_from_video import extract_audio_from_video
from video_audio_manipulation.video_to_gif import video_to_gif


# ---------------------------------------------------------------------------
# Build functions
# ---------------------------------------------------------------------------

def build_extract_audio(parent, status_bar):
    file_in = FileInput(
        parent, "Input Video File",
        [("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")],
    )
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output Audio File (optional)",
        [("Audio files", "*.mp3 *.wav *.aac *.ogg *.flac *.m4a")],
    )
    file_out.pack(fill="x", pady=(0, 16))

    fmt = ChoiceInput(
        parent, "Audio Format",
        ["mp3", "wav", "aac", "ogg", "flac", "m4a"], "mp3",
    )
    fmt.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status(
                "Please select an input video file", "error"
            )
        out = file_out.get()
        audio_fmt = fmt.get()
        out_path = Path(out) if out else Path(inp).with_suffix(f".{audio_fmt}")

        def task():
            extract_audio_from_video(Path(inp), audio_fmt, out_path)
            return f"Saved to {out_path}"

        status_bar.run_task(task, "Successfully extracted audio!")

    ctk.CTkButton(
        parent, text="Extract Audio", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


def build_video_to_gif(parent, status_bar):
    file_in = FileInput(
        parent, "Input Video File",
        [("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")],
    )
    file_in.pack(fill="x", pady=(0, 16))

    file_out = OutputFileInput(
        parent, "Output GIF File (optional)",
        [("GIF files", "*.gif")], ".gif",
    )
    file_out.pack(fill="x", pady=(0, 16))

    start = NumberInput(parent, "Start Time (seconds, optional)", "", 0)
    start.pack(fill="x", pady=(0, 8))

    end = NumberInput(parent, "End Time (seconds, optional)", "", 0)
    end.pack(fill="x", pady=(0, 8))

    fps = NumberInput(parent, "FPS (1-30)", "15", 1, 30)
    fps.pack(fill="x", pady=(0, 8))

    width = NumberInput(parent, "Width in pixels (optional)", "", 1)
    width.pack(fill="x", pady=(0, 24))

    def execute():
        inp = file_in.get()
        if not inp:
            return status_bar.set_status(
                "Please select an input video file", "error"
            )
        out = file_out.get()
        s = start.get()
        e = end.get()
        f = int(fps.get() or 15)
        w = int(width.get()) if width.get() else None
        out_path = Path(out) if out else Path(inp).with_suffix(".gif")

        def task():
            video_to_gif(Path(inp), out_path, s, e, f, w)
            return f"Saved to {out_path}"

        status_bar.run_task(task, "Successfully converted video to GIF!")

    ctk.CTkButton(
        parent, text="Convert to GIF", height=40, font=("", 14, "bold"),
        command=execute,
    ).pack(fill="x", pady=(8, 0))


# ---------------------------------------------------------------------------
# Exported section list
# ---------------------------------------------------------------------------

VIDEO_SECTIONS = [
    (
        "VIDEO / AUDIO",
        [
            {
                "name": "Extract Audio",
                "description": "Extract the audio track from a video file in various formats",
                "build_fn": build_extract_audio,
            },
            {
                "name": "Video to GIF",
                "description": "Convert a video (or clip) to an animated GIF",
                "build_fn": build_video_to_gif,
            },
        ],
    ),
]
