from urllib.parse import urlparse

from pytube import YouTube

from config import DEFAULT_OUTPUT_DIR, ensure_directory, sanitize_filename


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}


def is_youtube_url(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in {"http", "https"} and parsed.netloc.lower().split(":")[0] in YOUTUBE_HOSTS
    except ValueError:
        return False


def download_video(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, quality: str = "720p", audio_only: bool = False):
    """Download one video or its best available audio stream from YouTube."""
    ensure_directory(output_dir)
    yt = YouTube(url)
    title = sanitize_filename(yt.title)

    if audio_only:
        stream = yt.streams.filter(only_audio=True).order_by("abr").last()
        if stream is None:
            raise ValueError("No audio stream is available for this YouTube video.")
        return stream.download(output_path=output_dir, filename=f"{title}.mp3")

    stream = None
    if quality and quality != "best":
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=quality).first()
    if stream is None:
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()
    if stream is None:
        stream = yt.streams.get_highest_resolution()
    if stream is None:
        raise ValueError("No downloadable stream is available for this YouTube video.")
    return stream.download(output_path=output_dir, filename=f"{title}.mp4")


def download_from_input(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, quality: str = "720p", audio_only: bool = False):
    if not is_youtube_url(url):
        raise ValueError("Please enter a valid YouTube URL.")
    return download_video(url, output_dir=output_dir, quality=quality, audio_only=audio_only)
