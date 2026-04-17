import feedparser
import json
import re
import requests
from datetime import datetime

feeds = {
    "GSMArena": "https://www.gsmarena.com/rss-news-reviews.php3",
    "Android Authority": "https://www.androidauthority.com/feed/",
    "PhoneArena": "https://www.phonearena.com/rss/news"
}

news = []

# -------------------------
# 清洗HTML
# -------------------------
def clean_html(text):
    return re.sub('<.*?>', '', text)

# -------------------------
# 翻译（免费API）
# -------------------------
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
        res = requests.get(url, params=params, timeout=5)
        return res.json()[0][0][0]
    except:
        return text  # 失败就返回原文

# -------------------------
# 分类
# -------------------------
def classify(title):
    t = title.lower()
    if "iphone" in t or "apple" in t:
        return "苹果"
    elif "samsung" in t or "galaxy" in t:
        return "三星"
    elif "xiaomi" in t or "redmi" in t:
        return "小米"
    else:
        return "安卓"

# -------------------------
# SEO标题
# -------------------------
def seo_title(title_cn):
    return title_cn

# -------------------------
# 主逻辑
# -------------------------
for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:

        title_en = entry.get("title", "")
        summary_raw = entry.get("summary", "")

        # 清洗摘要
        summary_clean = clean_html(summary_raw)

        # 翻译
        title_cn = translate(title_en)
        summary_cn = translate(summary_clean)
        summary_cn = summary_cn[:180] if len(summary_cn) > 180 else summary_cn

        # 分类
        category = classify(title_en)

        # 日期
        date = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            except:
                date = ""

        img_match = re.search(r'<img.*?src="(.*?)"', summary_raw)
        image = img_match.group(1) if img_match else ""

        # ✅ 强制兜底（关键）
        if not image or image.strip() == "":
            image = "https://via.placeholder.com/120x80?text=Phone"

        news.append({
            "title": seo_title(title_cn),
            "source": source,
            "date": date,
            "summary": summary_cn,
            "url": entry.get("link", ""),
            "tags": [category],
            "image": image,
            "type": "news"
        })

data = {
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
    "news": news[:30]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
