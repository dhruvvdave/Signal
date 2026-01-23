"""Utility helpers for Signal Sports Analytics."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import numpy as np
import pandas as pd


def format_season_label(season: str) -> str:
    """Return a friendly season label."""
    return season.replace("-", "–")


def ensure_datetime(series: pd.Series) -> pd.Series:
    """Safely coerce a series into datetime values."""
    return pd.to_datetime(series, errors="coerce")


def compute_rolling_average(series: pd.Series, window: int = 5) -> pd.Series:
    """Compute a rolling average with a minimum of one observation."""
    return series.rolling(window=window, min_periods=1).mean()


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    """Clamp a numeric value between a lower and upper bound."""
    return float(max(lower, min(value, upper)))


def safe_mean(values: Iterable[float]) -> float:
    """Return the mean of values, falling back to 0.0 when empty."""
    values = list(values)
    if not values:
        return 0.0
    return float(np.nanmean(values))


def days_since(date_value: datetime) -> int:
    """Compute days since a provided datetime value."""
    if pd.isna(date_value):
        return 0
    delta = datetime.utcnow().date() - date_value.date()
    return max(delta.days, 0)
