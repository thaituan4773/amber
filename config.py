from pathlib import Path
import os

BASE_URL = "https://support.optisigns.com"
BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"

ARTICLES_DIR.mkdir(exist_ok=True)