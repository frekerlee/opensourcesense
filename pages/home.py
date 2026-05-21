"""首页 — 文章卡片网格"""

import streamlit as st
from components.article_card import render_article_cards
from components.sidebar import render_sidebar
from utils.data_loader import load_articles, filter_articles, sort_articles


def main():
    articles = load_articles()

    # 左侧边栏
    filters = render_sidebar()

    # ===== 来源平台快捷筛选 =====
    st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:0 0 6px 0;">📌 按来源平台筛选</p>', unsafe_allow_html=True)

    platform_filters = [
        ("📕 小红书", "source", "小红书时尚博主"),
        ("🎬 B站视频", "category", "视频解读"),
        ("📰 WWD", "source", "WWD"),
        ("🇨🇳 Ladymax", "source", "Ladymax"),
        ("🌐 FashionNetwork", "source", "FashionNetwork"),
        ("💬 深度评论", "category", "深度评论"),
    ]

    if "quick_source" not in st.session_state:
        st.session_state.quick_source = None

    cols = st.columns(len(platform_filters) + 1)
    with cols[0]:
        if st.button("🔄 全部", use_container_width=True,
                     type="primary" if st.session_state.quick_source is None else "secondary"):
            st.session_state.quick_source = None

    for i, (label, filter_type, filter_value) in enumerate(platform_filters):
        with cols[i + 1]:
            if st.button(label, use_container_width=True,
                         type="primary" if st.session_state.quick_source == filter_value else "secondary"):
                st.session_state.quick_source = filter_value

    st.markdown("---")

    # ===== 过滤逻辑 =====
    if st.session_state.quick_source:
        qs = st.session_state.quick_source
        if qs in ("小红书时尚博主", "WWD", "Ladymax", "FashionNetwork"):
            # 来源筛选
            filtered = filter_articles(
                articles,
                categories=filters["categories"],
                brands=filters["brands"],
                sources=[qs],
                date_range=filters["date_range"],
                search=filters["search"],
                trending_only=filters["trending_only"],
            )
        else:
            # 分类筛选（视频解读 / 深度评论）
            filtered = filter_articles(
                articles,
                categories=[qs],
                brands=filters["brands"],
                sources=filters["sources"],
                date_range=filters["date_range"],
                search=filters["search"],
                trending_only=filters["trending_only"],
            )
    else:
        filtered = filter_articles(
            articles,
            categories=filters["categories"],
            brands=filters["brands"],
            sources=filters["sources"],
            date_range=filters["date_range"],
            search=filters["search"],
            trending_only=filters["trending_only"],
        )

    sorted_articles = sort_articles(filtered, filters["sort_by"])

    # ===== 统计 =====
    xhs_count = sum(1 for a in sorted_articles if a["source"] == "小红书时尚博主")
    video_count = sum(1 for a in sorted_articles if a["category"] == "视频解读")
    wwd_count = sum(1 for a in sorted_articles if a["source"] == "WWD")
    other_count = len(sorted_articles) - xhs_count - video_count - wwd_count

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("总文章", len(sorted_articles))
    with col2:
        st.metric("📕 小红书", xhs_count)
    with col3:
        st.metric("🎬 B站视频", video_count)
    with col4:
        st.metric("📰 WWD", wwd_count)
    with col5:
        st.metric("其他来源", other_count)

    st.markdown("---")

    render_article_cards(sorted_articles)


if __name__ == "__main__":
    main()
