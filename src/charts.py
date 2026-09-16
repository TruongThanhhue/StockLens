from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

BG, GRID, TEXT, MINT, MUTED = "#101820", "#263640", "#e6edf3", "#4fd1b5", "#92a2ad"


def _layout(fig: go.Figure, title: str) -> go.Figure:
    return fig.update_layout(title=None, paper_bgcolor=BG, plot_bgcolor=BG, font={"color": TEXT, "family": "IBM Plex Sans"}, margin={"l": 6, "r": 12, "t": 15, "b": 5}, height=420, hovermode="x unified", legend={"orientation": "h", "y": 1.08}, xaxis={"showgrid": False}, yaxis={"gridcolor": GRID, "side": "right", "title": None, "tickformat": ",.2f"})


def price_chart(history: pd.DataFrame, ticker: str) -> go.Figure:
    recent = history.tail(180)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent.index, y=recent["Close"], name=f"{ticker} close", line={"color": TEXT, "width": 2.1}, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=recent.index, y=recent["ma_20"], name="MA 20", line={"color": "#d9be70", "width": 1.25}, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=recent.index, y=recent["ma_50"], name="MA 50", line={"color": "#759ac0", "width": 1.25}, hovertemplate="%{y:,.2f}<extra></extra>"))
    return _layout(fig, "")


def forecast_chart(history: pd.DataFrame, forecast: pd.DataFrame, ticker: str, confidence: float) -> go.Figure:
    recent = history.tail(90)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent.index, y=recent["Close"], name="Lịch sử", line={"color": TEXT, "width": 2}, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast["upper"], name=f"Dải {int(confidence*100)}%", line={"color": "rgba(135,229,193,0)", "width": 0}, showlegend=False, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast["lower"], name=f"Dải credible {int(confidence*100)}%", fill="tonexty", fillcolor="rgba(79,209,181,.16)", line={"color": "rgba(79,209,181,0)", "width": 0}, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast["forecast"], name="Median posterior", line={"color": MINT, "width": 3, "dash": "dot"}, hovertemplate="%{y:,.2f}<extra></extra>"))
    return _layout(fig, "")
