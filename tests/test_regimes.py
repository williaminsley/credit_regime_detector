import pandas as pd
from src.regimes import detect_credit_stress


def test_detect_credit_stress_flags_expected() -> None:
    df = pd.DataFrame(
        {
            "spread_z": [0.0, 2.0, 3.0],
            "spread_vol_20": [0.01, 0.03, 0.03],
            "corr_hyg_spy_60": [0.2, 0.7, 0.8],
        },
        index=pd.date_range("2024-01-01", periods=3, freq="D"),
    )

    stress = detect_credit_stress(df, z_thresh=1.5, vol_thresh=0.02, corr_thresh=0.6)
    assert stress.tolist() == [False, True, True]