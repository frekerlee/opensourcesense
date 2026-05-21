"""首页 — 文章卡片网格"""

import streamlit as st
from components.article_card import render_article_cards
from components.sidebar import render_sidebar
from utils.data_loader import load_articles, filter_articles, sort_articles


def main():
    # 加载数据
    articles = load_articles()

    # 渲染左侧边栏并获取筛选参数
    filters = render_sidebar()

    # 应用筛选
    filtered = filter_articles(
        articles,
        categories=filters["categories"],
        brands=filters["brands"],
        sources=filters["sources"],
        date_range=filters["date_range"],
        search=filters["search"],
        trending_only=filters["trending_only"],
    )

    # 排序
    sorted_articles = sort_articles(filtered, filters["sort_by"])

    # 统计信息行
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总文章", len(sorted_articles))
    with col2:
        avg_score = sum(a["fashion_score"] for a in sorted_articles) / max(1, len(sorted_articles))
        st.metric("平均评分", f"{avg_score:.1f}")
    with col3:
        trending_count = sum(1 for a in sorted_articles if a["is_trending"])
        st.metric("热门文章", trending_count)
    with col4:
        today_count = sum(1 for a in sorted_articles if a["published_date"] == sorted_articles[0]["published_date"]) if sorted_articles else 0
        st.metric("今日新增", today_count)

    st.markdown("---")

    # 渲染文章卡片
    render_article_cards(sorted_articles)


if __name__ == "__main__":
    main()
