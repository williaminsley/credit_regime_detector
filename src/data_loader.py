from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class DownloadConfig:
    tickers: tuple[str, ...] = ("LQD", "HYG", "SPY", "TLT", "^VIX")
    start: str = "2015-01-01"
    end: str | None = None


def download_adj_close(cfg: DownloadConfig) -> pd.DataFrame:
    """
    Download adjusted close prices for a list of tickers using yfinance.
    Returns a DataFrame indexed by date with columns = tickers.
    """
    data = yf.download(list(cfg.tickers), start=cfg.start, end=cfg.end, auto_adjust=False, progress=False)

    # yfinance returns a multi-index column frame when multiple tickers are used
    if isinstance(data.columns, pd.MultiIndex):
        adj = data["Adj Close"].copy()
    else:
        # single ticker case
        adj = data[["Adj Close"]].rename(columns={"Adj Close": cfg.tickers[0]})

    adj = adj.dropna(how="all")
    return adj
