"""NBA data loading service."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, playergamelog, teamgamelog
from nba_api.stats.static import players, teams

from services.shared.base_data_loader import BaseDataLoader


class NBADataLoader(BaseDataLoader):
    """NBA-specific data loader implementation."""

    DEFAULT_SEASON = "2023-24"
    DEFAULT_SEASON_TYPE = "Regular Season"

    def list_active_players(self) -> pd.DataFrame:
        """Return a DataFrame of active NBA players."""
        try:
            data = players.get_active_players()
        except Exception:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def list_active_teams(self) -> pd.DataFrame:
        """Return a DataFrame of NBA teams."""
        try:
            data = teams.get_teams()
        except Exception:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def get_player_id(self, player_name: str) -> Optional[int]:
        """Return the NBA player ID for a given full name."""
        matches = players.find_players_by_full_name(player_name)
        if not matches:
            return None
        return matches[0]["id"]

    def get_team_id(self, team_name: str) -> Optional[int]:
        """Return the NBA team ID for a given full name."""
        matches = [team for team in teams.get_teams() if team["full_name"] == team_name]
        if not matches:
            return None
        return matches[0]["id"]

    def load_player_game_log(
        self,
        player_id: int,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Fetch and clean a player's game log for a given season."""
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        try:
            response = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star=season_type,
            )
            data = response.get_data_frames()[0]
        except Exception:
            return pd.DataFrame()
        return self._clean_game_log(data)

    def load_team_game_log(
        self,
        team_id: int,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Fetch and clean a team's game log for a given season."""
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        try:
            response = teamgamelog.TeamGameLog(
                team_id=team_id,
                season=season,
                season_type_all_star=season_type,
            )
            data = response.get_data_frames()[0]
        except Exception:
            return pd.DataFrame()
        return self._clean_game_log(data)

    def load_league_player_stats(
        self,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Load league-wide player stats for similarity comparisons."""
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        try:
            response = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                season_type_all_star=season_type,
                per_mode_detailed="PerGame",
            )
            data = response.get_data_frames()[0]
        except Exception:
            return pd.DataFrame()
        return self._clean_league_stats(data, season=season)

    def get_stat_columns(self) -> dict[str, list[str]]:
        """Return NBA-specific stat column mappings."""
        return {
            "basic": ["PTS", "AST", "REB", "MIN"],
            "shooting": ["FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT"],
            "advanced": ["Points", "Assists", "Rebounds", "UsageRate", "TrueShootingPct"],
            "display_names": {
                "PTS": "Points",
                "AST": "Assists",
                "REB": "Rebounds",
                "MIN": "Minutes",
            },
        }

    def _clean_game_log(self, data: pd.DataFrame) -> pd.DataFrame:
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

    def _clean_league_stats(self, data: pd.DataFrame, season: str) -> pd.DataFrame:
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
