"""文章卡片组件 — 含结构拆解 + 朗读功能"""

import streamlit as st
import html
from utils.scoring import get_score_color, get_trend_icon, get_trend_class


def render_tts_button(text: str, btn_id: str):
    """渲染一个朗读按钮，使用 HTML5 SpeechSynthesis API"""
    safe_text = html.escape(text).replace("'", "\\'").replace("\n", " ")
    tts_html = f"""
    <button onclick="
        if(window.speechSynthesis.speaking){{window.speechSynthesis.cancel();this.textContent='🔊 朗读';return;}}
        var u=new SpeechSynthesisUtterance(document.getElementById('tts_{btn_id}').textContent);
        u.lang='zh-CN';u.rate=0.9;u.pitch=1.1;
        u.onend=function(){{document.getElementById('btn_{btn_id}').textContent='🔊 朗读';}};
        this.textContent='⏸ 停止';window.speechSynthesis.speak(u);
    " id="btn_{btn_id}" style="
        background:#2A2D33;color:#D4AF37;border:1px solid #3A3D43;border-radius:6px;
        padding:4px 12px;font-size:11px;cursor:pointer;margin-top:6px;
    ">🔊 朗读</button>
    <span id="tts_{btn_id}" style="display:none;">{safe_text}</span>
    """
    st.markdown(tts_html, unsafe_allow_html=True)


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

    card_id = article.get("id", "0")

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

        # 展开：摘要 + 结构拆解 + 原文链接 + 朗读
        with st.expander(f"📖 {article['title_cn'][:40]}...", expanded=False):
            # 内容摘要
            st.markdown(
                f"""
                <div style="color:#E8E6E3; font-size:13px; line-height:1.8; margin-bottom:12px;">
                <span style="color:#D4AF37; font-weight:600;">📝 内容摘要</span><br>
                {article['summary_cn']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # AI 解读（仅视频内容显示）
            ai_insight = article.get("ai_insight", [])
            if ai_insight:
                insight_html = "".join([f'<li style="margin-bottom:6px;">{ins}</li>' for ins in ai_insight])
                st.markdown(
                    f"""
                    <div style="background:linear-gradient(135deg, #1A1020 0%, #1A1D23 100%);
                                border:1px solid #8B5CF6; border-radius:10px; padding:14px 16px; margin-bottom:12px;">
                        <span style="color:#A78BFA; font-weight:700; font-size:12px;">🤖 AI 深度解读 · BibiGPT</span>
                        <ul style="color:#C4B5FD; font-size:11px; line-height:1.7; margin:8px 0 0 0; padding-left:16px;">
                            {insight_html}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # 结构拆解
            structure = article.get("structure", "")
            if structure:
                st.markdown(
                    f"""
                    <div style="background:#1A1D23; border-left:3px solid #FF4757; padding:10px 14px;
                                border-radius:0 8px 8px 0; margin-bottom:12px;">
                        <span style="color:#FF4757; font-weight:600; font-size:11px;">🔬 结构拆解</span><br>
                        <span style="color:#9B9B9B; font-size:11px; line-height:1.7;">{structure}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # 原文 + 朗读按钮
            col_link, col_tts = st.columns([3, 1])
            with col_link:
                st.markdown(
                    f'<a href="{article["url"]}" target="_blank" '
                    f'style="color:#D4AF37; font-size:12px; text-decoration:none;">'
                    f'→ 阅读原文</a>',
                    unsafe_allow_html=True,
                )
            with col_tts:
                # 朗读内容：标题 + 摘要
                tts_text = f"{article['title_cn']}。{article['summary_cn']}"
                render_tts_button(tts_text, article.get("id", "0"))
