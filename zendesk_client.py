import requests

class ZendeskScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_articles(self):
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
                    "url": article["url"],
                    "html_url": article["html_url"],
                    "updated_at": article["updated_at"],
                    "title": article["title"],
                    "body": article["body"],
                })
            
            url = data["next_page"]
        return articles
        