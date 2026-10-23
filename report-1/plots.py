
"""Save presentation-ready charts from the exploratory pilot."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Reliable PNG output in VS Code, terminals and CI.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save_heatmap(values: pd.DataFrame, title: str, output: Path) -> None:
    arr = values.to_numpy()
    bound = max(float(np.max(np.abs(arr))), 0.01)
    fig, ax = plt.subplots(figsize=(9, 7))
    image = ax.imshow(arr, cmap="RdBu_r", vmin=-bound, vmax=bound)
    ax.set_xticks(range(len(values.columns)), values.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(values.index)), values.index)
    ax.set_xlabel("Follower (or stock B for same-day correlation)")
    ax.set_ylabel("Candidate leader (or stock A)")
    ax.set_title(title)
    if len(values) <= 12:
        for i in range(len(values.index)):
            for j in range(len(values.columns)):
                ax.text(j, i, f"{arr[i, j]:+.2f}", ha="center", va="center", fontsize=7,
                        color="white" if abs(arr[i, j]) > 0.65 * bound else "black")
    fig.colorbar(image, ax=ax, label="Correlation / directional score", shrink=0.8)
    fig.tight_layout()
    fig.savefig(output, dpi=170)
    plt.close(fig)


def save_ranking(rankings: pd.Series, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    rankings.sort_values().plot.barh(ax=ax)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.set_title("Exploratory net leadership rankings (not evidence of skill)")
    ax.set_xlabel("Sum of directional lead-lag scores")
    fig.tight_layout()
    fig.savefig(output, dpi=170)
    plt.close(fig)
