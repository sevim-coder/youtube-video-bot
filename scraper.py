import feedparser
import re

def clean_text(text):
    # Gereksiz boşlukları ve HTML etiketlerini temizler
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_rss_entries(rss_url, limit=5):
    feed = feedparser.parse(rss_url)
    entries = []
    for entry in feed.entries[:limit]:
        title = clean_text(entry.get('title', ''))
        summary = clean_text(entry.get('summary', ''))
        link = entry.get('link', '')
        entries.append({
            'title': title,
            'summary': summary,
            'link': link
        })
    return entries

if __name__ == "__main__":
    rss_url = "https://www.sciencedaily.com/rss/top.xml"
    articles = fetch_rss_entries(rss_url)

    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}\n{article['summary']}\n{article['link']}")
