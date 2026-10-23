"""Daily log returns, contemporaneous correlation and directional lead-lag scores."""

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Log returns using adjusted prices; never forward-fill missing observations."""
    prices = prices.sort_index().copy()
    if prices.index.has_duplicates or prices.columns.has_duplicates:
        raise ValueError("Duplicate dates or ticker names.")
    if prices.shape[1] < 2:
        raise ValueError("Need at least two stocks.")
    if (prices <= 0).any().any():
        raise ValueError("All available price observations must be positive.")
    return np.log(prices).diff()


def calculate_matrices(returns: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (same-day correlation, forward correlation, lead-lag score).

    forward[i,j] = corr(r_i,t, r_j,t+1).
    The shift is positional, among ADJACENT observations in the original calendar.
    Rows with incomplete observations are removed only AFTER forming adjacent pairs.
    """
    same_day = returns.dropna(how="any").corr()
    if same_day.isna().any().any():
        raise ValueError("Not enough complete returns for the same-day correlations.")

    today = returns.iloc[:-1].to_numpy(dtype=float)
    next_session = returns.iloc[1:].to_numpy(dtype=float)
    valid = np.isfinite(today).all(axis=1) & np.isfinite(next_session).all(axis=1)
    today, next_session = today[valid], next_session[valid]
    n = len(today)
    if n < 60:
        raise ValueError(f"Only {n} valid adjacent-session pairs; need at least 60.")

    today_std = today.std(axis=0, ddof=1)
    next_std = next_session.std(axis=0, ddof=1)
    if (today_std == 0).any() or (next_std == 0).any():
        raise ValueError("Zero-variance returns detected for a stock.")

    x = (today - today.mean(axis=0)) / today_std
    y = (next_session - next_session.mean(axis=0)) / next_std
    tickers = returns.columns
    forward = pd.DataFrame(x.T @ y / (n - 1), index=tickers, columns=tickers)
    lead_lag = forward - forward.T
    np.fill_diagonal(lead_lag.values, 0.0)
    return same_day, forward, lead_lag


def rank_leaders(lead_lag: pd.DataFrame) -> pd.Series:
    """Exploratory row-sum scores; NOT a statistical significance test."""
    return lead_lag.sum(axis=1).sort_values(ascending=False).rename("Leadership_Score")


def strongest_pairs(lead_lag: pd.DataFrame, forward: pd.DataFrame) -> pd.DataFrame:
    """Sort unordered pairs by absolute directional score, labelled as hypotheses."""
    tickers = list(lead_lag.index)
    pairs = []
    for i, first in enumerate(tickers):
        for second in tickers[i + 1:]:
            score = float(lead_lag.loc[first, second])
            leader, follower = (first, second) if score >= 0 else (second, first)
            pairs.append({
                "Candidate_Leader": leader,
                "Candidate_Follower": follower,
                "Score": abs(score),
                "Forward_Corr": float(forward.loc[leader, follower]),
                "Reverse_Corr": float(forward.loc[follower, leader]),
            })
    return pd.DataFrame(pairs).sort_values("Score", ascending=False).reset_index(drop=True)
