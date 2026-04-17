import feedparser
import json
import re
from datetime import datetime

feeds = {
    "GSMArena": "https://www.gsmarena.com/rss-news-reviews.php3",
    "Android Authority": "https://www.androidauthority.com/feed/",
    "PhoneArena": "https://www.phonearena.com/rss/news"
}

news = []

def clean_html(text):
    return re.sub('<.*?>', '', text)

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:

        # ✅ 安全处理标题
        title = entry.get("title", "无标题")

        # ✅ 安全处理摘要
        summary_raw = entry.get("summary", "")
        summary = clean_html(summary_raw)[:120] if summary_raw else "暂无摘要"

        # ✅ 安全处理日期（不会报错）
        date = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            except:
                date = ""

        news.append({
            "title": title,
            "source": source,
            "date": date,
            "summary": summary,
            "url": entry.get("link", ""),
            "tags": ["手机","科技"],
            "type": "news"
        })

data = {
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
    "news": news[:30]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
