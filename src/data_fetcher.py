from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600, show_spinner=False)
def download_history(ticker: str, years: int) -> pd.DataFrame:
    if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
        raise ValueError("Mã cổ phiếu không hợp lệ. Ví dụ: VCB, FPT hoặc HPG.")
    try:
        from vnstock import Quote
        start = date.today().replace(year=date.today().year - years).isoformat()
        frame = Quote(symbol=ticker, source="KBS").history(start=start, end=date.today().isoformat(), interval="d")
    except ImportError as exc:
        raise ValueError("Chưa cài VNstock. Hãy chạy lệnh cài dependencies trong README.") from exc
    except Exception as exc:
        raise ValueError(f"VNstock không thể lấy dữ liệu cho mã {ticker}. Kiểm tra mã hoặc API key VNstock.") from exc
    if frame.empty or len(frame) < 80:
        raise ValueError(f"Không có đủ dữ liệu lịch sử cho mã {ticker}.")
    frame.columns = [str(column).strip().lower() for column in frame.columns]
    date_column = next((name for name in ("time", "date", "tradingdate") if name in frame.columns), None)
    if date_column is None:
        raise ValueError("VNstock trả về dữ liệu không có cột ngày giao dịch.")
    frame[date_column] = pd.to_datetime(frame[date_column])
    frame = frame.set_index(date_column)
    aliases = {"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
    frame = frame.rename(columns=aliases)
    needed = ["Open", "High", "Low", "Close", "Volume"]
    if not set(needed).issubset(frame.columns):
        raise ValueError("VNstock trả về thiếu OHLCV cho mã này.")
    return frame[needed].apply(pd.to_numeric, errors="coerce").dropna().sort_index()

