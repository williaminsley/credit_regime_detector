from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class DownloadConfig:
    tickers: tuple[str, ...] = ("HYG", "LQD", "SPY")
    start: str = "2018-01-01"
    end: str = "2024-01-01"
    cache_path: str = "outputs/cache/prices.parquet"


def download_adj_close(cfg: DownloadConfig) -> pd.DataFrame:
    cache_file = Path(cfg.cache_path)
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    if cache_file.exists():
        prices = pd.read_parquet(cache_file)
        return prices

    data = yf.download(list(cfg.tickers), start=cfg.start, end=cfg.end, auto_adjust=False, progress=False)

    if isinstance(data.columns, pd.MultiIndex):
        adj = data["Adj Close"].copy()
    else:
        adj = data[["Adj Close"]].rename(columns={"Adj Close": cfg.tickers[0]})

    adj = adj.dropna(how="any")
    adj.to_parquet(cache_file)
    return adj