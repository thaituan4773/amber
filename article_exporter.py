import re
from markdownify import markdownify
from config import ARTICLES_DIR

# slugify a string to create a valid filename
def slugify(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s-]", "", title)   # remove special chars
    title = re.sub(r"[\s_-]+", "-", title)    # replace space/underscore with -
    title = re.sub(r"^-+|-+$", "", title)     # trim leading/trailing -
    return title

# save articles to markdown files
def save_articles_to_files(articles: list):
    for article in articles:
        slug = slugify(article['title'])
        file_path = ARTICLES_DIR / f"{slug}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {article['title']}\n\n")
            f.write(f"**URL:** {article['html_url']}\n\n")
            f.write(f"**Last Updated:** {article['updated_at']}\n\n")
            f.write(markdownify(article['body']))
