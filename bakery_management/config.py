import os
from pathlib import Path

APP_NAME = "Bakery Management System"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = str(DATA_DIR / "bakery.db")


def ensure_data_dir() -> str:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return str(DATA_DIR)
