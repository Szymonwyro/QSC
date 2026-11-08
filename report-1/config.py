"""Settings for Quanta Student Capital's exploratory lead-lag pilot."""

# Provisional stock list. Replace after Rohan and Jesaiah agree the universe.
# Currently passing 'TICKERS' into main.py, so change to use the demo
TICKERS_Demo = [
    "AAPL", "MSFT", "NVDA", "AMD", "ORCL",  # Technology
    "CAT", "DE", "HON", "GE", "RTX",      # Industrials
]

TICKERS = [
    "AEP",
     # "AESI", leaving this one out as it start lates and causes a drop of 300 days
    "APA",
    "AR",
    "BKR",
    "BP",
    "BSM",
    "CCJ",
    "CEG",
    "CHRD",
    "CNX",
    "COP",
    "CRC",
    "CRGY",
    "CRK",
    "CVX",
    "D",
    "DINO",
    "DK",
    "DTM",
    "DUK",
    "DVN",
    "EOG",
    "EPD",
    "EQNR",
    "EQT",
    "ET",
    "EXE",
    "FANG",
    "HAL",
    "HP",
    "KMI",
    "LEU",
    "LNG",
    "MPC",
    "MTDR",
    "MUR",
    "NEE",
    "NRG",
    "OKE",
    "OXY",
    "PBF",
    "PR",
    "PSX",
    "PTEN"
]

# Yahoo Finance's end date is exclusive: this includes up to 2026-10-22.
START_DATE = "2022-01-01"
END_DATE = "2026-10-23"
