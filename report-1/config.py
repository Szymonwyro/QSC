"""Settings for Quanta Student Capital's exploratory lead-lag pilot."""

# Provisional stock list. Replace after Rohan and Jesaiah agree the universe.
TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMD", "ORCL",  # Technology
    "CAT", "DE", "HON", "GE", "RTX",      # Industrials
]

# Yahoo Finance's end date is exclusive: this includes up to 2026-10-22.
START_DATE = "2022-01-01"
END_DATE = "2026-10-23"
