import feedparser
import json
from datetime import datetime

feeds = {
    "GSMArena": "https://www.gsmarena.com/rss-news-reviews.php3",
    "Android Authority": "https://www.androidauthority.com/feed/",
    "PhoneArena": "https://www.phonearena.com/rss/news"
}

news = []

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:
        news.append({
            "title": entry.get("title", ""),
            "source": source,
            "date": entry.get("published", "")[:10],
            "summary": entry.get("summary", "")[:100],
            "url": entry.get("link", ""),
            "tags": ["手机"],
            "type": "news"
        })

data = {
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
    "news": news[:30]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
