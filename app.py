"""OPEN SOURCESENSE — 时尚内容开源情报平台"""

import streamlit as st
from config import CUSTOM_CSS

st.set_page_config(
    page_title="Open SourceSense — 时尚内容情报平台",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 初始化数据
from utils.data_loader import load_articles, filter_articles, sort_articles
from components.article_card import render_article_cards
load_articles()

# ===== 顶部导航 =====
st.markdown(
    """
    <div class="top-nav">
        <span class="logo">OPEN SOURCESENSE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tab 导航
tabs = st.tabs([
    "🏠 首页",
    "📕 小红书",
    "🎬 视频解读",
    "📰 时尚媒体",
    "📊 趋势分析",
    "🗂 来源库",
])

from pages.home import render_home
from pages.gallery import main as gallery_page
from pages.trends import main as trends_page
from pages.source_library import main as source_page
from pages.detail import main as detail_page

with tabs[0]:
    render_home()

with tabs[1]:
    xhs = [a for a in load_articles() if a["source"] == "小红书关注"]
    xhs = sorted(xhs, key=lambda x: x["social_heat"], reverse=True)

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### 📕 小红书时尚热点")
        st.caption("实时爬取小红书时尚穿搭、奢侈品、设计师品牌等内容")
    with col_h2:
        st.metric("笔记数", len(xhs))

    if xhs:
        from components.article_card import render_article_cards
        render_article_cards(xhs[:30])
    else:
        st.info("暂无小红书内容 · 点击侧边栏刷新")

with tabs[2]:
    # 视频解读专属视图
    videos = filter_articles(load_articles(), categories=["视频解读"])
    videos = sort_articles(videos, "综合评分")

    st.markdown("### 🎬 视频解读 · B站时尚博主")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("视频总数", len(videos))
    with col2:
        st.metric("博主", "AHALOLO + 午夜飞行鼠")

    if videos:
        from components.article_card import render_article_cards
        render_article_cards(videos)
    else:
        st.info("暂无视频内容")

with tabs[3]:
    # 时尚媒体
    media_sources = ["WWD", "Business of Fashion", "Miss Tweed", "NYT / Vanessa Friedman",
                     "FashionNetwork", "Ladymax", "Vogue Business"]
    media = [a for a in load_articles() if a["source"] in media_sources]
    media = sorted(media, key=lambda x: x["fashion_score"], reverse=True)

    st.markdown("### 📰 时尚媒体")
    cols_media = st.columns(4)
    for i, src in enumerate(["WWD", "Business of Fashion", "NYT / Vanessa Friedman", "Miss Tweed"]):
        count = sum(1 for a in media if a["source"] == src)
        with cols_media[i]:
            st.metric(src, count)

    if media:
        from components.article_card import render_article_cards
        render_article_cards(media[:30])
    else:
        st.info("暂无媒体内容")

with tabs[4]:
    trends_page()

with tabs[5]:
    source_page()
