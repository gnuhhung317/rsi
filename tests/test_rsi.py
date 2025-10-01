from math import isclose
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import _compute_rsi


def assert_sequence_close(result, expected):
    assert len(result) == len(expected)
    for actual, target in zip(result, expected):
        if target != target:  # NaN check
            assert actual != actual
        else:
            assert isclose(actual, target, rel_tol=1e-9, abs_tol=1e-9)


def test_insufficient_history_returns_nan():
    prices = [100, 101, 102]
    rsi = _compute_rsi(prices, lookback=5)
    assert all(value != value for value in rsi)


def test_all_gains_returns_hundred_after_window():
    prices = [1, 2, 3, 4, 5]
    rsi = _compute_rsi(prices, lookback=2)
    expected = [float("nan"), float("nan"), 100.0, 100.0, 100.0]
    assert_sequence_close(rsi, expected)


def test_all_losses_returns_zero_after_window():
    prices = [5, 4, 3, 2, 1]
    rsi = _compute_rsi(prices, lookback=2)
    expected = [float("nan"), float("nan"), 0.0, 0.0, 0.0]
    assert_sequence_close(rsi, expected)


def test_flat_series_returns_fifty_after_window():
    prices = [5, 5, 5, 5, 5]
    rsi = _compute_rsi(prices, lookback=2)
    expected = [float("nan"), float("nan"), 50.0, 50.0, 50.0]
    assert_sequence_close(rsi, expected)


def test_short_series_returns_expected_values():
    prices = [10, 11, 12, 11, 12]
    rsi = _compute_rsi(prices, lookback=2)
    expected = [float("nan"), float("nan"), 100.0, 50.0, 75.0]
    assert_sequence_close(rsi, expected)
