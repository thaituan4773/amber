from pathlib import Path

from openai import OpenAI
from config import OPENAI_API_KEY, ARTICLES_DIR, VECTOR_STORE_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def upload_articles_to_openai(files: list[Path]) -> list[str]:
    if not files:
        raise ValueError("No files provided for upload")
    
    files_id: list[str] = []

    for file in files:
        with open(file, "rb") as f:
            upload = client.files.create(
                file=f,
                purpose="assistants"
            )
        files_id.append(upload.id)

    return files_id

def attach_to_vector_store(files_ids: list[str]):
    if not VECTOR_STORE_ID:
        raise ValueError("VECTOR_STORE_ID is not set")
    
    client.vector_stores.file_batches.create(
        vector_store_id=VECTOR_STORE_ID,
        file_ids=files_ids
    )
