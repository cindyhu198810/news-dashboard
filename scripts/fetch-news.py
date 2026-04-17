import feedparser
import json
import re
import requests
from datetime import datetime

def translate(text):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "zh-CN",
            "dt": "t",
            "q": text
        }
        res = requests.get(url, params=params)
        return res.json()[0][0][0]
    except:
        return text

feeds = {
    "GSMArena": "https://www.gsmarena.com/rss-news-reviews.php3",
    "Android Authority": "https://www.androidauthority.com/feed/",
    "PhoneArena": "https://www.phonearena.com/rss/news"
}

news = []

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:

        raw_summary = entry.get("summary", "")
        clean_summary = re.sub('<.*?>', '', raw_summary)

        date_str = entry.get("published", "")
        try:
            dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
            date = dt.strftime("%Y-%m-%d")
        except:
            date = ""

        news.append({
            "title": translate(entry.get("title", "")),
            "source": source,
            "date": date,
            "summary": clean_summary[:120],
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
