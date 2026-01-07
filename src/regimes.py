from __future__ import annotations

import pandas as pd


def detect_credit_stress(
    features: pd.DataFrame,
    z_thresh: float = 1.5,
    vol_thresh: float = 0.02,
    corr_thresh: float = 0.6,
) -> pd.Series:
    """
    Rule-based stress regime detector (desk-friendly and explainable).

    Stress regime triggers when:
    - HY underperforms IG unusually (spread_z high)
    - spread proxy is volatile (spread_vol_20 high)
    - credit becomes highly equity-correlated (corr_hyg_spy_60 high)

    Returns a boolean series indexed like features.
    """
    required = {"spread_z", "spread_vol_20", "corr_hyg_spy_60"}
    missing = required - set(features.columns)
    if missing:
        raise ValueError(f"Missing required feature columns: {sorted(missing)}")

    stress = (
        (features["spread_z"] > z_thresh)
        & (features["spread_vol_20"] > vol_thresh)
        & (features["corr_hyg_spy_60"] > corr_thresh)
    )
    return stress.rename("stress")