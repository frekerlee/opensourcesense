"""数据加载与处理"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


DATA_FILE = Path(__file__).parent.parent / "data" / "articles.json"
META_FILE = Path(__file__).parent.parent / "data" / ".meta.json"
BRIEF_DIR = Path(os.path.expanduser("~/Desktop/时尚日报"))


def get_latest_brief() -> Path | None:
    """扫描日报目录，返回最新的 .md 文件路径"""
    if not BRIEF_DIR.exists():
        return None
    md_files = sorted(BRIEF_DIR.glob("*.md"), reverse=True)
    return md_files[0] if md_files else None


def get_meta() -> dict:
    """读取元数据（上次更新时间等）"""
    if META_FILE.exists():
        with open(META_FILE, "r") as f:
            return json.load(f)
    return {"last_update": None, "total_articles": 0, "brief_file": None}


def save_meta(meta: dict):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def refresh_from_brief() -> tuple[int, str]:
    """从最新日报刷新数据，返回 (文章数, 日报文件名)"""
    latest = get_latest_brief()
    if not latest:
        return 0, ""

    from data.parse_daily_brief import parse_brief
    articles = parse_brief(latest)

    # Fix source names
    import re
    for a in articles:
        a["source"] = re.sub(r'\s*（[^）]+）', '', a["source"]).strip()

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    meta = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_articles": len(articles),
        "brief_file": latest.name,
    }
    save_meta(meta)

    # Clear Streamlit cache
    load_articles.clear()
    return len(articles), latest.name


@st.cache_data(ttl=300)
def load_articles(path: str = None) -> list[dict]:
    """加载文章数据（带缓存，5分钟过期）。优先从 JSON 加载，否则尝试最新日报，最后回退 mock"""
    if path is None:
        path = DATA_FILE
    if not Path(path).exists():
        latest = get_latest_brief()
        if latest:
            refresh_from_brief()
        else:
            from data.mock_data import save_articles
            save_articles(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def to_dataframe(articles: list[dict]) -> pd.DataFrame:
    """将文章列表转为 DataFrame，方便筛选操作"""
    return pd.DataFrame(articles)


def filter_articles(
    articles: list[dict],
    categories: list[str] = None,
    brands: list[str] = None,
    sources: list[str] = None,
    date_range: str = "全部",
    search: str = "",
    trending_only: bool = False,
) -> list[dict]:
    """根据筛选条件过滤文章"""
    result = articles

    if categories:
        result = [a for a in result if a["category"] in categories]

    if brands:
        result = [
            a for a in result
            if any(b in a["brands"] for b in brands)
        ]

    if sources:
        result = [a for a in result if a["source"] in sources]

    if date_range == "今天":
        today = datetime.now().strftime("%Y-%m-%d")
        result = [a for a in result if a["published_date"] == today]
    elif date_range == "本周":
        cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        result = [a for a in result if a["published_date"] >= cutoff]
    elif date_range == "本月":
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        result = [a for a in result if a["published_date"] >= cutoff]

    if search:
        keyword = search.lower()
        result = [
            a for a in result
            if keyword in a["title_en"].lower()
            or keyword in a["title_cn"]
            or keyword in a["summary_cn"]
            or any(keyword in b.lower() for b in a["brands"])
        ]

    if trending_only:
        result = [a for a in result if a["is_trending"]]

    return result


def sort_articles(articles: list[dict], sort_by: str = "综合评分") -> list[dict]:
    """排序文章列表"""
    key_map = {
        "综合评分": "fashion_score",
        "社媒热度": "social_heat",
        "行业影响力": "industry_impact",
        "趋势速度": "trend_velocity",
        "最新发布": "published_date",
        "内容质量": "content_quality",
    }
    key = key_map.get(sort_by, "fashion_score")
    return sorted(articles, key=lambda x: x.get(key, 0), reverse=True)


def get_top_brands(articles: list[dict], top_n: int = 10) -> pd.DataFrame:
    """统计品牌出现频次"""
    from collections import Counter
    counter = Counter()
    for a in articles:
        for b in a.get("brands", []):
            counter[b] += 1
    return pd.DataFrame(
        counter.most_common(top_n), columns=["brand", "count"]
    )


def get_category_distribution(articles: list[dict]) -> pd.DataFrame:
    """统计内容类型分布"""
    from collections import Counter
    counter = Counter(a["category"] for a in articles)
    return pd.DataFrame(
        counter.items(), columns=["category", "count"]
    ).sort_values("count", ascending=False)


def get_source_contribution(articles: list[dict]) -> pd.DataFrame:
    """统计来源贡献"""
    from collections import Counter
    counter = Counter(a["source"] for a in articles)
    df = pd.DataFrame(counter.items(), columns=["source", "count"])
    return df.sort_values("count", ascending=False)
