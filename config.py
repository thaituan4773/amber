from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} is not set.")
    return value

BASE_URL = get_env("BASE_URL")
BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"

ARTICLES_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
VECTOR_STORE_ID = get_env("VECTOR_STORE_ID")