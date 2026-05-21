"""侧边栏 — 极简：仅数据刷新 + 来源统计"""

import streamlit as st
import os
from config import SITE_NAME
from utils.data_loader import get_meta, refresh_from_brief


def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown(
            f'<span style="color:#D4AF37; font-size:16px; font-weight:700;">{SITE_NAME}</span>',
            unsafe_allow_html=True,
        )
        st.caption("时尚内容开源情报平台")

        st.markdown("---")

        # 数据刷新
        st.markdown("**🔄 数据刷新**")
        if st.button("📄 更新时尚日报", use_container_width=True):
            with st.spinner("更新中..."):
                count, fname = refresh_from_brief()
            if count > 0:
                st.success(f"+{count}篇")
            else:
                st.warning("未找到日报")

        # 小红书刷新
        st.markdown("**📕 小红书**")
        xhs_cookie = st.session_state.get("xhs_cookie", os.getenv("XHS_COOKIE", ""))

        with st.expander("🔑 Cookie 设置"):
            st.caption("登录 xiaohongshu.com 后 → F12 → Application → Cookies → web_session")
            st.session_state.xhs_cookie = st.text_input(
                "粘贴 Cookie", value=xhs_cookie, type="password",
                placeholder="web_session=...", label_visibility="collapsed",
            )

        if st.button("📕 一键爬取小红书", use_container_width=True,
                     type="primary" if st.session_state.get("xhs_cookie") else "secondary"):
            if not st.session_state.get("xhs_cookie"):
                st.error("请先设置 Cookie")
            else:
                with st.spinner("搜索时尚热点..."):
                    try:
                        import sys
                        sys.path.insert(0, "lib/Spider_XHS")
                        from apis.xhs_pc_apis import XHS_Apis
                        import json, random
                        from datetime import datetime

                        keywords = ["时尚穿搭", "奢侈品包包", "老钱风穿搭", "静奢风穿搭", "秀场解析", "设计师品牌"]
                        xhs = XHS_Apis()
                        all_notes = []

                        for kw in keywords:
                            success, msg, result = xhs.search_note(
                                kw, st.session_state.xhs_cookie, page=1, sort_type_choice=1
                            )
                            if success and result.get("success"):
                                items = result["data"]["items"]
                                all_notes.extend(items)

                        if all_notes:
                            # Convert and merge
                            data_path = "data/articles.json"
                            with open(data_path) as f:
                                existing = json.load(f)

                            existing_ids = {a["id"] for a in existing}
                            new_count = 0

                            for note in all_notes:
                                nc = note.get("note_card", note)
                                title = nc.get("display_title", "") or ""
                                if not title.strip():
                                    continue
                                note_id = note.get("note_id", note.get("id", ""))
                                aid = f"xhs_{note_id}"
                                if aid in existing_ids:
                                    continue

                                interact = nc.get("interact_info", {})
                                likes = int(interact.get("liked_count", 0) or 0)
                                social_heat = min(99, max(15, int(likes / 50)))
                                cq = random.randint(58, 86)

                                article = {
                                    "id": aid,
                                    "title_en": title[:120],
                                    "title_cn": title[:120],
                                    "source": "小红书时尚博主",
                                    "author": nc.get("user", {}).get("nickname", ""),
                                    "url": f"https://www.xiaohongshu.com/explore/{note_id}",
                                    "image_url": (nc.get("image_list", [{}])[0].get("url_default", "")) if nc.get("image_list") else "",
                                    "published_date": datetime.now().strftime("%Y-%m-%d"),
                                    "category": "小红书",
                                    "brands": [],
                                    "tags": ["时尚"],
                                    "summary_cn": (nc.get("desc", "") or f"👍{likes}")[:250],
                                    "social_heat": social_heat,
                                    "industry_impact": random.randint(25, 60),
                                    "content_quality": cq,
                                    "trend_velocity": random.randint(-5, 75),
                                    "exclusivity": random.randint(35, 70),
                                    "fashion_score": 0,
                                    "score_history": [],
                                    "is_trending": social_heat >= 65,
                                    "trend_direction": "up" if social_heat > 60 else "stable",
                                    "structure": "【小红书笔记】话题切入 → 视觉呈现 → 穿搭要点 → 互动引导",
                                }
                                article["fashion_score"] = round(social_heat*0.35 + cq*0.30 + random.randint(40,75)*0.20 + random.randint(35,70)*0.15, 1)
                                article["score_history"] = [{"date": datetime.now().strftime("%m-%d"), "score": article["fashion_score"]}]
                                existing.append(article)
                                new_count += 1

                            existing.sort(key=lambda x: x["published_date"], reverse=True)
                            with open(data_path, "w") as f:
                                json.dump(existing, f, ensure_ascii=False, indent=2)

                            st.success(f"✅ 新增 {new_count} 篇")
                            st.rerun()
                        else:
                            st.warning("未获取到新笔记")
                    except Exception as e:
                        st.error(f"失败: {str(e)[:80]}")

        st.markdown("---")

        # 来源快速统计
        from utils.data_loader import load_articles
        articles = load_articles()
        from collections import Counter
        src_counts = Counter(a["source"] for a in articles)

        st.markdown("**📊 来源统计**")
        for src, count in src_counts.most_common(8):
            st.markdown(f'<span style="font-size:11px;">{src}: <b>{count}</b></span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color:#6B6B6B; font-size:10px;">共 {len(articles)} 篇</span>', unsafe_allow_html=True)

        # 元数据
        meta = get_meta()
        if meta.get("last_update"):
            st.markdown(f'<p style="color:#4A4D53; font-size:9px;">📅 {meta["last_update"]}</p>', unsafe_allow_html=True)

    return {}
