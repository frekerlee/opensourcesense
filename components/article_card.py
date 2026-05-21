"""文章卡片组件"""

import streamlit as st
from utils.scoring import get_score_color, get_trend_icon, get_trend_class


def render_article_card(article: dict):
    """渲染单篇文章卡片"""

    score = article["fashion_score"]
    score_color = get_score_color(score)
    trend_icon = get_trend_icon(article["trend_direction"])
    trend_cls = get_trend_class(article["trend_direction"])

    # 构建标签 HTML
    tags_html = ""
    for tag in article.get("tags", []):
        tags_html += f'<span class="tag">{tag}</span>'
    for brand in article.get("brands", []):
        tags_html += f'<span class="tag brand">{brand}</span>'
    if article["is_trending"]:
        tags_html += '<span class="tag trending">TRENDING</span>'

    # 评分条宽度百分比
    score_pct = min(100, max(0, score))

    card_html = f"""
    <div class="article-card">
        <div style="display:flex; gap:14px;">
            <div style="flex-shrink:0; width:140px; height:95px; border-radius:8px; overflow:hidden;">
                <img src="{article['image_url']}" style="width:100%; height:100%; object-fit:cover;"
                     onerror="this.style.opacity='0.3'" />
            </div>
            <div style="flex:1; min-width:0;">
                <div class="card-title-en">{article['title_en']}</div>
                <div class="card-title-cn">{article['title_cn']}</div>
                <div class="card-meta">
                    <span class="source">{article['source']}</span> · {article['published_date']}
                    &nbsp;<span class="{trend_cls}">{trend_icon}</span>
                </div>
                <div class="score-bar-container">
                    <span class="score-label">SCORE</span>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{score_pct}%;"></div>
                    </div>
                    <span class="score-value" style="color:{score_color};">{score}</span>
                </div>
                <div class="sub-metrics">
                    <span class="sub-metric">📊 <span class="val">{article['social_heat']}</span></span>
                    <span class="sub-metric">💬 <span class="val">{article['industry_impact']}</span></span>
                    <span class="sub-metric">🎨 <span class="val">{article['content_quality']}</span></span>
                    <span class="sub-metric">📈 <span class="val">{article['trend_velocity']}</span></span>
                    <span class="sub-metric">💎 <span class="val">{article['exclusivity']}</span></span>
                </div>
                <div class="tags">{tags_html}</div>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


def render_article_cards(articles: list[dict], max_items: int = None):
    """批量渲染文章卡片列表"""
    items = articles[:max_items] if max_items else articles
    if not items:
        st.markdown(
            '<div style="text-align:center; padding:60px 20px; color:#6B6B6B;">'
            '<p style="font-size:48px; margin:0;">🔍</p>'
            '<p>没有匹配的文章，请调整筛选条件</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return
    for article in items:
        render_article_card(article)
        # 使用 expander 展示摘要
        with st.expander(f"📖 {article['title_cn'][:40]}...", expanded=False):
            st.markdown(
                f"""
                <div style="color:#E8E6E3; font-size:13px; line-height:1.8;">
                {article['summary_cn']}
                </div>
                <div style="margin-top:12px;">
                <a href="{article['url']}" target="_blank" style="color:#D4AF37; font-size:12px; text-decoration:none;">
                → 阅读原文
                </a>
                </div>
                """,
                unsafe_allow_html=True,
            )
