from src.data_loader import DownloadConfig, download_adj_close
import pytest
pytestmark = pytest.mark.integration

def test_download_returns_dataframe() -> None:
    cfg = DownloadConfig(tickers=("SPY",), start="2024-01-01", end="2024-02-01")
    df = download_adj_close(cfg)
    assert df is not None
    assert df.shape[1] == 1