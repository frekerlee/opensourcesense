"""评分算法 — Fashion Score 计算引擎"""

from config import SCORE_WEIGHTS


def compute_fashion_score(
    social_heat: float,
    industry_impact: float,
    content_quality: float,
    trend_velocity: float,
    exclusivity: float,
    weights: dict = None,
) -> float:
    """加权计算综合 Fashion Score (0-100)"""
    w = weights or SCORE_WEIGHTS
    score = (
        social_heat * w["social_heat"]
        + industry_impact * w["industry_impact"]
        + content_quality * w["content_quality"]
        + trend_velocity * w["trend_velocity"]
        + exclusivity * w["exclusivity"]
    )
    return round(score, 1)


def get_score_color(score: float) -> str:
    """根据分数返回颜色（用于渐变条）"""
    if score >= 85:
        return "#2ED573"  # 绿色 - 优秀
    elif score >= 70:
        return "#FFA502"  # 橙色 - 良好
    elif score >= 50:
        return "#FF6B81"  # 粉色 - 一般
    else:
        return "#FF4757"  # 红色 - 低


def get_trend_icon(direction: str) -> str:
    """返回趋势图标"""
    icons = {"up": "△", "down": "▽", "stable": "―"}
    return icons.get(direction, "―")


def get_trend_class(direction: str) -> str:
    """返回趋势 CSS 类名"""
    classes = {"up": "trend-up", "down": "trend-down", "stable": "trend-stable"}
    return classes.get(direction, "trend-stable")
