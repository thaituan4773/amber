from zendesk_client import ZendeskScraper
from article_exporter import save_articles_to_files
from config import BASE_URL
from ingest_articles import upload_articles_to_openai, attach_to_vector_store
from state_store import load_state, save_state, has_changed

def main():
    print("Starting daily Zendesk sync job")

    scraper = ZendeskScraper(BASE_URL)
    articles = scraper.get_all_articles()

    state = load_state()
    
    added = 0
    updated = 0
    skipped = 0

    changed_articles = []

    # 1. Check for changes in articles
    for article in articles:
        article_id = str(article["id"])

        if article_id not in state:
            added += 1
            changed_articles.append(article)
        elif has_changed(article, state):
            updated += 1
            changed_articles.append(article)
        else:
            skipped += 1

    print(f"Articles added: {added}, updated: {updated}, skipped: {skipped}")

    if not changed_articles:
        print("No new or updated articles to process.")
        return
    
    # 2. Save changed articles to markdown files
    saved_files = save_articles_to_files(changed_articles)
    print(f"Saved {len(saved_files)} articles to markdown files.")

    # 3. Upload saved files to OpenAI
    files_ids = upload_articles_to_openai(saved_files)
    print(f"Uploaded {len(files_ids)} articles to OpenAI.")

    # 4. Attach uploaded files to the vector store
    attach_to_vector_store(files_ids)
    print(f"Attached {len(files_ids)} articles to Vector Store.")

    # 5. Update state with the latest updated_at timestamps
    for article in changed_articles:
        state[str(article["id"])] = article["updated_at"]

    save_state(state)

    print("Sync completed successfully.")



if __name__ == "__main__":
    main()

