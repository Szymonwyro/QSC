"""Run the Quanta Student Capital stock lead-lag pilot.

    python main.py --demo     # Runs offline; explicitly fictional stocks
    python main.py            # Downloads real adjusted closes (internet needed)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from analysis import calculate_returns, calculate_matrices, rank_leaders, strongest_pairs
from config import TICKERS, START_DATE, END_DATE
from data import download_prices, simulated_prices
from plots import save_heatmap, save_ranking


def main() -> None:
    parser = argparse.ArgumentParser(description="Quanta lead-lag stock pilot")
    parser.add_argument("--demo", action="store_true", help="Use synthetic offline dataset")
    args = parser.parse_args()

    mode = "demo" if args.demo else "market"
    out = Path(__file__).resolve().parent / "results" / mode
    out.mkdir(parents=True, exist_ok=True)

    if args.demo:
        prices = simulated_prices(TICKERS)
    else:
        prices = download_prices(TICKERS, START_DATE, END_DATE)

    returns = calculate_returns(prices)
    same_day, forward, lead_lag = calculate_matrices(returns)
    leaders = rank_leaders(lead_lag)
    pairs = strongest_pairs(lead_lag, forward)

    # Save reproducible tabular outputs.
    prices.to_csv(out / "prices.csv")
    returns.to_csv(out / "log_returns.csv")
    same_day.to_csv(out / "same_day_correlations.csv")
    forward.to_csv(out / "forward_correlations.csv")
    lead_lag.to_csv(out / "lead_lag_scores.csv")
    leaders.to_csv(out / "leadership_rankings.csv", header=True)
    pairs.to_csv(out / "strongest_pairs.csv", index=False)

    # Save three charts for Sunday's meeting.
    save_heatmap(same_day, "Same-day correlations of stock returns", out / "01_correlations.png")
    save_heatmap(lead_lag, "Next-day directional lead-lag score", out / "02_lead_lag.png")
    save_ranking(leaders, out / "03_leadership_rankings.png")

    print(f"\nMode: {mode.upper()}; tickers: {len(TICKERS)}; price observations: {len(prices)}")
    print("\nCandidate strongest directional pairs (exploratory only):")
    print(pairs.head(5).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if args.demo:
        print("\nSIMULATED EXAMPLE: MSFT -> AMD was deliberately programmed; no real claim.")
        print(f"Observed MSFT -> AMD directional score: {lead_lag.loc['MSFT', 'AMD']:.3f}")
    print(f"\nCharts and CSVs saved in: {out.resolve()}")


if __name__ == "__main__":
    main()
