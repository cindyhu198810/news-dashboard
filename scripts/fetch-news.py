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
        result = res.json()[0]
        # ✅ 拼接完整句子（关键优化）
        return "".join([item[0] for item in result])
    except:
        return text

# -------------------------
# 分类
# -------------------------
def classify(title):
# -------------------------
# AI摘要优化（核心升级）
# -------------------------
def ai_summary(text):
    text = text.strip().replace("\n", "").replace("  ", " ")

    # 去掉奇怪符号
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、:： ]', '', text)

    # 常见优化
    text = text.replace("该 设备", "该设备")
    text = text.replace("这个 设备", "该设备")

    # 控制长度（适合网页展示）
    if len(text) > 110:
        text = text[:110] + "..."

    # AI风格增强
    if "发布" in text:
        text += "，带来多项升级"
    elif "曝光" in text:
        text += "，更多细节逐步揭晓"
    elif "更新" in text:
        text += "，用户体验进一步优化"

    return text
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
# -------------------------
# 标题优化（关键词）
# -------------------------
def optimize_title(title):
    replace_map = {
        "Google": "谷歌",
        "Samsung": "三星",
        "Apple": "苹果",
        "Xiaomi": "小米",
        "Redmi": "红米",
        "launch": "发布",
        "launches": "发布",
        "reveals": "曝光",
        "leak": "泄露",
        "hands-on": "上手",
        "review": "评测",
        "vs": "对比"
    }

    for k, v in replace_map.items():
        title = title.replace(k, v)

    return title.strip()
def seo_title(title_cn):
    title_cn = optimize_title(title_cn)

    # AI风格增强
    if "发布" in title_cn:
        title_cn += "，新机正式登场"
    elif "曝光" in title_cn or "泄露" in title_cn:
        title_cn += "，核心配置曝光"
    elif "评测" in title_cn:
        title_cn += "，真实体验如何？"

    # 防止过长
    if len(title_cn) > 38:
        title_cn = title_cn[:38] + "..."

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

        # 太短就用标题补充
        if len(summary_clean) < 30:
            summary_clean = title_en

        # 翻译
        title_cn = translate(title_en)
        summary_cn = translate(summary_clean)
        summary_cn = ai_summary(summary_cn)

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
