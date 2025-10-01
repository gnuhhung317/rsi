"""RSI computation utilities."""
from __future__ import annotations

from math import isclose, nan
from typing import Iterable, List

try:  # pragma: no cover - optional dependency
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover - executed when pandas missing
    pd = None  # type: ignore[assignment]


def _resolve_rsi_value(avg_gain: float, avg_loss: float) -> float:
    """Return the RSI value for the supplied average gain/loss pair."""

    if isclose(avg_gain, 0.0) and isclose(avg_loss, 0.0):
        return 50.0
    if isclose(avg_loss, 0.0):
        return 100.0
    if isclose(avg_gain, 0.0):
        return 0.0

    relative_strength = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + relative_strength))


def _wrap_result(values: List[float], original: Iterable[float]):
    """Wrap a result list into a Series when pandas is available."""

    if pd is None:
        return values

    if isinstance(original, pd.Series):
        return pd.Series(values, index=original.index, dtype="float64")

    return pd.Series(values, dtype="float64")


def _compute_rsi(prices: Iterable[float], lookback: int = 14):
    """Compute the Relative Strength Index for a price sequence.

    Parameters
    ----------
    prices
        Iterable of price values ordered chronologically.
    lookback
        Number of periods used for the Wilder exponential moving average.

    Returns
    -------
    Sequence of floats (or ``pandas.Series`` when pandas is installed)
        RSI values with the same length as the input sequence. Entries before a
        full lookback window are ``NaN``.
    """

    if lookback <= 0:
        raise ValueError("lookback must be a positive integer")

    prices_list = [float(price) for price in prices]
    count = len(prices_list)

    if count == 0:
        return _wrap_result([], prices)

    rsi_values: List[float] = [nan] * count

    if count <= lookback:
        return _wrap_result(rsi_values, prices)

    gains = [0.0] * count
    losses = [0.0] * count

    for idx in range(1, count):
        change = prices_list[idx] - prices_list[idx - 1]
        if change > 0:
            gains[idx] = change
        else:
            losses[idx] = -change

    avg_gain = sum(gains[1 : lookback + 1]) / lookback
    avg_loss = sum(losses[1 : lookback + 1]) / lookback
    rsi_values[lookback] = _resolve_rsi_value(avg_gain, avg_loss)

    for idx in range(lookback + 1, count):
        avg_gain = ((avg_gain * (lookback - 1)) + gains[idx]) / lookback
        avg_loss = ((avg_loss * (lookback - 1)) + losses[idx]) / lookback
        rsi_values[idx] = _resolve_rsi_value(avg_gain, avg_loss)

    return _wrap_result(rsi_values, prices)


__all__ = ["_compute_rsi"]
