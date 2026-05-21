"""首页 — 文章卡片网格"""

import streamlit as st
from components.article_card import render_article_cards
from utils.data_loader import load_articles, filter_articles, sort_articles, get_meta


def render_home():
    articles = load_articles()

    # 简洁的 KPI 行
    total = len(articles)
    xhs = sum(1 for a in articles if a["source"] == "小红书关注")
    videos = sum(1 for a in articles if a["category"] == "视频解读")
    media = sum(1 for a in articles if a["source"] in
                ["WWD", "Business of Fashion", "FashionNetwork", "Ladymax", "Miss Tweed", "NYT / Vanessa Friedman"])
    trending = sum(1 for a in articles if a["is_trending"])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 总内容", f"{total} 篇")
    with col2:
        st.metric("📕 小红书", f"{xhs} 篇")
    with col3:
        st.metric("🎬 B站视频", f"{videos} 篇")
    with col4:
        st.metric("📰 媒体", f"{media} 篇")
    with col5:
        st.metric("🔥 热门", f"{trending} 篇")

    # 元数据
    meta = get_meta()
    if meta.get("last_update"):
        st.caption(f"📅 上次更新：{meta['last_update']}  |  📄 {meta.get('brief_file', '')}  |  🔗 share.streamlit.io/frekerlee/opensourcesense")

    st.markdown("---")

    # 搜索 + 排序（轻量）
    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 搜索", placeholder="品牌、关键词...", label_visibility="collapsed")
    with col_sort:
        sort_by = st.selectbox("排序", ["综合评分", "最新发布", "社媒热度"], label_visibility="collapsed")

    filtered = articles
    if search:
        filtered = filter_articles(articles, search=search)
    sorted_articles = sort_articles(filtered, sort_by)

    render_article_cards(sorted_articles)


# Keep for standalone page support
def main():
    render_home()


if __name__ == "__main__":
    main()
