"""左侧边栏筛选器"""

import streamlit as st
from config import CATEGORIES, BRANDS, SOURCES, SITE_NAME, SITE_SUBTITLE


def render_sidebar() -> dict:
    """渲染左侧边栏，返回筛选参数字典"""

    with st.sidebar:
        # Logo / Site Name
        st.markdown(
            f"""
            <div style="padding: 12px 0 8px 0;">
                <span style="color:#D4AF37; font-size:20px; font-weight:700; letter-spacing:1px;">{SITE_NAME}</span>
                <br>
                <span style="color:#9B9B9B; font-size:11px;">{SITE_SUBTITLE}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # 搜索
        search = st.text_input(
            "🔍 搜索",
            placeholder="文章、品牌、关键词...",
            label_visibility="collapsed",
        )

        # 内容类型
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 内容类型</p>', unsafe_allow_html=True)
        categories = []
        for cat in CATEGORIES:
            if st.checkbox(cat, value=True, key=f"cat_{cat}"):
                categories.append(cat)

        st.markdown("---")

        # 品牌
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 品牌</p>', unsafe_allow_html=True)
        brand_search = st.text_input(
            "搜索品牌",
            placeholder="输入品牌名...",
            key="brand_search",
            label_visibility="collapsed",
        )
        filtered_brands = [b for b in BRANDS if brand_search.lower() in b.lower()] if brand_search else BRANDS[:8]
        brands = st.multiselect(
            "选择品牌",
            options=BRANDS,
            default=[],
            label_visibility="collapsed",
            placeholder="全部品牌",
        )
        # 展示当前筛选的品牌标签
        if brands:
            tags_html = " ".join(
                [f'<span class="tag brand">{b}</span>' for b in brands]
            )
            st.markdown(f'<div class="tags" style="margin-bottom:8px;">{tags_html}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # 来源
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 来源</p>', unsafe_allow_html=True)
        sources = st.multiselect(
            "选择来源",
            options=SOURCES,
            default=[],
            label_visibility="collapsed",
            placeholder="全部来源",
        )

        st.markdown("---")

        # 时间
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 时间范围</p>', unsafe_allow_html=True)
        date_range = st.selectbox(
            "时间范围",
            options=["全部", "今天", "本周", "本月"],
            index=2,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # 排序
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 排序方式</p>', unsafe_allow_html=True)
        sort_by = st.selectbox(
            "排序",
            options=["综合评分", "社媒热度", "行业影响力", "趋势速度", "内容质量", "最新发布"],
            index=0,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # 仅看热门
        trending_only = st.toggle("🔥 仅看热门文章", value=False)

        st.markdown("<br>", unsafe_allow_html=True)

        # 底部署名
        st.markdown(
            '<p style="color:#4A4D53; font-size:9px; text-align:center;">OPEN SOURCESENSE v1.0<br>Powered by Streamlit</p>',
            unsafe_allow_html=True,
        )

    return {
        "search": search,
        "categories": categories,
        "brands": brands,
        "sources": sources,
        "date_range": date_range,
        "sort_by": sort_by,
        "trending_only": trending_only,
    }
