import os
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9\s._-]", "", name or "youtube_video")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "youtube_video"


def ensure_directory(path: str) -> str:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory)


def format_bytes(num: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num)
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"
