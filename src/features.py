from __future__ import annotations

import numpy as np
import pandas as pd


def add_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    data["log_return"] = np.log(data["Close"]).diff()
    data["ma_20"] = data["Close"].rolling(20).mean()
    data["ma_50"] = data["Close"].rolling(50).mean()
    delta = data["Close"].diff()
    gains, losses = delta.clip(lower=0), -delta.clip(upper=0)
    rs = gains.rolling(14).mean() / losses.rolling(14).mean().replace(0, np.nan)
    data["rsi_14"] = 100 - (100 / (1 + rs))
    data["volatility_20"] = data["log_return"].rolling(20).std() * np.sqrt(252)
    data["volume_ratio"] = data["Volume"] / data["Volume"].rolling(20).mean()
    return data
