import re
from pathlib import Path

APP_TITLE = "YouTube Downloader"
DEFAULT_OUTPUT_DIR = str(Path.home() / "Downloads" / "YouTube")
QUALITY_CHOICES = ["best", "1080p", "720p", "480p", "360p"]


def sanitize_filename(name: str) -> str:
    """Return a filesystem-safe filename while preserving a useful title."""
    cleaned = re.sub(r"[^A-Za-z0-9\s._-]", "", name or "youtube_video")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "youtube_video"


def ensure_directory(path: str) -> str:
    directory = Path(path).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory)
