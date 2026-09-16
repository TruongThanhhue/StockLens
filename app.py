"""StockLens — financial intelligence workspace for Bayesian forecasts."""
from __future__ import annotations

from html import escape

import streamlit as st

from src.charts import price_chart, forecast_chart
from src.data_fetcher import download_history
from src.features import add_indicators
from src.forecast import make_forecast
from src.evaluation import calculate_metrics

st.set_page_config(page_title="StockLens | Forecast Workspace", page_icon="SL", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
:root { --canvas:#0a0f14; --surface:#101820; --surface-2:#15212a; --rule:#263640; --text:#e6edf3; --muted:#92a2ad; --accent:#4fd1b5; --positive:#4fd18a; --negative:#f08b7c; --warning:#d9be70; }
html, body, [class*="css"] { font-family:'IBM Plex Sans', sans-serif; }
.stApp { background:var(--canvas); color:var(--text); }
[data-testid="stSidebar"] { background:#0d141b; border-right:1px solid var(--rule); }
[data-testid="stSidebar"] > div:first-child { padding-top:1.4rem; }
[data-testid="stSidebar"] * { color:var(--text); }
[data-testid="stSidebar"] .stCaption { color:var(--muted)!important; }
[data-testid="stSidebar"] label { font-size:.72rem!important; letter-spacing:.08em; text-transform:uppercase; color:var(--muted)!important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div, [data-testid="stSidebar"] input { background:var(--surface)!important; border-color:var(--rule)!important; }
.block-container { max-width:1600px; padding:1.5rem 2.25rem 3.5rem; }
.brand-lockup { display:flex; gap:.75rem; align-items:center; margin-bottom:1.9rem; }
.brand-mark { display:grid; place-items:center; width:28px; height:28px; border:1px solid var(--accent); color:var(--accent); font-family:'IBM Plex Mono',monospace; font-size:.72rem; }
.brand-name { font-family:'IBM Plex Mono',monospace; font-weight:600; letter-spacing:.08em; font-size:.82rem; }
.rail-caption { font-size:.78rem; color:var(--muted); line-height:1.55; }
.workspace-top { display:flex; justify-content:space-between; gap:1.5rem; align-items:end; padding:.6rem 0 1.5rem; border-bottom:1px solid var(--rule); margin-bottom:1.75rem; }
.workspace-top h1 { font-size:clamp(1.8rem,3vw,3rem); letter-spacing:-.05em; line-height:1; margin:.3rem 0 0; font-weight:600; }
.kicker, .section-kicker, .metric-label { font-family:'IBM Plex Mono',monospace; font-size:.68rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }
.workspace-meta { font-family:'IBM Plex Mono',monospace; color:var(--muted); font-size:.72rem; text-align:right; line-height:1.65; }
.instrument-header { display:grid; grid-template-columns:1.25fr repeat(3, 1fr); border:1px solid var(--rule); background:var(--surface); margin-bottom:2rem; }
.instrument-cell { min-height:108px; padding:1.15rem 1.25rem; border-right:1px solid var(--rule); }
.instrument-cell:last-child { border-right:0; }
.instrument-ticker { font-family:'IBM Plex Mono',monospace; font-size:2.05rem; letter-spacing:-.08em; margin:.45rem 0 .2rem; }
.instrument-value { font-family:'IBM Plex Mono',monospace; font-size:1.45rem; letter-spacing:-.05em; margin:.65rem 0 0; color:var(--text); }
.positive { color:var(--positive)!important; } .negative { color:var(--negative)!important; }
.section-head { display:flex; justify-content:space-between; align-items:end; padding-bottom:.7rem; border-bottom:1px solid var(--rule); margin:0 0 1rem; }
.section-head h2 { font-size:1rem; margin:.3rem 0 0; letter-spacing:-.015em; font-weight:600; }
.section-note { color:var(--muted); font-size:.78rem; text-align:right; }
.panel { border:1px solid var(--rule); background:var(--surface); padding:1.05rem; }
.technical-list { padding:0 .15rem; }
.technical-row { display:flex; align-items:baseline; justify-content:space-between; gap:1rem; padding:1rem 0; border-bottom:1px solid var(--rule); }
.technical-row:last-child { border-bottom:0; }
.technical-row span { color:var(--muted); font-size:.82rem; }.technical-row strong { font-family:'IBM Plex Mono',monospace; font-size:1rem; font-weight:500; }
.technical-footnote { color:var(--muted); font-size:.78rem; line-height:1.55; border-top:1px solid var(--rule); padding-top:1rem; margin-top:.3rem; }
.assessment { display:grid; grid-template-columns:repeat(4,1fr); border:1px solid var(--rule); background:var(--surface); margin-bottom:1.2rem; }
.assessment-item { padding:1rem 1.15rem; border-right:1px solid var(--rule); }.assessment-item:last-child { border:0; }
.assessment-value { display:block; font-family:'IBM Plex Mono',monospace; font-size:1.08rem; margin-top:.55rem; }
.disclaimer { border-left:2px solid var(--warning); padding:.85rem 1rem; color:var(--muted); background:#13171a; font-size:.8rem; line-height:1.55; }
.stButton button, .stDownloadButton button { width:100%; min-height:42px; border:1px solid var(--accent); background:var(--accent); color:#07120f; font-weight:700; border-radius:6px; box-shadow:none; }
.stButton button:hover, .stDownloadButton button:hover { background:#6ee0c6; border-color:#6ee0c6; color:#07120f; }
.stButton button:active, .stDownloadButton button:active { transform:translateY(1px); }
[data-testid="stPlotlyChart"] { border:0; }
[data-testid="stSpinner"] { color:var(--accent); }
@media (max-width: 900px) { .block-container { padding:1.25rem 1rem 2.5rem; } .workspace-top { align-items:start; flex-direction:column; } .workspace-meta { text-align:left; } .instrument-header, .assessment { grid-template-columns:repeat(2,1fr); } .instrument-cell:nth-child(2) { border-right:0; } .instrument-cell { border-bottom:1px solid var(--rule); } .instrument-cell:nth-last-child(-n+2) { border-bottom:0; } .assessment-item:nth-child(2) { border-right:0; } .assessment-item:nth-last-child(-n+2) { border-top:1px solid var(--rule); } }
@media (max-width: 520px) { .instrument-header, .assessment { grid-template-columns:1fr; } .instrument-cell, .instrument-cell:nth-child(2), .assessment-item, .assessment-item:nth-child(2) { border-right:0; border-bottom:1px solid var(--rule); } .instrument-cell:last-child, .assessment-item:last-child { border-bottom:0; } }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand-lockup"><div class="brand-mark">SL</div><div class="brand-name">STOCKLENS</div></div>', unsafe_allow_html=True)
    st.markdown('<p class="rail-caption">Vietnam equities<br>Bayesian forecast workspace</p>', unsafe_allow_html=True)
    st.divider()
    ticker = st.text_input("Mã cổ phiếu Việt Nam", "VCB", help="Ví dụ: VCB, FPT, HPG, VNM.").strip().upper()
    years = st.select_slider("Dữ liệu lịch sử", options=[1, 2, 3, 5], value=3, format_func=lambda x: f"{x} năm")
    horizon = st.select_slider("Horizon dự báo", options=[7, 14, 30], value=14, format_func=lambda x: f"{x} ngày")
    confidence = st.select_slider("Khoảng credible", options=[0.80, 0.90, 0.95], value=0.90, format_func=lambda x: f"{int(x*100)}%")
    run = st.button("Cập nhật phân tích", use_container_width=True)
    st.divider()
    st.markdown('<p class="rail-caption">Nguồn dữ liệu: VNstock<br>Mô hình: posterior predictive</p>', unsafe_allow_html=True)

st.markdown("""
<section class="workspace-top">
  <div><div class="kicker">Financial intelligence / forecast desk</div><h1>Forecast workspace</h1></div>
  <div class="workspace-meta">DỮ LIỆU LỊCH SỬ · VNSTOCK<br>ƯỚC LƯỢNG XÁC SUẤT · POSTERIOR PREDICTIVE</div>
</section>
""", unsafe_allow_html=True)

if "submitted" not in st.session_state:
    st.session_state.submitted = True
if run:
    st.session_state.submitted = True

try:
    with st.spinner(f"Đang lấy và xử lý dữ liệu {ticker}..."):
        history = add_indicators(download_history(ticker, years))
        result = make_forecast(history, horizon, confidence)
        metrics = calculate_metrics(history)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
except Exception as exc:
    st.error("Không thể hoàn tất phân tích. Hãy kiểm tra kết nối mạng hoặc mã cổ phiếu.")
    st.caption(f"Chi tiết kỹ thuật: {exc}")
    st.stop()

last = float(history["Close"].iloc[-1])
end_price = float(result.frame["forecast"].iloc[-1])
change = (end_price / last - 1) * 100
volatility = float(history["volatility_20"].iloc[-1]) * 100
trend = "Tăng" if change >= 0 else "Giảm"
safe_ticker = escape(ticker)
trend_class = "positive" if change >= 0 else "negative"
st.markdown(f"""
<section class="instrument-header">
  <div class="instrument-cell"><div class="metric-label">Instrument</div><div class="instrument-ticker">{safe_ticker}</div><div class="section-note">{years} năm dữ liệu lịch sử</div></div>
  <div class="instrument-cell"><div class="metric-label">Close gần nhất</div><div class="instrument-value">{last:,.2f}</div></div>
  <div class="instrument-cell"><div class="metric-label">Xu hướng {horizon} phiên</div><div class="instrument-value {trend_class}">{trend}</div><div class="section-note {trend_class}">{change:+.2f}% median forecast</div></div>
  <div class="instrument-cell"><div class="metric-label">Biến động 20 phiên</div><div class="instrument-value">{volatility:.2f}%</div></div>
</section>
""", unsafe_allow_html=True)

left, right = st.columns((1.45, 1), gap="large")
with left:
    st.markdown('<div class="section-head"><div><div class="section-kicker">Market view</div><h2>Giá lịch sử & đường trung bình</h2></div><div class="section-note">Close · MA20 · MA50</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.plotly_chart(price_chart(history, ticker), use_container_width=True, config={"displaylogo": False, "responsive": True})
    st.markdown('</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="section-head"><div><div class="section-kicker">Technical context</div><h2>Tín hiệu kỹ thuật</h2></div><div class="section-note">OHLCV lịch sử</div></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="panel technical-list">
      <div class="technical-row"><span>RSI (14)</span><strong>{history['rsi_14'].iloc[-1]:.1f}</strong></div>
      <div class="technical-row"><span>MA20 so với MA50</span><strong>{(history['ma_20'].iloc[-1]/history['ma_50'].iloc[-1]-1)*100:+.2f}%</strong></div>
      <div class="technical-row"><span>Khối lượng / TB 20 phiên</span><strong>{history['volume_ratio'].iloc[-1]:.2f}x</strong></div>
      <div class="technical-footnote">Chỉ báo mô tả dữ liệu quá khứ, không xác nhận xu hướng tương lai.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2.25rem'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="section-head"><div><div class="section-kicker">Bayesian forecast</div><h2>Posterior predictive · {horizon} phiên tới</h2></div><div class="section-note">Median forecast · dải credible {int(confidence * 100)}%</div></div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.plotly_chart(forecast_chart(history, result.frame, ticker, confidence), use_container_width=True, config={"displaylogo": False, "responsive": True})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:2.25rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="section-kicker">Model assessment</div><h2>Đánh giá baseline</h2></div><div class="section-note">Naive forecast · 30 phiên gần nhất</div></div>', unsafe_allow_html=True)
assessment = "".join(f'<div class="assessment-item"><div class="metric-label">{escape(name)}</div><span class="assessment-value">{escape(value)}</span></div>' for name, value in metrics.items())
st.markdown(f'<section class="assessment">{assessment}</section>', unsafe_allow_html=True)

csv = result.frame.reset_index().to_csv(index=False, float_format="%.2f").encode("utf-8-sig")
download_col, disclosure_col = st.columns((.28, .72), gap="large")
with download_col:
    st.download_button("Tải forecast CSV", csv, file_name=f"forecast_{ticker}_{horizon}d.csv", mime="text/csv")
with disclosure_col:
    st.markdown("<p class='disclaimer'>Công cụ phục vụ học tập và nghiên cứu. Dự báo tài chính luôn có rủi ro; đây không phải khuyến nghị mua, bán hoặc nắm giữ chứng khoán.</p>", unsafe_allow_html=True)
