"""來源庫 — 对标原站「原始字幕軍火庫」，展示全部22+来源及文章"""

import streamlit as st
from collections import defaultdict
from config import SOURCES
from utils.data_loader import load_articles


def main():
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            <span style="color:#D4AF37; font-size:18px; font-weight:700;">🗂 原始素材軍火庫</span>
            <span style="color:#9B9B9B; font-size:11px;">全部监控来源 · 原文直链</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    articles = load_articles()

    # 按来源分组
    source_groups = defaultdict(list)
    for a in articles:
        source_groups[a["source"]].append(a)

    # 统计面板
    open_sources = [s for s in SOURCES if s["access"] == "open"]
    paywall_sources = [s for s in SOURCES if s["access"] == "paywall"]
    blogger_sources = [s for s in SOURCES if s["access"] == "blogger"]
    active_sources = set(a["source"] for a in articles)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("监控来源", len(SOURCES))
    with col2:
        st.metric("今日有文章", len(active_sources))
    with col3:
        st.metric("可直接访问", len(open_sources))
    with col4:
        st.metric("付费墙", len(paywall_sources))
    with col5:
        st.metric("博主平台", len(blogger_sources))

    st.markdown("---")

    # Tab 切换：活跃来源 / 全部来源 / 付费墙
    tab1, tab2, tab3 = st.tabs(["📋 有文章的来源", "📡 全部监控来源", "🔒 付费墙 / 博主平台"])

    with tab1:
        render_active_sources(source_groups, articles)

    with tab2:
        render_all_sources(SOURCES, source_groups)

    with tab3:
        render_restricted_sources(paywall_sources, blogger_sources, source_groups)


def render_active_sources(source_groups, articles):
    """展示有文章的来源（按文章数排序）"""
    sorted_sources = sorted(source_groups.items(), key=lambda x: len(x[1]), reverse=True)

    for source_name, source_articles in sorted_sources:
        avg_score = sum(a["fashion_score"] for a in source_articles) / len(source_articles)
        trending_count = sum(1 for a in source_articles if a["is_trending"])
        source_info = next((s for s in SOURCES if s["name"] == source_name), None)
        desc = source_info["desc"] if source_info else ""

        st.markdown(
            f"""
            <div style="background:#1E2127; border-radius:8px; padding:12px 16px; margin-bottom:10px;
                        display:flex; align-items:center; justify-content:space-between;">
                <div>
                    <span style="color:#D4AF37; font-weight:600; font-size:15px;">{source_name}</span>
                    <span style="color:#6B6B6B; font-size:10px; margin-left:8px;">{desc}</span>
                    <span style="color:#4A4D53; font-size:10px; margin-left:6px;">· {len(source_articles)}篇</span>
                </div>
                <div style="display:flex; gap:16px;">
                    <span style="color:#9B9B9B; font-size:11px;">均分 <b style="color:#E8E6E3;">{avg_score:.1f}</b></span>
                    <span style="color:#FF4757; font-size:11px;">🔥 {trending_count}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 文章列表
        for a in source_articles[:8]:
            score_color = "#2ED573" if a["fashion_score"] >= 85 else "#FFA502" if a["fashion_score"] >= 70 else "#FF4757"
            trend = "△" if a["trend_direction"] == "up" else "▽" if a["trend_direction"] == "down" else "―"
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:12px; padding:8px 16px;
                            border-bottom:1px solid #1A1D23; font-size:12px;">
                    <span style="color:{score_color}; font-weight:700; min-width:30px;">{a['fashion_score']:.0f}</span>
                    <span style="color:#6B6B6B; font-size:9px; min-width:12px;">{trend}</span>
                    <div style="flex:1; min-width:0;">
                        <div style="color:#E8E6E3; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{a['title_cn']}</div>
                    </div>
                    <span style="color:#6B6B6B; font-size:10px; min-width:50px; text-align:right;">{a['category']}</span>
                    <a href="{a['url']}" target="_blank" style="color:#D4AF37; font-size:10px; text-decoration:none;">原文 →</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if len(source_articles) > 8:
            with st.expander(f"全部 {len(source_articles)} 篇"):
                for a in source_articles[8:]:
                    st.markdown(f'- **{a["fashion_score"]:.0f}** [{a["title_cn"]}]({a["url"]}) · {a["category"]}')


def render_all_sources(all_sources, source_groups):
    """展示全部22+来源（含无文章的），按状态分组"""
    active = {s["name"] for s in all_sources if s["name"] in source_groups}
    inactive = [s for s in all_sources if s["name"] not in source_groups]

    # 活跃来源
    st.markdown('<p style="color:#2ED573; font-size:12px; margin:8px 0;">🟢 活跃来源</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, source in enumerate([s for s in all_sources if s["name"] in active]):
        src_articles = source_groups.get(source["name"], [])
        avg = sum(a["fashion_score"] for a in src_articles) / max(1, len(src_articles))
        access_icon = "🔓" if source["access"] == "open" else "🔒"
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="background:#1E2127; border-radius:6px; padding:10px 12px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#D4AF37; font-weight:600; font-size:13px;">{source['name']}</span>
                        <span style="font-size:10px;">{access_icon}</span>
                    </div>
                    <div style="color:#9B9B9B; font-size:10px; margin:2px 0;">{source['desc']}</div>
                    <div style="display:flex; justify-content:space-between; margin-top:4px;">
                        <span style="color:#6B6B6B; font-size:10px;">{len(src_articles)}篇</span>
                        <span style="color:#E8E6E3; font-size:10px;">均分 {avg:.1f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 无文章来源（当日无更新）
    if inactive:
        st.markdown('<p style="color:#9B9B9B; font-size:12px; margin:16px 0 8px 0;">⏸️ 今日无更新</p>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, source in enumerate(inactive):
            access_icon = "🔓" if source["access"] == "open" else "🔒"
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:#16181D; border-radius:6px; padding:10px 12px; margin-bottom:8px; opacity:0.6;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#9B9B9B; font-weight:500; font-size:13px;">{source['name']}</span>
                            <span style="font-size:10px;">{access_icon}</span>
                        </div>
                        <div style="color:#6B6B6B; font-size:10px;">{source['desc']}</div>
                        <div style="color:#4A4D53; font-size:10px; margin-top:2px;">暂无新文章</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_restricted_sources(paywall_sources, blogger_sources, source_groups):
    """付费墙和博主平台"""
    st.markdown("### 🔒 付费墙来源")
    st.caption("以下来源有付费墙限制，通过搜索获取公开摘要")

    cols = st.columns(2)
    for i, source in enumerate(paywall_sources):
        has_articles = source["name"] in source_groups
        count = len(source_groups.get(source["name"], []))
        with cols[i % 2]:
            status_color = "#2ED573" if has_articles else "#6B6B6B"
            status_text = f"{count}篇" if has_articles else "未获取"
            st.markdown(
                f"""
                <div style="background:#1E2127; border-radius:6px; padding:10px 12px; margin-bottom:6px;">
                    <span style="color:#D4AF37; font-size:13px; font-weight:500;">{source['name']}</span>
                    <span style="color:{status_color}; font-size:10px; margin-left:6px;">{status_text}</span>
                    <div style="color:#9B9B9B; font-size:10px;">{source['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### 📱 博主 / 平台内容")
    st.caption("小红书、微信公众号等平台博主内容（即将接入）")

    for source in blogger_sources:
        has_articles = source["name"] in source_groups
        st.markdown(
            f"""
            <div style="background:#1E2127; border-radius:6px; padding:10px 12px; margin-bottom:6px;">
                <span style="color:#FF6B81; font-size:13px; font-weight:500;">{source['name']}</span>
                <span style="color:#6B6B6B; font-size:10px; margin-left:6px;">
                    {'已接入' if has_articles else '即将接入'}
                </span>
                <div style="color:#9B9B9B; font-size:10px;">{source['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
