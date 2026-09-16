from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_metrics(history: pd.DataFrame) -> dict[str, str]:
    actual = history["Close"].tail(30)
    predicted = history["Close"].shift(1).tail(30)
    error = actual - predicted
    mae = error.abs().mean()
    rmse = np.sqrt((error ** 2).mean())
    mape = (error.abs() / actual).mean() * 100
    return {"MAE (naive)": f"{mae:,.2f}", "RMSE (naive)": f"{rmse:,.2f}", "MAPE (naive)": f"{mape:.2f}%", "Phiên cuối": history.index[-1].strftime("%d/%m/%Y")}
