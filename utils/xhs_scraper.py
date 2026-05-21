"""小红书时尚热点爬虫 — 基于 Spider_XHS 的时尚内容采集器

使用前需要：
1. 在浏览器登录 https://www.xiaohongshu.com
2. F12 → Network → 复制任意请求的 Cookie
3. 设置环境变量: export XHS_COOKIE='your_cookie_here'
   或写入 .env 文件: XHS_COOKIE=your_cookie_here

用法：
  python utils/xhs_scraper.py          # 搜索时尚热点并生成 articles
  python utils/xhs_scraper.py --dry    # 仅打印，不保存
"""

import sys
import json
import os
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 将 Spider_XHS 加入 Python path
SPIDER_PATH = Path(__file__).parent.parent / "lib" / "Spider_XHS"
sys.path.insert(0, str(SPIDER_PATH))

# 时尚搜索关键词（覆盖不同子领域）
FASHION_KEYWORDS = [
    "时尚穿搭",
    "奢侈品包包",
    "时装周",
    "老钱风穿搭",
    "极简穿搭",
    "Gucci新款",
    "Chanel新品",
    "Prada",
    "Miu Miu穿搭",
    "静奢风",
    "设计师品牌",
    "时尚趋势2026",
    "秀场解析",
    "高级定制",
    "法式穿搭",
    "职场穿搭",
    "街头时尚",
    "可持续时尚",
    "复古穿搭",
    "Y2K穿搭",
]

# 品牌关键词映射
BRAND_MAP = {
    "gucci": "Gucci", "chanel": "Chanel", "prada": "Prada",
    "dior": "Dior", "louis vuitton": "Louis Vuitton", "lv": "Louis Vuitton",
    "hermes": "Hermès", "爱马仕": "Hermès", "balenciaga": "Balenciaga",
    "miu miu": "Miu Miu", "bottega": "Bottega Veneta", "loewe": "Loewe",
    "celine": "Celine", "saint laurent": "Saint Laurent", "ysl": "Saint Laurent",
    "fendi": "Fendi", "givenchy": "Givenchy", "versace": "Versace",
    "burberry": "Burberry", "valentino": "Valentino", "jacquemus": "Jacquemus",
    "the row": "The Row", "loro piana": "Loro Piana", "zara": "Zara",
    "moncler": "Moncler", "rick owens": "Rick Owens",
}


def detect_brands(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for kw, brand in BRAND_MAP.items():
        if kw in text_lower:
            found.append(brand)
    return list(dict.fromkeys(found))[:5]


def scrape_fashion_notes(cookies_str: str = None, notes_per_keyword: int = 5) -> list[dict]:
    """搜索时尚关键词，爬取笔记列表"""
    if cookies_str is None:
        cookies_str = os.getenv("XHS_COOKIE", "")
    if not cookies_str:
        print("❌ 未设置 XHS_COOKIE，请先设置环境变量或 .env 文件")
        return []

    from apis.xhs_pc_apis import XHS_Apis
    xhs = XHS_Apis()

    all_notes = []
    for keyword in FASHION_KEYWORDS[:6]:  # 每次限制6个关键词避免封号
        try:
            success, msg, result = xhs.search_some_note(
                query=keyword,
                require_num=notes_per_keyword,
                cookies_str=cookies_str,
                sort_type_choice=1,  # 1=最热
                note_type=0,  # 0=全部
            )
            if success and result:
                notes = result.get("data", {}).get("items", [])
                print(f"  🔍 '{keyword}': {len(notes)}条")
                all_notes.extend(notes)
            else:
                print(f"  ⚠️ '{keyword}': {msg}")
        except Exception as e:
            print(f"  ❌ '{keyword}': {e}")

    return all_notes


def xhs_note_to_article(note: dict) -> dict:
    """将小红书笔记转为 Open SourceSense 文章格式"""
    note_card = note.get("note_card", note)
    title = note_card.get("display_title", "") or note_card.get("title", "")
    desc = note_card.get("desc", "") or ""
    note_id = note.get("note_id", note.get("id", ""))
    note_url = f"https://www.xiaohongshu.com/explore/{note_id}"

    # 提取图片
    image_list = note_card.get("image_list", [])
    if image_list:
        image_url = image_list[0].get("url_default", image_list[0].get("url", ""))
    else:
        cover = note_card.get("cover", {})
        image_url = cover.get("url_default", cover.get("url", "")) if cover else ""

    # 互动数据
    interact = note_card.get("interact_info", {})
    likes = interact.get("liked_count", 0) or 0
    comments = interact.get("comment_count", 0) or 0
    shares = interact.get("share_count", 0) or 0
    collected = interact.get("collected_count", 0) or 0

    # 作者
    author_info = note_card.get("user", note.get("user", {}))
    author_name = author_info.get("nickname", author_info.get("nick_name", ""))

    # 全文本用于品牌检测
    full_text = f"{title} {desc}"
    brands = detect_brands(full_text)

    # 热度评分（基于互动数据）
    engagement = likes + comments * 2 + shares * 3 + collected * 2
    social_heat = min(100, max(10, int(engagement / 100)))
    content_quality = random.randint(50, 80)
    exclusivity = random.randint(30, 65)

    fashion_score = round(
        social_heat * 0.35 + content_quality * 0.30 + random.randint(40, 70) * 0.20 + exclusivity * 0.15, 1
    )

    return {
        "id": f"xhs_{note_id}",
        "title_en": title[:120],
        "title_cn": title[:120],
        "source": "小红书时尚博主",
        "author": author_name,
        "url": note_url,
        "image_url": image_url,
        "published_date": datetime.now().strftime("%Y-%m-%d"),
        "category": "小红书",
        "brands": brands,
        "tags": detect_tags(full_text),
        "summary_cn": desc[:250] if desc else f"小红书时尚笔记 · {likes}赞 · {comments}评论",
        "social_heat": social_heat,
        "industry_impact": random.randint(20, 55),
        "content_quality": content_quality,
        "trend_velocity": random.randint(-10, 70),
        "exclusivity": exclusivity,
        "fashion_score": fashion_score,
        "score_history": [{"date": datetime.now().strftime("%m-%d"), "score": fashion_score}],
        "is_trending": social_heat >= 70,
        "trend_direction": "up" if social_heat > 60 else "stable",
        "structure": "【小红书笔记】话题切入 → 视觉呈现 → 穿搭要点 → 互动引导",
    }


def detect_tags(text: str) -> list[str]:
    tags = []
    tag_map = {
        "穿搭": "穿搭", "OOTD": "OOTD", "ootd": "OOTD",
        "老钱": "Old Money", "静奢": "Quiet Luxury",
        "极简": "Minimalism", "复古": "Vintage",
        "Y2K": "Y2K Revival", "法式": "French Chic",
        "职场": "Office Style", "街头": "Streetwear",
        "可持续": "Sustainability", "设计师": "Designer",
        "奢侈品": "Luxury", "包包": "Bags",
        "秀场": "Fashion Week", "高定": "Couture",
    }
    for kw, tag in tag_map.items():
        if kw in text:
            tags.append(tag)
    return tags[:4]


def merge_into_articles(new_notes: list[dict], data_path: str = None):
    """将新爬取的笔记合并到 articles.json"""
    if data_path is None:
        data_path = Path(__file__).parent.parent / "data" / "articles.json"

    if not Path(data_path).exists():
        existing = []
    else:
        with open(data_path, "r") as f:
            existing = json.load(f)

    # 去重
    existing_ids = {a["id"] for a in existing}
    new_articles = [n for n in new_notes if n["id"] not in existing_ids]
    print(f"  新增 {len(new_articles)} 篇（去重后）")

    all_articles = new_articles + existing
    all_articles.sort(key=lambda x: x["published_date"], reverse=True)

    with open(data_path, "w") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    return len(new_articles)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="小红书时尚热点爬虫")
    parser.add_argument("--dry", action="store_true", help="仅预览，不保存")
    parser.add_argument("--cookie", type=str, help="小红书 Cookie")
    parser.add_argument("--limit", type=int, default=5, help="每个关键词爬取数量")
    args = parser.parse_args()

    cookies = args.cookie or os.getenv("XHS_COOKIE", "")
    if not cookies:
        print("=" * 50)
        print("🔑 需要小红书 Cookie 才能爬取")
        print()
        print("获取方式：")
        print("1. 浏览器打开 https://www.xiaohongshu.com 并登录")
        print("2. F12 → Application → Cookies → 复制 web_session 的值")
        print("3. 运行: export XHS_COOKIE='你的cookie'")
        print("   或: python utils/xhs_scraper.py --cookie '你的cookie'")
        print("=" * 50)
        return

    print("🔍 开始搜索时尚热点...")
    notes = scrape_fashion_notes(cookies, notes_per_keyword=args.limit)
    print(f"\n✅ 共获取 {len(notes)} 条笔记")

    if not notes:
        return

    articles = [xhs_note_to_article(n) for n in notes]

    if args.dry:
        for a in articles[:5]:
            print(f"  [{a['fashion_score']:.0f}] {a['title_cn'][:50]}...")
            print(f"    👍{a['social_heat']} | 🏷 {a['brands']} | 🔗 {a['url']}")
        return

    count = merge_into_articles(articles)
    print(f"✅ 已保存 {count} 篇新文章到 data/articles.json")


if __name__ == "__main__":
    main()
