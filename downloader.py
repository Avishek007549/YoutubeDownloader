import os
from pathlib import Path

from pytube import YouTube

from config import DEFAULT_OUTPUT_DIR
from utils import ensure_directory, sanitize_filename


def download_video(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, quality: str = "720p", audio_only: bool = False):
    """Download a YouTube video or audio stream."""
    ensure_directory(output_dir)

    yt = YouTube(url)
    title = sanitize_filename(yt.title)

    if audio_only:
        stream = yt.streams.filter(only_audio=True).order_by("abr").last()
        if stream is None:
            raise ValueError("No audio stream is available for this video.")
        filename = f"{title}.mp3"
        output_path = stream.download(output_path=output_dir, filename=filename)
        return output_path

    stream = None
    if quality and quality != "best":
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=quality).first()

    if stream is None:
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()

    if stream is None:
        stream = yt.streams.get_highest_resolution()

    if stream is None:
        raise ValueError("No downloadable stream is available for this URL.")

    output_path = stream.download(output_path=output_dir, filename=f"{title}.mp4")
    return output_path


def download_from_input(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, quality: str = "720p", audio_only: bool = False):
    """Wrapper used by the Tkinter app."""
    if not url or not url.startswith("http"):
        raise ValueError("Please enter a valid YouTube URL.")

    return download_video(url, output_dir=output_dir, quality=quality, audio_only=audio_only)
