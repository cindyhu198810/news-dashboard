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

        # 清洗摘要
        summary = clean_html(entry.get("summary", ""))[:120]

        # 处理日期（转 YYYY-MM-DD）
        date_raw = entry.get("published", "")
        try:
            date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        except:
            date = ""

        news.append({
            "title": entry.get("title", ""),
            "source": source,   # ✅ 正确来源
            "date": date,       # ✅ 中文格式日期
            "summary": summary if summary else "暂无摘要",
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
