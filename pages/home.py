"""首页 — 文章卡片网格"""

import streamlit as st
from components.article_card import render_article_cards
from components.sidebar import render_sidebar
from utils.data_loader import load_articles, filter_articles, sort_articles


def main():
    articles = load_articles()

    # 渲染左侧边栏并获取筛选参数
    filters = render_sidebar()

    # 顶部快速筛选按钮
    st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:0 0 4px 0;">快速筛选</p>', unsafe_allow_html=True)
    quick_cols = st.columns([1, 1, 1, 1, 1, 1, 2])
    quick_filters = ["全部", "🎬 视频解读", "📰 产业新闻", "📊 趋势分析", "💬 深度评论", "👗 时装周"]

    # 用 session state 记住快捷筛选
    if "quick_filter" not in st.session_state:
        st.session_state.quick_filter = "全部"

    for i, qf in enumerate(quick_filters):
        with quick_cols[i]:
            label = qf.replace("🎬 ", "").replace("📰 ", "").replace("📊 ", "").replace("💬 ", "").replace("👗 ", "")
            if st.button(qf, key=f"qf_{i}", use_container_width=True,
                         type="primary" if st.session_state.quick_filter == label else "secondary"):
                st.session_state.quick_filter = label

    st.markdown("---")

    # 合并侧边栏筛选 + 快捷筛选
    if st.session_state.quick_filter != "全部":
        # 快捷筛选覆盖侧边栏的 category 筛选
        filtered = filter_articles(
            articles,
            categories=[st.session_state.quick_filter],
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

    # 统计信息行
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("当前文章", len(sorted_articles))
    with col2:
        avg_score = sum(a["fashion_score"] for a in sorted_articles) / max(1, len(sorted_articles))
        st.metric("平均评分", f"{avg_score:.1f}")
    with col3:
        trending_count = sum(1 for a in sorted_articles if a["is_trending"])
        st.metric("热门", trending_count)
    with col4:
        video_count = sum(1 for a in sorted_articles if a.get("category") == "视频解读")
        st.metric("视频", video_count)

    st.markdown("---")

    render_article_cards(sorted_articles)


if __name__ == "__main__":
    main()
