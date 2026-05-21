"""B站字幕获取 — 移植自 BibiGPT-v1 的核心逻辑

通过 Bilibili API 获取视频字幕，提取纯文本供 AI 总结使用。
"""

import requests
import json
import re
from typing import Optional


def get_video_info(bvid: str) -> Optional[dict]:
    """获取 B站视频信息（包括 aid, cid, title 等）"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data.get("code") == 0:
            return data["data"]
    except Exception:
        pass
    return None


def get_subtitle_urls(aid: int, cid: int) -> list[dict]:
    """获取字幕 URL 列表"""
    url = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data.get("code") == 0:
            subtitles = data.get("data", {}).get("subtitle", {}).get("subtitles", [])
            return subtitles
    except Exception:
        pass
    return []


def fetch_subtitle_text(bvid: str) -> tuple[str, str]:
    """获取 B站视频的字幕纯文本

    Returns:
        (title, subtitle_text) — 标题和字幕文本
    """
    info = get_video_info(bvid)
    if not info:
        return "", ""

    title = info.get("title", "")
    aid = info.get("aid", 0)
    pages = info.get("pages", [])

    if not pages:
        return title, ""

    cid = pages[0].get("cid", 0)
    subtitles = get_subtitle_urls(aid, cid)

    if not subtitles:
        return title, ""

    # 优先中文，否则第一个
    best = None
    for sub in subtitles:
        if sub.get("lan") == "zh-CN":
            best = sub
            break
    if not best:
        best = subtitles[0]

    sub_url = best.get("subtitle_url", "")
    if sub_url.startswith("//"):
        sub_url = "https:" + sub_url

    try:
        resp = requests.get(sub_url, timeout=10)
        data = resp.json()
    except Exception:
        return title, ""

    # 提取文本（去掉时间戳）
    body = data if isinstance(data, list) else data.get("body", [])
    texts = []
    for item in body:
        content = item.get("content", "")
        # 清理 HTML 标签
        content = re.sub(r"<[^>]+>", "", content)
        if content.strip():
            texts.append(content.strip())

    return title, "\n".join(texts)


def extract_video_id(url: str) -> Optional[str]:
    """从 B站 URL 提取 BV 号"""
    # 支持格式: BVxxx, /video/BVxxx, bvid=xxx
    match = re.search(r"(BV[a-zA-Z0-9]{10})", url)
    if match:
        return match.group(1)
    # 也支持 av 号
    match = re.search(r"av(\d+)", url, re.IGNORECASE)
    if match:
        return f"av{match.group(1)}"
    return None


if __name__ == "__main__":
    # 测试
    test_bvid = "BV1Sa5p6SEqx"
    title, text = fetch_subtitle_text(test_bvid)
    print(f"标题: {title}")
    print(f"字幕长度: {len(text)} 字")
    print(f"前200字: {text[:200]}...")
