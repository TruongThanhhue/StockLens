from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class ForecastResult:
    frame: pd.DataFrame


def make_forecast(history: pd.DataFrame, horizon: int, confidence: float) -> ForecastResult:
    """Posterior predictive MVP: Gaussian likelihood on daily log returns.

    A normal-inverse-gamma inspired shrinkage estimates mean/variance, then uses
    Monte Carlo paths to expose interval uncertainty rather than a point claim.
    """
    returns = history["log_return"].dropna().tail(504).to_numpy()
    n = len(returns)
    prior_strength, prior_mean = 20, 0.0
    mean = (n * returns.mean() + prior_strength * prior_mean) / (n + prior_strength)
    variance = ((returns - returns.mean()) ** 2).sum() / max(n - 1, 1)
    rng = np.random.default_rng(42)
    paths = history["Close"].iloc[-1] * np.exp(rng.normal(mean, np.sqrt(variance), size=(5000, horizon)).cumsum(axis=1))
    alpha = (1 - confidence) / 2
    dates = pd.bdate_range(history.index[-1] + pd.offsets.BDay(1), periods=horizon)
    output = pd.DataFrame({
        "forecast": np.median(paths, axis=0),
        "lower": np.quantile(paths, alpha, axis=0),
        "upper": np.quantile(paths, 1 - alpha, axis=0),
    }, index=dates)
    output.index.name = "date"
    return ForecastResult(output)
