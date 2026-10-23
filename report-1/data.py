"""Download adjusted closes or generate controlled synthetic market data."""

from __future__ import annotations

import numpy as np
import pandas as pd


def download_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Download split/dividend-adjusted daily closing prices (internet required)."""
    import yfinance as yf

    raw = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=True,
        group_by="column",
        multi_level_index=True,
        threads=False,
        progress=False,
    )
    if raw.empty or "Close" not in raw.columns.get_level_values(0):
        raise RuntimeError("No adjusted closing prices returned. Check dates/internet/tickers.")

    prices = raw["Close"].reindex(columns=tickers)
    missing = prices.columns[prices.isna().all()].tolist()
    if missing:
        raise RuntimeError(f"No price history for these tickers: {missing}")

    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices.index.name = "Date"
    return prices


def simulated_prices(tickers: list[str], days: int = 850, seed: int = 2026) -> pd.DataFrame:
    """Synthetic demo: deliberately impose MSFT -> AMD next-session dependence.

    All price series are fictional, irrespective of their familiar ticker labels.
    """
    if "MSFT" not in tickers or "AMD" not in tickers:
        raise ValueError("Simulation requires MSFT and AMD in the ticker list.")

    rng = np.random.default_rng(seed)
    common_market = rng.normal(0, 0.006, days)
    tech = rng.normal(0, 0.004, days)
    industrial = rng.normal(0, 0.004, days)
    leader_shock = rng.normal(0, 0.012, days)

    log_r = {}
    for idx, ticker in enumerate(tickers):
        sector = tech if idx < 5 else industrial
        log_r[ticker] = (
            0.6 * common_market + 0.6 * sector + rng.normal(0, 0.01, days)
        )

    log_r["MSFT"] = 0.6 * common_market + 0.6 * tech + leader_shock
    lagged_shock = np.r_[0, leader_shock[:-1]]
    log_r["AMD"] = (
        0.6 * common_market + 0.6 * tech
        + 0.85 * lagged_shock + rng.normal(0, 0.008, days)
    )
    index = pd.bdate_range("2023-01-02", periods=days, name="Date")
    return 100 * np.exp(pd.DataFrame(log_r, index=index).cumsum())
