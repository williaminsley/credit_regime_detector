from __future__ import annotations

import numpy as np
import pandas as pd


def max_drawdown(equity_curve: pd.Series) -> float:
    peak = equity_curve.cummax()
    dd = equity_curve / peak - 1.0
    return float(dd.min())


def sharpe_ratio(daily_returns: pd.Series, annualisation: int = 252) -> float:
    mu = daily_returns.mean()
    sigma = daily_returns.std()
    if sigma == 0 or np.isnan(sigma):
        return 0.0
    return float((mu / sigma) * np.sqrt(annualisation))


def summary_stats(daily_returns: pd.Series) -> dict[str, float]:
    equity = (1 + daily_returns).cumprod()
    return {
        "total_return": float(equity.iloc[-1] - 1.0),
        "max_drawdown": max_drawdown(equity),
        "sharpe": sharpe_ratio(daily_returns),
    }