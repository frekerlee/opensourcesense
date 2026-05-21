"""Plotly 图表组件 — 趋势分析页使用"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def render_brand_bar_chart(brand_df: pd.DataFrame):
    """品牌热度 TOP10 柱状图"""
    if brand_df.empty:
        st.caption("暂无数据")
        return

    fig = px.bar(
        brand_df,
        x="count",
        y="brand",
        orientation="h",
        color="count",
        color_continuous_scale=["#2A2D33", "#FF6B81", "#FF4757"],
        text="count",
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(color="#E8E6E3", size=11),
        marker=dict(line=dict(width=0)),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(
            categoryorder="total ascending",
            color="#E8E6E3",
            tickfont=dict(size=12),
            gridcolor="#2A2D33",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=30, t=10, b=10),
        height=350,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_category_pie(cat_df: pd.DataFrame):
    """内容类型分布饼图"""
    if cat_df.empty:
        st.caption("暂无数据")
        return

    colors = ["#FF4757", "#FF6B81", "#FFA502", "#D4AF37", "#2ED573", "#1E90FF"]
    fig = go.Figure(
        go.Pie(
            labels=cat_df["category"],
            values=cat_df["count"],
            hole=0.5,
            marker=dict(colors=colors[: len(cat_df)]),
            textinfo="label+percent",
            textfont=dict(color="#E8E6E3", size=11),
            hovertemplate="%{label}: %{value}篇<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_source_bar(source_df: pd.DataFrame):
    """来源贡献度排名"""
    if source_df.empty:
        st.caption("暂无数据")
        return

    fig = px.bar(
        source_df.head(10),
        x="count",
        y="source",
        orientation="h",
        color="count",
        color_continuous_scale=["#2A2D33", "#D4AF37"],
        text="count",
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(color="#E8E6E3", size=11),
        marker=dict(line=dict(width=0)),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(
            categoryorder="total ascending",
            color="#E8E6E3",
            tickfont=dict(size=11),
            gridcolor="#2A2D33",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=30, t=10, b=10),
        height=350,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_trend_timeline(articles: list[dict]):
    """文章发布时间线（按天聚合热度）"""
    if not articles:
        st.caption("暂无数据")
        return

    df = pd.DataFrame(articles)
    df["date"] = pd.to_datetime(df["published_date"])
    daily = df.groupby("date").agg(
        avg_score=("fashion_score", "mean"),
        count=("id", "count"),
        max_score=("fashion_score", "max"),
    ).reset_index().sort_values("date")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["avg_score"],
            mode="lines+markers",
            name="平均评分",
            line=dict(color="#FF4757", width=2.5),
            marker=dict(color="#FF4757", size=8),
        )
    )
    fig.add_trace(
        go.Bar(
            x=daily["date"],
            y=daily["count"],
            name="文章数",
            marker=dict(color="rgba(212, 175, 55, 0.4)"),
            yaxis="y2",
        )
    )

    fig.update_layout(
        xaxis=dict(color="#9B9B9B", gridcolor="#2A2D33", tickformat="%m-%d", tickfont={"size": 10}),
        yaxis=dict(
            title="平均评分",
            titlefont=dict(color="#FF4757", size=10),
            color="#FF4757",
            gridcolor="#2A2D33",
            range=[0, 100],
        ),
        yaxis2=dict(
            title="文章数",
            titlefont=dict(color="#D4AF37", size=10),
            color="#D4AF37",
            overlaying="y",
            side="right",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#9B9B9B", size=10),
        ),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
