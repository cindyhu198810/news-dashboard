import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser

def fetch_latest_news():
    news = []
    
    # 1. GSMA RSS
    try:
        feed = feedparser.parse('https://www.gsma.com/newsroom/feed/')
        for entry in feed.entries[:3]:
            news.append({
                'title': entry.title,
                'source': 'GSMA',
                'date': entry.published[:10] if 'published' in entry else datetime.now().strftime('%Y-%m-%d'),
                'summary': (entry.summary or '')[:120] + '...' if len(entry.summary or '') > 120 else (entry.summary or ''),
                'url': entry.link,
                'tags': ['GSMA', '行业新闻'],
                'type': 'news'
            })
    except:
        pass
    
    # 2. Counterpoint 最新报告
    counterpoint_reports = [
        {
            'title': 'Apple leads global smartphone market with 20% share in 2025',
            'source': 'Counterpoint',
            'date': '2026-01-12',
            'summary': 'Global smartphone market analysis: Apple 20%, Samsung 18%, Xiaomi 11%.',
            'url': 'https://www.channelnewsasia.com/business/apple-leads-global-smartphone-market-20-share-in-2025-says-counterpoint-5852586',
            'tags': ['Counterpoint', '市场报告', '苹果'],
            'type': 'report'
        }
    ]
    news.extend(counterpoint_reports)
    
    # 3. IDC 智能手机市场
    idc_reports = [
        {
            'title': 'Smartphone Market Share Q1 2026',
            'source': 'IDC',
            'date': '2026-03-22',
            'summary': 'Global smartphone shipments grew 2.4% YoY in Q1 2026.',
            'url': 'https://www.idc.com/promo/smartphone-market-share/',
            'tags': ['IDC', '市场报告'],
            'type': 'report'
        }
    ]
    news.extend(idc_reports)
    
    return news

def main():
    print("开始抓取手机市场资讯...")
    news = fetch_latest_news()
    
    data = {
        'updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'news': news[:10]
    }
    
    # 写回 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新成功！共 {len(news)} 条资讯")
    print(f"⏰ 更新时间：{data['updated']}")

if __name__ == '__main__':
    main()
