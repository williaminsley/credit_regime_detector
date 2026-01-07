from __future__ import annotations

import pandas as pd


def sanity_check_features(features: pd.DataFrame) -> list[str]:
    warnings: list[str] = []

    if features.isna().any().any():
        warnings.append("Features contain NaNs after build (unexpected).")

    # stress detectors should not flip constantly
    if "spread_z" in features.columns:
        if features["spread_z"].abs().max() > 10:
            warnings.append("spread_z extreme (>10). Potential data issue or thin window.")

    return warnings


def regime_flip_rate(regime: pd.Series) -> float:
    """Fraction of days where regime differs from previous day."""
    flips = regime.ne(regime.shift(1)).sum()
    return float(flips / len(regime))