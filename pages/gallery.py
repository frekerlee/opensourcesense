"""Gallery Mode — 缩略图网格浏览"""

import streamlit as st
from components.sidebar import render_sidebar
from utils.data_loader import load_articles, filter_articles, sort_articles


def main():
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <span style="color:#D4AF37; font-size:18px; font-weight:700;">📸 GALLERY MODE</span>
            <span style="color:#9B9B9B; font-size:11px;">缩略图快速浏览</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 加载数据
    articles = load_articles()

    # 筛选
    filters = render_sidebar()
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

    if not sorted_articles:
        st.markdown(
            '<div style="text-align:center; padding:60px; color:#6B6B6B;">暂无匹配文章</div>',
            unsafe_allow_html=True,
        )
        return

    # 网格列数选择
    col_count = st.select_slider(
        "每行列数",
        options=[2, 3, 4, 5],
        value=4,
        label_visibility="collapsed",
    )

    # 渲染画廊网格
    cols = st.columns(col_count)
    for i, article in enumerate(sorted_articles):
        col_idx = i % col_count
        with cols[col_idx]:
            score = article["fashion_score"]
            score_color = "#2ED573" if score >= 85 else "#FFA502" if score >= 70 else "#FF4757"

            card_html = f"""
            <div class="gallery-card" style="margin-bottom:12px;">
                <img src="{article['image_url']}" onerror="this.style.opacity='0.2'" />
                <div class="gallery-card-info">
                    <div class="title" title="{article['title_en']}">{article['title_cn'][:30]}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
                        <span style="color:#6B6B6B; font-size:10px;">{article['source']}</span>
                        <span class="score" style="color:{score_color};">{score}</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # 点击展开详情
            with st.expander(f"📖 查看", expanded=False):
                st.markdown(f"**{article['title_en']}**")
                st.markdown(f"*{article['title_cn']}*")
                st.caption(article["summary_cn"])
                st.link_button("🔗 阅读原文", article["url"])


if __name__ == "__main__":
    main()
