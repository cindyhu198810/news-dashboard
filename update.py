import json
from datetime import datetime

# 模拟真实抓取（等API稳定后再替换）
news = [
    {
        "title": "GSMA发布2026年移动行业展望报告",
        "source": "GSMA",
        "date": "2026-04-08",
        "summary": "5G-A网络部署加速，AI手机渗透率预计达35%",
        "url": "https://www.gsma.com/newsroom/",
        "tags": ["GSMA", "5G", "AI"],
        "type": "report"
    },
    {
        "title": "Counterpoint：Q1全球智能手机出货量增长3%",
        "source": "Counterpoint",
        "date": "2026-04-07",
        "summary": "苹果市占率稳定20%，华为海外增长迅猛",
        "url": "https://counterpointresearch.com/",
        "tags": ["Counterpoint", "市场报告", "苹果"],
        "type": "report"
    }
]

data = {
    "updated": datetime.now().strftime('%Y-%m-%d %H:%M'),
    "news": news
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 数据更新成功！")
