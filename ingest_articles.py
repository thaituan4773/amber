from openai import OpenAI
from config import OPENAI_API_KEY, ARTICLES_DIR, VECTOR_STORE_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def upload_articles_to_openai() -> list[str]:
    files = list(ARTICLES_DIR.glob("*.md"))

    if not files:
        raise ValueError(f"No markdown files found in {ARTICLES_DIR}")
    
    files_id: list[str] = []

    for file in files:
        with open(file, "rb") as f:
            upload = client.files.create(
                file=f,
                purpose="assistants"
            )
        files_id.append(upload.id)

    print(f"Uploaded {len(files_id)} files to OpenAI. File IDs: {files_id}")
    return files_id

def attach_to_vector_store(files_ids: list[str]):
    if not VECTOR_STORE_ID:
        raise ValueError("VECTOR_STORE_ID is not set")
    
    client.vector_stores.file_batches.create(
        vector_store_id=VECTOR_STORE_ID,
        file_ids=files_ids
    )

    print(f"Attached files to Vector Store {VECTOR_STORE_ID}")