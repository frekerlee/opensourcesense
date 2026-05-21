"""趋势分析页 — 品牌热度、内容分布、趋势时间线"""

import streamlit as st
from components.charts import (
    render_brand_bar_chart,
    render_category_pie,
    render_source_bar,
    render_trend_timeline,
)
from utils.data_loader import (
    load_articles,
    get_top_brands,
    get_category_distribution,
    get_source_contribution,
)


def main():
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <span style="color:#D4AF37; font-size:18px; font-weight:700;">📊 趋势分析</span>
            <span style="color:#9B9B9B; font-size:11px;">时尚内容全景洞察</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    articles = load_articles()

    # === 第一行：KPI 卡片 ===
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("文章总数", len(articles))
    with col2:
        st.metric("平均评分", f"{sum(a['fashion_score'] for a in articles) / len(articles):.1f}")
    with col3:
        st.metric("热门率", f"{sum(1 for a in articles if a['is_trending']) / len(articles) * 100:.0f}%")
    with col4:
        st.metric("品牌覆盖", len(set(b for a in articles for b in a["brands"])))
    with col5:
        st.metric("来源覆盖", len(set(a["source"] for a in articles)))

    st.markdown("---")

    # === 第二行：图表区 ===
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown('<p style="color:#E8E6E3; font-weight:600; margin-bottom:8px;">🔥 本周热门品牌 TOP10</p>', unsafe_allow_html=True)
        brand_df = get_top_brands(articles)
        render_brand_bar_chart(brand_df)

    with col_chart2:
        st.markdown('<p style="color:#E8E6E3; font-weight:600; margin-bottom:8px;">📂 内容类型分布</p>', unsafe_allow_html=True)
        cat_df = get_category_distribution(articles)
        render_category_pie(cat_df)

    st.markdown("---")

    # === 第三行：趋势时间线 ===
    st.markdown('<p style="color:#E8E6E3; font-weight:600; margin-bottom:8px;">📈 热度趋势 & 发文频率</p>', unsafe_allow_html=True)
    render_trend_timeline(articles)

    st.markdown("---")

    # === 第四行：来源贡献 ===
    col_src1, col_src2 = st.columns([3, 2])

    with col_src1:
        st.markdown('<p style="color:#E8E6E3; font-weight:600; margin-bottom:8px;">📰 来源贡献度 TOP10</p>', unsafe_allow_html=True)
        source_df = get_source_contribution(articles)
        render_source_bar(source_df)

    with col_src2:
        st.markdown('<p style="color:#E8E6E3; font-weight:600; margin-bottom:8px;">🏆 评分最高的文章</p>', unsafe_allow_html=True)
        top5 = sorted(articles, key=lambda x: x["fashion_score"], reverse=True)[:5]
        for i, a in enumerate(top5):
            score_color = "#FF4757" if a["fashion_score"] < 70 else "#FFA502" if a["fashion_score"] < 85 else "#2ED573"
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px; padding:6px 8px; background:#1E2127; border-radius:8px;">
                    <span style="color:#6B6B6B; font-size:12px;">#{i+1}</span>
                    <div style="flex:1; min-width:0;">
                        <div style="color:#E8E6E3; font-size:11px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{a['title_cn']}</div>
                        <div style="color:#6B6B6B; font-size:9px;">{a['source']} · {a['published_date']}</div>
                    </div>
                    <span style="color:{score_color}; font-weight:700; font-size:14px;">{a['fashion_score']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
