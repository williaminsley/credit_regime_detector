# Credit Regime Detector

A production-style Python project that detects **credit stress regimes** using transparent, desk-aligned signals and evaluates a simple credit-quality tilt strategy.

## Motivation
In stressed markets, high-yield credit tends to underperform investment-grade, volatility increases, and credit becomes more equity-correlated. This project formalises that intuition into a **testable regime framework**.

## Signals Used
- HY vs IG relative returns (HYG − LQD)
- Rolling z-score of relative spread proxy
- Rolling volatility of credit spreads
- Rolling correlation between credit ETFs and equities (SPY)

## Regime Definition
A **credit stress regime** is flagged when:
- Relative HY underperformance is statistically extreme
- Credit spread volatility is elevated
- Credit-equity correlation increases

The rules are intentionally **explainable** and aligned with trader intuition.

## Strategy Example
A toy LQD–HYG relative value strategy is evaluated:
- Risk-on: Long LQD, short HYG
- Risk-off: Flat exposure during stress regimes

Performance metrics include total return, max drawdown and Sharpe ratio.

## Engineering Features
- Deterministic feature pipeline
- Offline-safe testing (unit vs integration separation)
- Parquet-based data caching
- Continuous Integration (GitHub Actions)

## Outputs
Running `python main.py` produces:
- `features.csv`
- `stress_flags.csv`
- `strategy_returns.csv`
- `strategy_summary.csv`

## Example Strategy Output

A simple regime-aware risk-off strategy was evaluated to demonstrate end-to-end signal generation, backtesting, and risk evaluation.

Example output (single run):

| Metric        | Value      |
|---------------|------------|
| Total Return  | -8.7%      |
| Max Drawdown  | -27.0%     |
| Sharpe Ratio  | -0.10      |

> Note: This strategy is included as a demonstrator of regime detection, feature engineering, and evaluation infrastructure. Results are not presented as optimised or investable and are intentionally left un-tuned to avoid overfitting.
