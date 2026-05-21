"""來源庫 — 对标原站「原始字幕軍火庫」，展示所有来源及其文章"""

import streamlit as st
from collections import defaultdict
from utils.data_loader import load_articles


def main():
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <span style="color:#D4AF37; font-size:18px; font-weight:700;">🗂 原始素材軍火庫</span>
            <span style="color:#9B9B9B; font-size:11px;">按来源浏览所有文章 · 原文直链</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    articles = load_articles()

    # 按来源分组
    source_groups = defaultdict(list)
    for a in articles:
        source_groups[a["source"]].append(a)

    # 来源选择
    all_sources = sorted(source_groups.keys())
    col_select, col_count = st.columns([3, 1])
    with col_select:
        selected_source = st.selectbox(
            "选择来源",
            options=["全部来源"] + all_sources,
            label_visibility="collapsed",
        )
    with col_count:
        if selected_source == "全部来源":
            total = len(articles)
        else:
            total = len(source_groups[selected_source])
        st.metric("文章数", total)

    # 确定要展示的来源
    sources_to_show = all_sources if selected_source == "全部来源" else [selected_source]

    for source in sources_to_show:
        source_articles = sorted(
            source_groups[source],
            key=lambda x: x["fashion_score"],
            reverse=True,
        )

        avg_score = sum(a["fashion_score"] for a in source_articles) / len(source_articles)
        trending_count = sum(1 for a in source_articles if a["is_trending"])

        # 来源头部
        st.markdown(
            f"""
            <div style="background:#1E2127; border-radius:8px; padding:12px 16px; margin-bottom:10px;
                        display:flex; align-items:center; justify-content:space-between;">
                <div>
                    <span style="color:#D4AF37; font-weight:600; font-size:15px;">{source}</span>
                    <span style="color:#6B6B6B; font-size:11px; margin-left:8px;">{len(source_articles)} 篇文章</span>
                </div>
                <div style="display:flex; gap:16px;">
                    <span style="color:#9B9B9B; font-size:11px;">均分 <b style="color:#E8E6E3;">{avg_score:.1f}</b></span>
                    <span style="color:#FF4757; font-size:11px;">🔥 {trending_count} 热门</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 文章列表（紧凑模式）
        for a in source_articles[:10]:
            score_color = "#2ED573" if a["fashion_score"] >= 85 else "#FFA502" if a["fashion_score"] >= 70 else "#FF4757"
            trend = "△" if a["trend_direction"] == "up" else "▽" if a["trend_direction"] == "down" else "―"

            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:12px; padding:8px 16px;
                            border-bottom:1px solid #1A1D23; font-size:12px;">
                    <span style="color:{score_color}; font-weight:700; min-width:32px;">{a['fashion_score']}</span>
                    <span style="color:{'#2ED573' if a['trend_direction']=='up' else '#FF4757' if a['trend_direction']=='down' else '#9B9B9B'}; font-size:10px; min-width:14px;">{trend}</span>
                    <div style="flex:1; min-width:0;">
                        <div style="color:#E8E6E3; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{a['title_cn']}</div>
                        <div style="color:#6B6B6B; font-size:10px;">{a['title_en'][:60]}...</div>
                    </div>
                    <span style="color:#6B6B6B; font-size:10px; min-width:80px; text-align:right;">{a['published_date']}</span>
                    <span style="color:#9B9B9B; font-size:10px; min-width:60px; text-align:right;">{a['category']}</span>
                    <a href="{a['url']}" target="_blank" style="color:#D4AF37; font-size:10px; text-decoration:none;">原文 →</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 如果文章多，折叠显示
        if len(source_articles) > 10:
            with st.expander(f"查看 {source} 全部 {len(source_articles)} 篇文章"):
                for a in source_articles[10:]:
                    score_color = "#2ED573" if a["fashion_score"] >= 85 else "#FFA502" if a["fashion_score"] >= 70 else "#FF4757"
                    st.markdown(
                        f'- **{a["fashion_score"]}** [{a["title_cn"]}]({a["url"]}) — *{a["published_date"]}* · {a["category"]}',
                    )

        if selected_source == "全部来源":
            st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
