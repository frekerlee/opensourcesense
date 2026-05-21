"""指标展示组件"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS


def render_score_gauge(score: float, size: int = 160):
    """渲染一个圆形评分表盘"""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"color": "#E8E6E3", "size": 42, "family": "Helvetica Neue"},
                     "suffix": ""},
            title={"text": "FASHION SCORE", "font": {"color": "#9B9B9B", "size": 12}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#9B9B9B",
                    "tickfont": {"color": "#9B9B9B", "size": 9},
                },
                "bar": {"color": "#FF4757" if score < 70 else "#FFA502" if score < 85 else "#2ED573",
                         "thickness": 0.15},
                "bgcolor": "#1A1D23",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "#2A1A1D"},
                    {"range": [50, 70], "color": "#2A2518"},
                    {"range": [70, 85], "color": "#252A1A"},
                    {"range": [85, 100], "color": "#1A2A1D"},
                ],
            },
        )
    )

    fig.update_layout(
        width=size,
        height=size + 20,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#9B9B9B"},
    )
    st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})


def render_radar_chart(article: dict):
    """渲染指标雷达图"""
    categories = ["社媒热度", "行业影响力", "内容质量", "趋势速度", "独家性"]
    values = [
        article["social_heat"],
        article["industry_impact"],
        article["content_quality"],
        max(0, article["trend_velocity"]),  # trend_velocity can be negative
        article["exclusivity"],
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(255, 71, 87, 0.25)",
            line=dict(color="#FF4757", width=2),
            name=article["title_cn"][:20],
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#9B9B9B",
                gridcolor="#2A2D33",
                tickfont={"color": "#9B9B9B", "size": 9},
            ),
            angularaxis=dict(
                color="#E8E6E3",
                gridcolor="#2A2D33",
                tickfont={"size": 11},
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=20, b=20),
        height=350,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_trend_line(score_history: list[dict]):
    """渲染评分趋势线"""
    if not score_history:
        return

    df = pd.DataFrame(score_history)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["score"],
            mode="lines+markers",
            line=dict(color="#FF4757", width=2),
            marker=dict(color="#FF4757", size=6),
            fill="tozeroy",
            fillcolor="rgba(255, 71, 87, 0.1)",
        )
    )

    fig.update_layout(
        xaxis=dict(color="#9B9B9B", gridcolor="#2A2D33", tickfont={"size": 9}),
        yaxis=dict(color="#9B9B9B", gridcolor="#2A2D33", range=[0, 100], tickfont={"size": 9}),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_metric_bar(label: str, value: float, max_val: float = 100):
    """渲染单条指标条"""
    pct = min(100, max(0, value / max_val * 100))
    color = "#2ED573" if pct >= 85 else "#FFA502" if pct >= 70 else "#FF4757"
    html = f"""
    <div style="margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
            <span style="color:#9B9B9B;">{label}</span>
            <span style="color:{color}; font-weight:600;">{value:.0f}</span>
        </div>
        <div style="height:3px; background:#2A2D33; border-radius:2px;">
            <div style="height:100%; width:{pct}%; background:{color}; border-radius:2px;"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_row(metrics: dict):
    """横向渲染一组指标"""
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(label=label, value=value)
