from pathlib import Path
from markdownify import markdownify
from config import ARTICLES_DIR

def save_articles_to_files(articles: list[dict]) -> dict[str, Path]:
    saved_files: dict[str, Path] = {}

    for article in articles:
        article_id = str(article["id"])
        file_path = ARTICLES_DIR / f"{article_id}.md"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {article['title']}\n\n")
            f.write(f"**URL:** {article['html_url']}\n\n")
            f.write(f"**Last Updated:** {article['updated_at']}\n\n")
            f.write(markdownify(article["body"]))

        saved_files[article_id] = file_path

    return saved_files