import requests

class ZendeskScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_articles(self) -> list[dict]:
        url = f"{self.base_url}/api/v2/help_center/articles.json"
        articles = []
        while url:
            print(f"Fetching articles from: {url}")
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            
            for article in data["articles"]:
                articles.append({
                    "id": article["id"],
                    "html_url": article["html_url"],
                    "updated_at": article["updated_at"],
                    "title": article["title"],
                    "body": article["body"],
                })
            
            url = data["next_page"]
        return articles
    
    # Since incremental article endpoint requires authentication, we will fetch all articles and filter them based on the updated_at timestamp.
    def get_articles_since(self, last_sync: str) -> list[dict]:
        url = f"{self.base_url}/api/v2/help_center/en-us/articles.json?sort_by=updated_at&sort_order=desc"

        articles = []

        while url:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for article in data["articles"]:
                #Stop early if the article's updated_at is older than last_sync
                if article["updated_at"] <= last_sync:
                    return articles
                
                articles.append({
                    "id": article["id"],
                    "html_url": article["html_url"],
                    "updated_at": article["updated_at"],
                    "title": article["title"],
                    "body": article["body"],
                })

            url = data.get("next_page")
                
        return articles