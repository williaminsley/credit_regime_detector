from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def plot_stress_indicator(stress: pd.Series, out_dir: Path) -> None:
    s = stress.astype(float)

    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot baseline
    ax.plot(s.index, s.values, alpha=0.3, label="Stress flag")

    # Shade stress regions
    for date, val in s.items():
        if val == 1.0:
            ax.axvspan(
                date - pd.Timedelta(days=3),
                date + pd.Timedelta(days=3),
                color="red",
                alpha=0.3
            )

    ax.set_title("Credit Stress Regimes (HYG vs LQD)")
    ax.text(
        0.01,
        0.95,
        "Stress events are rare and cluster during systemic shocks (e.g. COVID-19)",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top"
    )
    ax.set_xlabel("Date")
    ax.set_yticks([0, 1])
    ax.set_ylabel("Stress regime")
    ax.legend()

    fig.tight_layout()
    out_dir.mkdir(exist_ok=True)
    fig.savefig(out_dir / "stress_indicator.png", dpi=200)
    plt.close(fig)