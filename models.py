"""Modeling logic for Signal Sports Analytics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from utils import clamp, compute_rolling_average, safe_mean


@dataclass
class FatigueInputs:
    rest_days: int
    is_home: bool
    minutes_last_game: float


def calculate_fatigue_score(inputs: FatigueInputs) -> float:
    """Compute a custom fatigue score (0-100).

    Higher score indicates higher fatigue.
    """
    rest_component = clamp(100 - (inputs.rest_days * 15), 0, 100)
    travel_component = 10 if not inputs.is_home else 0
    minutes_component = clamp((inputs.minutes_last_game / 48) * 40, 0, 40)
    raw_score = rest_component + travel_component + minutes_component
    return clamp(raw_score, 0, 100)


def build_similarity_model(stats: pd.DataFrame, feature_cols: list[str]) -> tuple[NearestNeighbors, StandardScaler]:
    """Fit a KNN model for player similarity."""
    scaler = StandardScaler()
    feature_matrix = scaler.fit_transform(stats[feature_cols].fillna(0))
    model = NearestNeighbors(n_neighbors=4, metric="euclidean")
    model.fit(feature_matrix)
    return model, scaler


def find_player_comps(
    stats: pd.DataFrame,
    player_name: str,
    feature_cols: list[str],
) -> pd.DataFrame:
    """Return the top 3 similar players for a given player."""
    if stats.empty or any(col not in stats.columns for col in feature_cols):
        return pd.DataFrame()
    model, scaler = build_similarity_model(stats, feature_cols)
    player_row = stats[stats["Player"] == player_name]
    if player_row.empty:
        return pd.DataFrame()

    player_vector = scaler.transform(player_row[feature_cols].fillna(0))
    distances, indices = model.kneighbors(player_vector, n_neighbors=4)
    comp_indices = indices[0][1:]
    comps = stats.iloc[comp_indices].copy()
    comps["SimilarityScore"] = 1 - (distances[0][1:] / max(distances[0][1:].max(), 1e-6))
    return comps


def build_prop_validator(game_log: pd.DataFrame, stat_col: str = "PTS") -> pd.DataFrame:
    """Compare rolling averages vs season averages for anomaly detection."""
    if game_log.empty or stat_col not in game_log.columns:
        return pd.DataFrame()

    if "GAME_DATE" in game_log.columns:
        sorted_games = game_log.sort_values("GAME_DATE")
    else:
        sorted_games = game_log.copy()
    sorted_games["Rolling_Avg"] = compute_rolling_average(sorted_games[stat_col], window=5)
    season_avg = safe_mean(sorted_games[stat_col])
    sorted_games["Season_Avg"] = season_avg

    sorted_games["Signal"] = np.where(
        sorted_games["Rolling_Avg"] > season_avg * 1.2,
        "Hot Streak",
        np.where(
            sorted_games["Rolling_Avg"] < season_avg * 0.8,
            "Cold Streak",
            "Neutral",
        ),
    )
    return sorted_games
