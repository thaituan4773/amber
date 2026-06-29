from pathlib import Path

from openai import OpenAI
from config import OPENAI_API_KEY, VECTOR_STORE_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def upload_files(files: dict[str, Path]) -> dict[str, str]:
    uploaded: dict[str, str] = {}

    total = len(files)

    for i, (article_id, path) in enumerate(files.items(), start=1):
        print(f"[{i}/{total}] Uploading {path.name}")

        with open(path, "rb") as f:
            upload = client.files.create(
                file=f,
                purpose="assistants"
            )

        uploaded[article_id] = upload.id

    return uploaded

def attach_to_vector_store(files_ids: list[str]):
    client.vector_stores.file_batches.create(
        vector_store_id=VECTOR_STORE_ID,
        file_ids=files_ids
    )

def delete_files(files_ids: list[str]):
    for file_id in files_ids:
        client.files.delete(file_id=file_id)
