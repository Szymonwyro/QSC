
"""Unit tests to detect date-alignment and score-sign mistakes."""

import unittest

import numpy as np
import pandas as pd

from analysis import calculate_returns, calculate_matrices
from config import TICKERS
from data import simulated_prices


class TestLeadLag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prices = simulated_prices(TICKERS)
        cls.returns = calculate_returns(prices)
        cls.same_day, cls.forward, cls.scores = calculate_matrices(cls.returns)

    def test_expected_delayed_relationship(self):
        self.assertGreater(self.scores.loc["MSFT", "AMD"], 0.4)

    def test_score_antisymmetry(self):
        np.testing.assert_allclose(self.scores.to_numpy(), -self.scores.to_numpy().T, atol=1e-12)

    def test_diagonal_is_zero(self):
        np.testing.assert_allclose(np.diag(self.scores), 0, atol=1e-12)

    def test_log_returns_are_correct(self):
        prices = pd.DataFrame({"A": [100.0, 110.0], "B": [200.0, 220.0]})
        returns = calculate_returns(prices)
        self.assertAlmostEqual(returns.loc[1, "A"], np.log(1.1), places=12)

    def test_next_session_not_same_session(self):
        # This verifies a known perfect one-day delayed link on an independent dataset.
        rng = np.random.default_rng(12)
        leader = rng.normal(size=400) * 0.01
        follower = np.r_[0, leader[:-1]]
        prices = 100 * np.exp(pd.DataFrame({"L": leader, "F": follower}).cumsum())
        _, _, scores = calculate_matrices(calculate_returns(prices))
        self.assertGreater(scores.loc["L", "F"], 0.8)


if __name__ == "__main__":
    unittest.main()
