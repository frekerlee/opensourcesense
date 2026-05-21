"""文章详情页 — 深度分析 + 雷达图 + 趋势线"""

import streamlit as st
from components.metrics import (
    render_score_gauge,
    render_radar_chart,
    render_trend_line,
    render_metric_bar,
)
from utils.data_loader import load_articles
from utils.scoring import get_trend_icon


def main():
    articles = load_articles()

    # 文章选择器
    st.markdown(
        '<p style="color:#D4AF37; font-weight:600; margin-bottom:4px;">📋 选择文章查看详情</p>',
        unsafe_allow_html=True,
    )

    article_options = {
        f"[{a['fashion_score']:.0f}] {a['title_cn'][:40]} — {a['source']}": a["id"]
        for a in articles
    }
    selected_label = st.selectbox(
        "选择文章",
        options=list(article_options.keys()),
        label_visibility="collapsed",
    )
    article_id = article_options[selected_label]
    article = next(a for a in articles if a["id"] == article_id)

    # === 头部：大图 + 标题 + 基本信息 ===
    col_img, col_info = st.columns([2, 3])

    with col_img:
        st.image(
            article["image_url"],
            use_container_width=True,
        )
        # 原文链接
        st.link_button(
            "🔗 阅读原文",
            article["url"],
            use_container_width=True,
        )

    with col_info:
        st.markdown(f'<h2 style="color:#E8E6E3; margin-bottom:4px;">{article["title_en"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#9B9B9B; font-size:15px; margin-bottom:12px;">{article["title_cn"]}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<span style="color:#D4AF37; font-weight:500;">{article["source"]}</span>'
            f'<span style="color:#6B6B6B;"> · {article["author"]} · {article["published_date"]}</span>',
            unsafe_allow_html=True,
        )

        # Trending badge
        if article["is_trending"]:
            st.markdown(
                '<span style="background:rgba(255,71,87,0.15); color:#FF4757; padding:2px 10px; border-radius:10px; font-size:11px;">🔥 TRENDING</span>'
                + f' <span style="color:#9B9B9B; font-size:11px;">{get_trend_icon(article["trend_direction"])}</span>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # === 评分仪表盘 + 雷达图 ===
    col_gauge, col_radar = st.columns([2, 3])

    with col_gauge:
        st.markdown('<p style="color:#9B9B9B; text-align:center; font-size:11px;">综合评分</p>', unsafe_allow_html=True)
        render_score_gauge(article["fashion_score"])

        # 详细指标条
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin-top:8px;">指标明细</p>', unsafe_allow_html=True)
        render_metric_bar("📊 社媒热度", article["social_heat"])
        render_metric_bar("💬 行业影响力", article["industry_impact"])
        render_metric_bar("🎨 内容质量", article["content_quality"])
        render_metric_bar("📈 趋势速度", max(0, article["trend_velocity"]))
        render_metric_bar("💎 独家性", article["exclusivity"])

    with col_radar:
        st.markdown('<p style="color:#9B9B9B; font-size:11px;">能力雷达图</p>', unsafe_allow_html=True)
        render_radar_chart(article)

    st.markdown("---")

    # === 摘要 ===
    st.markdown("### 📖 内容摘要")
    st.markdown(
        f'<div style="background:#1A1D23; padding:20px; border-radius:8px; color:#E8E6E3; line-height:1.9; font-size:14px;">'
        f'{article["summary_cn"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # === 结构拆解 ===
    structure = article.get("structure", "")
    if structure:
        st.markdown("### 🔬 结构拆解")
        st.markdown(
            f"""
            <div style="background:#1A1D23; border-left:4px solid #FF4757; padding:16px 20px;
                        border-radius:0 10px 10px 0; margin-bottom:16px;">
                <span style="color:#9B9B9B; font-size:13px; line-height:2.0;">{structure}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # === 朗读按钮 ===
    from components.article_card import render_tts_button
    tts_full = f"{article['title_cn']}。{article['summary_cn']}。结构拆解：{structure}"
    col_tts, _ = st.columns([1, 3])
    with col_tts:
        render_tts_button(tts_full, article.get("id", "detail"))
    st.markdown("---")

    # === 分类与标签 ===
    col_cat, col_brands, col_tags = st.columns(3)
    with col_cat:
        st.metric("内容类型", article["category"])
    with col_brands:
        st.metric("关联品牌", ", ".join(article["brands"]) if article["brands"] else "—")
    with col_tags:
        st.metric("标签", ", ".join(article["tags"]) if article["tags"] else "—")

    st.markdown("---")

    # === 趋势线 ===
    st.markdown("### 📈 评分趋势（近7天）")
    if article.get("score_history"):
        render_trend_line(article["score_history"])
    else:
        st.caption("暂无历史数据")

    # === 相似文章推荐 ===
    st.markdown("### 🔗 你可能也感兴趣")
    similar = [
        a for a in articles
        if a["id"] != article["id"]
        and (
            any(b in a["brands"] for b in article["brands"])
            or a["category"] == article["category"]
        )
    ][:4]

    if similar:
        cols = st.columns(4)
        for i, sim in enumerate(similar):
            with cols[i]:
                st.image(sim["image_url"], use_container_width=True)
                st.markdown(
                    f'<p style="color:#E8E6E3; font-size:11px; font-weight:500;">{sim["title_cn"][:25]}...</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<span style="color:#FF4757; font-size:10px; font-weight:600;">SCORE {sim["fashion_score"]}</span>'
                    f'<span style="color:#6B6B6B; font-size:10px;"> · {sim["source"]}</span>',
                    unsafe_allow_html=True,
                )
    else:
        st.caption("暂无相似文章")


if __name__ == "__main__":
    main()
