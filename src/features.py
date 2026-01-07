from __future__ import annotations

import pandas as pd


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Simple daily pct returns."""
    return prices.pct_change().dropna(how="any")


def rolling_vol(returns: pd.Series, window: int = 20) -> pd.Series:
    """Rolling annualised volatility proxy is not needed; keep it daily-scale."""
    return returns.rolling(window).std()


def rolling_corr(a: pd.Series, b: pd.Series, window: int = 60) -> pd.Series:
    return a.rolling(window).corr(b)


def zscore(s: pd.Series, window: int = 60) -> pd.Series:
    mean = s.rolling(window).mean()
    std = s.rolling(window).std()
    return (s - mean) / std


def build_feature_frame(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact feature set aligned to credit e-trading:
    - HY vs IG "spread proxy" via relative returns (HYG - LQD)
    - rolling vol on spread proxy
    - rolling correlation of credit vs equities
    """
    rets = daily_returns(prices)

    required = {"HYG", "LQD", "SPY"}
    missing = required - set(rets.columns)
    if missing:
        raise ValueError(
            f"Feature pipeline requires credit ETFs HYG and LQD. "
            f"Missing: {sorted(missing)}"
        )


    spread_proxy = (rets["HYG"] - rets["LQD"]).rename("spread_proxy")
    spread_z = zscore(spread_proxy, window=60).rename("spread_z")

    vol_20 = rolling_vol(spread_proxy, window=20).rename("spread_vol_20")

    corr_hyg_spy = rolling_corr(rets["HYG"], rets["SPY"], window=60).rename("corr_hyg_spy_60")
    corr_lqd_spy = rolling_corr(rets["LQD"], rets["SPY"], window=60).rename("corr_lqd_spy_60")

    out = pd.concat([spread_proxy, spread_z, vol_20, corr_hyg_spy, corr_lqd_spy], axis=1)
    out = out.dropna(how="any")
    return out