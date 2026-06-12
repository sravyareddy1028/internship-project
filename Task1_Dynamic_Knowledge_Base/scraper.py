import feedparser
import json

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"

def fetch_articles():
    feed = feedparser.parse(RSS_URL)

    articles = []

    for entry in feed.entries[:20]:
        articles.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        })

    return articles


def save_articles():
    articles = fetch_articles()

    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)

    print(f"Saved {len(articles)} articles")


if __name__ == "__main__":
    save_articles()