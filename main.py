from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.data_loader import DownloadConfig, download_adj_close
from src.features import build_feature_frame, daily_returns
from src.regimes import detect_credit_stress
from src.metrics import summary_stats
from src.plots import plot_stress_indicator

def backtest_lqd_hyg_risk_off(prices: pd.DataFrame, stress: pd.Series) -> pd.Series:
    """
    Simple desk-style toy strategy:
    - Base position: long LQD, short HYG (credit quality tilt)
    - When stress=True: go flat (risk-off)
    """
    rets = daily_returns(prices)[["LQD", "HYG"]]
    common = rets.index.intersection(stress.index)
    rets = rets.loc[common]
    stress = stress.loc[common]

    strat = (rets["LQD"] - rets["HYG"]).where(~stress, 0.0)
    strat.name = "strategy_ret"
    return strat


def main() -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    cfg = DownloadConfig(tickers=("HYG", "LQD", "SPY"), start="2018-01-01", end=None)
    prices = download_adj_close(cfg)
    features = build_feature_frame(prices)
    stress = detect_credit_stress(features)
    plot_stress_indicator(stress, out_dir)

    # Save outputs
    features.to_csv(out_dir / "features.csv")
    stress.to_frame().to_csv(out_dir / "stress_flags.csv")

    strat_rets = backtest_lqd_hyg_risk_off(prices, stress)
    strat_rets.to_frame().to_csv(out_dir / "strategy_returns.csv")

    stats = summary_stats(strat_rets)
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv(out_dir / "strategy_summary.csv", index=False)
    print(stats_df)

    print("Saved outputs to outputs/")
    print(stats_df.to_string(index=False))
    print(f"Stress regime frequency: {stress.mean():.2%}")


if __name__ == "__main__":
    main()
