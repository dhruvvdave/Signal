"""Data loading utilities for Signal Sports Analytics."""

from __future__ import annotations

from datetime import datetime
import importlib.util
from typing import Optional

import pandas as pd
import requests

NBA_API_AVAILABLE = importlib.util.find_spec("nba_api") is not None


def _load_nba_api_modules():
    """Lazily import nba_api modules when available."""
    if not NBA_API_AVAILABLE:
        return None
    from nba_api.stats.endpoints import leaguedashplayerstats, playergamelog, teamgamelog
    from nba_api.stats.static import players, teams

    return leaguedashplayerstats, playergamelog, teamgamelog, players, teams


DEFAULT_SEASON = "2023-24"
DEFAULT_SEASON_TYPE = "Regular Season"
NHL_BASE_URL = "https://statsapi.web.nhl.com/api/v1"


def get_player_id(player_name: str) -> Optional[int]:
    """Return the NBA player ID for a given full name.

    Args:
        player_name: Full player name (e.g., "Luka Doncic").

    Returns:
        The NBA player ID if found, otherwise None.
    """
    if not NBA_API_AVAILABLE:
        return None
    modules = _load_nba_api_modules()
    if modules is None:
        return None
    _, _, _, players, _ = modules
    matches = players.find_players_by_full_name(player_name)
    if not matches:
        return None
    return matches[0]["id"]


def get_team_id(team_name: str) -> Optional[int]:
    """Return the NBA team ID for a given full name."""
    if not NBA_API_AVAILABLE:
        return None
    modules = _load_nba_api_modules()
    if modules is None:
        return None
    _, _, _, _, teams = modules
    matches = [team for team in teams.get_teams() if team["full_name"] == team_name]
    if not matches:
        return None
    return matches[0]["id"]


def list_active_players() -> pd.DataFrame:
    """Return a DataFrame of active NBA players."""
    if not NBA_API_AVAILABLE:
        return pd.DataFrame()
    modules = _load_nba_api_modules()
    if modules is None:
        return pd.DataFrame()
    _, _, _, players, _ = modules
    try:
        data = players.get_active_players()
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame(data)


def list_active_teams() -> pd.DataFrame:
    """Return a DataFrame of NBA teams."""
    if not NBA_API_AVAILABLE:
        return pd.DataFrame()
    modules = _load_nba_api_modules()
    if modules is None:
        return pd.DataFrame()
    _, _, _, _, teams = modules
    try:
        data = teams.get_teams()
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame(data)


def load_player_game_log(
    player_id: int,
    season: str = DEFAULT_SEASON,
    season_type: str = DEFAULT_SEASON_TYPE,
) -> pd.DataFrame:
    """Fetch and clean a player's game log for a given season.

    Args:
        player_id: NBA API player ID.
        season: Season in "YYYY-YY" format (e.g., "2023-24").
        season_type: "Regular Season" or "Playoffs".

    Returns:
        Cleaned pandas DataFrame with parsed dates and numeric columns.
    """
    if not NBA_API_AVAILABLE:
        return pd.DataFrame()
    modules = _load_nba_api_modules()
    if modules is None:
        return pd.DataFrame()
    _, playergamelog, _, _, _ = modules
    try:
        response = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star=season_type,
        )
        data = response.get_data_frames()[0]
    except Exception:
        return pd.DataFrame()
    return _clean_game_log(data)


def load_team_game_log(
    team_id: int,
    season: str = DEFAULT_SEASON,
    season_type: str = DEFAULT_SEASON_TYPE,
) -> pd.DataFrame:
    """Fetch and clean a team's game log for a given season."""
    if not NBA_API_AVAILABLE:
        return pd.DataFrame()
    modules = _load_nba_api_modules()
    if modules is None:
        return pd.DataFrame()
    _, _, teamgamelog, _, _ = modules
    try:
        response = teamgamelog.TeamGameLog(
            team_id=team_id,
            season=season,
            season_type_all_star=season_type,
        )
        data = response.get_data_frames()[0]
    except Exception:
        return pd.DataFrame()
    return _clean_game_log(data)


def load_league_player_stats(
    season: str = DEFAULT_SEASON,
    season_type: str = DEFAULT_SEASON_TYPE,
) -> pd.DataFrame:
    """Load league-wide player stats for similarity comparisons."""
    if not NBA_API_AVAILABLE:
        return pd.DataFrame()
    modules = _load_nba_api_modules()
    if modules is None:
        return pd.DataFrame()
    leaguedashplayerstats, _, _, _, _ = modules
    try:
        response = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star=season_type,
            per_mode_detailed="PerGame",
        )
        data = response.get_data_frames()[0]
    except Exception:
        return pd.DataFrame()
    return _clean_league_stats(data, season=season)


def _clean_game_log(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize game log fields for downstream analytics."""
    cleaned = data.copy()
    if "GAME_DATE" in cleaned.columns:
        cleaned["GAME_DATE"] = pd.to_datetime(
            cleaned["GAME_DATE"],
            format="%Y-%m-%d",
            errors="coerce",
        )

    numeric_cols = [
        "PTS",
        "AST",
        "REB",
        "MIN",
        "FGM",
        "FGA",
        "FG3M",
        "FG3A",
        "FTM",
        "FTA",
        "PLUS_MINUS",
    ]
    for col in numeric_cols:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    if "MATCHUP" in cleaned.columns:
        cleaned["IS_HOME"] = cleaned["MATCHUP"].str.contains("vs.", na=False)

    return cleaned


def _clean_league_stats(data: pd.DataFrame, season: str) -> pd.DataFrame:
    """Clean league stats and normalize column naming."""
    cleaned = data.copy()
    rename_map = {
        "PLAYER_NAME": "Player",
        "TEAM_ABBREVIATION": "Team",
        "PTS": "Points",
        "AST": "Assists",
        "REB": "Rebounds",
        "USG_PCT": "UsageRate",
        "TS_PCT": "TrueShootingPct",
    }
    cleaned = cleaned.rename(columns=rename_map)

    metric_cols = ["Points", "Assists", "Rebounds", "UsageRate", "TrueShootingPct"]
    for col in metric_cols:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        else:
            cleaned[col] = 0.0

    cleaned["Season"] = season
    cleaned["LastUpdated"] = datetime.utcnow()
    return cleaned


def load_nhl_standings() -> pd.DataFrame:
    """Fetch NHL standings from the public Stats API."""
    try:
        response = requests.get(f"{NHL_BASE_URL}/standings", timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return pd.DataFrame()

    data = response.json()
    records = []
    for record in data.get("records", []):
        for team_record in record.get("teamRecords", []):
            team = team_record.get("team", {})
            records.append(
                {
                    "Division": record.get("division", {}).get("name"),
                    "Conference": record.get("conference", {}).get("name"),
                    "Team": team.get("name"),
                    "Games": team_record.get("gamesPlayed"),
                    "Wins": team_record.get("leagueRecord", {}).get("wins"),
                    "Losses": team_record.get("leagueRecord", {}).get("losses"),
                    "OT": team_record.get("leagueRecord", {}).get("ot"),
                    "Points": team_record.get("points"),
                    "GoalDiff": team_record.get("goalsScored", 0)
                    - team_record.get("goalsAgainst", 0),
                    "Streak": team_record.get("streak", {}).get("streakCode"),
                }
            )
    return pd.DataFrame(records)


def load_nhl_team_stats() -> pd.DataFrame:
    """Fetch NHL team stats from the public Stats API."""
    try:
        response = requests.get(f"{NHL_BASE_URL}/teams?expand=team.stats", timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return pd.DataFrame()

    data = response.json()
    records = []
    for team in data.get("teams", []):
        splits = team.get("teamStats", [])[0].get("splits", [])
        if not splits:
            continue
        stats = splits[0].get("stat", {})
        records.append(
            {
                "Team": team.get("name"),
                "Games": stats.get("gamesPlayed"),
                "GoalsPerGame": stats.get("goalsPerGame"),
                "GoalsAgainstPerGame": stats.get("goalsAgainstPerGame"),
                "ShotsPerGame": stats.get("shotsPerGame"),
                "ShotsAllowedPerGame": stats.get("shotsAllowed"),
                "PowerPlayPct": stats.get("powerPlayPercentage"),
                "PenaltyKillPct": stats.get("penaltyKillPercentage"),
            }
        )
    return pd.DataFrame(records)
