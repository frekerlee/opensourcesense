"""OPEN SOURCESENSE — 时尚内容开源情报平台

复刻 bk.zszhdzc.com 的核心逻辑，为时尚编辑打造的爆款内容解读看板。

四大核心模块（对标原站逻辑）：
  📝 時尚脫水報告  → 浓缩文章 + 多维评分 + 一句话解读（对标原站 "脫水報告"）
  📥 原始素材軍火庫 → 来源库 + 画廊浏览 + 原文直链（对标原站 "原始字幕軍火庫"）
  🇨🇳 雙語精翻譯讀 → EN→CN 标题摘要 + 深度拆解 + 雷达图（对标原站 "大模型中文精翻"）
  🧠 趨勢雙向進化 → 品牌热度 + 时间线 + 评分进化追踪（对标原站 "靈魂雙向進化"）
"""

import streamlit as st
from config import CUSTOM_CSS

# ============ 页面配置 ============
st.set_page_config(
    page_title="OPEN SOURCESENSE — 时尚内容开源情报平台",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ 注入自定义样式 ============
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============ 初始化数据 ============
from utils.data_loader import load_articles
load_articles()  # 首次加载确保数据文件存在

# ============ 页面路由 ============
pages = {
    "📝 時尚脫水報告": [
        st.Page("pages/home.py", title="📋 文章看板", icon="📋"),
        st.Page("pages/detail.py", title="🔍 深度解讀", icon="🔍"),
    ],
    "📥 原始素材軍火庫": [
        st.Page("pages/gallery.py", title="📸 Gallery Mode", icon="📸"),
        st.Page("pages/source_library.py", title="🗂 來源庫", icon="🗂"),
    ],
    "🧠 趨勢雙向進化": [
        st.Page("pages/trends.py", title="📊 趨勢分析", icon="📊"),
    ],
}

pg = st.navigation(pages)
pg.run()
