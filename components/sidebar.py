"""左侧边栏筛选器"""

import streamlit as st
import os
from config import CATEGORIES, BRANDS, SOURCES, SOURCE_NAMES, SITE_NAME, SITE_SUBTITLE
from utils.data_loader import get_meta, refresh_from_brief


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
            options=SOURCE_NAMES,
            default=[],
            label_visibility="collapsed",
            placeholder=f"全部 {len(SOURCE_NAMES)} 个来源",
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

        # ===== 数据刷新 =====
        st.markdown('<p style="color:#9B9B9B; font-size:10px; margin:12px 0 4px 0; text-transform:uppercase;">▼ 数据刷新</p>', unsafe_allow_html=True)

        col_refresh, col_status = st.columns([1, 1.5])
        with col_refresh:
            if st.button("🔄 更新日报", use_container_width=True, help="从最新日报文件刷新数据"):
                with st.spinner("更新中..."):
                    count, fname = refresh_from_brief()
                if count > 0:
                    st.success(f"+{count}篇")
                else:
                    st.warning("无日报")

        with col_status:
            meta = get_meta()
            if meta.get("last_update"):
                st.markdown(
                    f'<p style="color:#4A4D53; font-size:9px; margin:0;">📅 {meta["last_update"]}<br>📄 {meta.get("brief_file", "")}</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<p style="color:#4A4D53; font-size:9px;">点击刷新加载</p>', unsafe_allow_html=True)

        # ===== 小红书一键刷新 =====
        st.markdown("---")
        st.markdown('<p style="color:#FF6B81; font-size:10px; margin:0 0 4px 0; text-transform:uppercase;">📕 小红书热点爬虫</p>', unsafe_allow_html=True)

        # Cookie 输入（存 session_state，本次会话有效）
        if "xhs_cookie" not in st.session_state:
            st.session_state.xhs_cookie = os.getenv("XHS_COOKIE", "")

        with st.expander("⚙️ 设置 Cookie", expanded=not bool(st.session_state.xhs_cookie)):
            st.caption("1. 打开 xiaohongshu.com 并登录")
            st.caption("2. F12 → Application → Cookies → web_session")
            st.session_state.xhs_cookie = st.text_input(
                "粘贴 Cookie",
                value=st.session_state.xhs_cookie,
                type="password",
                placeholder="web_session=...",
                label_visibility="collapsed",
            )

        if st.button("📕 一键爬取小红书时尚热点", use_container_width=True,
                     type="primary" if st.session_state.xhs_cookie else "secondary"):
            if not st.session_state.xhs_cookie:
                st.error("请先展开上方 ⚙️ 设置 Cookie 并粘贴")
            else:
                with st.spinner("🔍 正在搜索时尚热点..."):
                    try:
                        from utils.xhs_scraper import scrape_fashion_notes, xhs_note_to_article, merge_into_articles
                        notes = scrape_fashion_notes(st.session_state.xhs_cookie, notes_per_keyword=3)
                        if notes:
                            articles = [xhs_note_to_article(n) for n in notes]
                            count = merge_into_articles(articles)
                            st.success(f"✅ 新增 {count} 篇小红书内容")
                            st.rerun()
                        else:
                            st.warning("未获取到新笔记（Cookie可能已过期）")
                    except Exception as e:
                        st.error(f"失败: {str(e)[:80]}")

        # 底部署名
        st.markdown(
            '<p style="color:#4A4D53; font-size:9px; text-align:center; margin-top:12px;">OPEN SOURCESENSE v1.0<br>Powered by Streamlit</p>',
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
