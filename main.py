from zendesk_client import ZendeskScraper
from article_exporter import save_articles_to_files
from config import BASE_URL
from openai_storage import delete_files, upload_files, attach_to_vector_store
from state_store import load_state, save_state, has_changed
from datetime import datetime

def parse_time(t: str):
    return datetime.fromisoformat(t.replace("Z", "+00:00"))

def main():
    print("Starting daily Zendesk sync job")
    
    state = load_state()
    last_sync = state.get("latest_updated_at")

    scraper = ZendeskScraper(BASE_URL)

    if(not last_sync):
        print("No previous sync found. Performing full sync.")
        articles = scraper.get_all_articles()
    else:
        print(f"Last sync was at {last_sync}. Fetching updated articles since then.")
        articles = scraper.get_articles_since(last_sync)

    added = 0
    updated = 0

    changed_articles = []

    # 1. Detect changes
    for article in articles:
        article_id = str(article["id"])

        if article_id not in state:
            added += 1
            changed_articles.append(article)

        elif has_changed(article, state):
            updated += 1
            changed_articles.append(article)

    print(f"Articles added: {added}, updated: {updated}")

    if not changed_articles:
        print("No new or updated articles to process.")
        return

    # 2. Save markdown files
    saved_files = save_articles_to_files(changed_articles)
    print(f"Saved {len(saved_files)} articles to markdown files.")

    try:
        # 3. Upload new files
        uploaded_files = upload_files(saved_files)
        print(f"Uploaded {len(uploaded_files)} articles to OpenAI.")

        # 4. Attach new files to vector store FIRST
        attach_to_vector_store(list(uploaded_files.values()))
        print("Attached files to Vector Store.")

        # 5. Delete old files (ONLY for updated articles)
        old_file_ids = []

        for article_id, file_id in uploaded_files.items():
            if article_id in state and "file_id" in state[article_id]:
                old_file_ids.append(state[article_id]["file_id"])

        if old_file_ids:
            delete_files(old_file_ids)
            print(f"Deleted {len(old_file_ids)} old files from OpenAI.")

        # 6. Update state ONLY after success
        latest_article = max(
            changed_articles,
            key=lambda a: parse_time(a["updated_at"])
        )
        state["latest_updated_at"] = latest_article["updated_at"]

        article_lookup = {
            str(a["id"]): a
            for a in changed_articles
        }

        for article_id, file_id in uploaded_files.items():
            article = article_lookup[article_id]

            state[article_id] = {
                "updated_at": article["updated_at"],
                "file_id": file_id,
            }

        save_state(state)

    except Exception as e:
        print(f"Sync failed: {e}")
        return

    print("Sync completed successfully.")


if __name__ == "__main__":
    main()