"""NHL data loading service using nhl-api-py."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd

from services.shared.base_data_loader import BaseDataLoader


class NHLDataLoader(BaseDataLoader):
    """NHL-specific data loader implementation."""

    DEFAULT_SEASON = "20232024"  # NHL uses concatenated format
    DEFAULT_SEASON_TYPE = "Regular Season"

    def __init__(self):
        """Initialize NHL data loader."""
        # We'll use a simple approach with NHL's public API endpoints
        self.base_url = "https://api-web.nhle.com/v1"
        self.teams_cache = None
        self.players_cache = None

    def list_active_players(self) -> pd.DataFrame:
        """Return a DataFrame of active NHL players.
        
        Note: NHL API doesn't have a simple "all active players" endpoint.
        Full player roster aggregation pending API implementation.
        """
        try:
            if self.players_cache is not None:
                return self.players_cache

            # Initialize with empty DataFrame with proper structure
            # TODO: Aggregate from team rosters when NHL API is fully integrated
            self.players_cache = pd.DataFrame(columns=["id", "full_name", "team"])
            return self.players_cache
        except Exception:
            return pd.DataFrame(columns=["id", "full_name", "team"])

    def list_active_teams(self) -> pd.DataFrame:
        """Return a DataFrame of NHL teams."""
        try:
            if self.teams_cache is not None:
                return self.teams_cache

            # Current NHL teams for 2023-24 season (32 teams)
            teams_data = [
                {"id": 1, "full_name": "New Jersey Devils", "abbreviation": "NJD"},
                {"id": 2, "full_name": "New York Islanders", "abbreviation": "NYI"},
                {"id": 3, "full_name": "New York Rangers", "abbreviation": "NYR"},
                {"id": 4, "full_name": "Philadelphia Flyers", "abbreviation": "PHI"},
                {"id": 5, "full_name": "Pittsburgh Penguins", "abbreviation": "PIT"},
                {"id": 6, "full_name": "Boston Bruins", "abbreviation": "BOS"},
                {"id": 7, "full_name": "Buffalo Sabres", "abbreviation": "BUF"},
                {"id": 8, "full_name": "Montréal Canadiens", "abbreviation": "MTL"},
                {"id": 9, "full_name": "Ottawa Senators", "abbreviation": "OTT"},
                {"id": 10, "full_name": "Toronto Maple Leafs", "abbreviation": "TOR"},
                {"id": 12, "full_name": "Carolina Hurricanes", "abbreviation": "CAR"},
                {"id": 13, "full_name": "Florida Panthers", "abbreviation": "FLA"},
                {"id": 14, "full_name": "Tampa Bay Lightning", "abbreviation": "TBL"},
                {"id": 15, "full_name": "Washington Capitals", "abbreviation": "WSH"},
                {"id": 16, "full_name": "Chicago Blackhawks", "abbreviation": "CHI"},
                {"id": 17, "full_name": "Detroit Red Wings", "abbreviation": "DET"},
                {"id": 18, "full_name": "Nashville Predators", "abbreviation": "NSH"},
                {"id": 19, "full_name": "St. Louis Blues", "abbreviation": "STL"},
                {"id": 20, "full_name": "Calgary Flames", "abbreviation": "CGY"},
                {"id": 21, "full_name": "Colorado Avalanche", "abbreviation": "COL"},
                {"id": 22, "full_name": "Edmonton Oilers", "abbreviation": "EDM"},
                {"id": 23, "full_name": "Vancouver Canucks", "abbreviation": "VAN"},
                {"id": 24, "full_name": "Anaheim Ducks", "abbreviation": "ANA"},
                {"id": 25, "full_name": "Dallas Stars", "abbreviation": "DAL"},
                {"id": 26, "full_name": "Los Angeles Kings", "abbreviation": "LAK"},
                {"id": 28, "full_name": "San Jose Sharks", "abbreviation": "SJS"},
                {"id": 29, "full_name": "Columbus Blue Jackets", "abbreviation": "CBJ"},
                {"id": 30, "full_name": "Minnesota Wild", "abbreviation": "MIN"},
                {"id": 52, "full_name": "Winnipeg Jets", "abbreviation": "WPG"},
                {"id": 53, "full_name": "Utah Hockey Club", "abbreviation": "UTA"},
                {"id": 54, "full_name": "Vegas Golden Knights", "abbreviation": "VGK"},
                {"id": 55, "full_name": "Seattle Kraken", "abbreviation": "SEA"},
            ]

            self.teams_cache = pd.DataFrame(teams_data)
            return self.teams_cache
        except Exception:
            return pd.DataFrame()

    def get_player_id(self, player_name: str) -> Optional[int]:
        """Return the NHL player ID for a given full name."""
        # This would require a player search API
        # For now, return None to indicate not found
        return None

    def get_team_id(self, team_name: str) -> Optional[int]:
        """Return the NHL team ID for a given full name."""
        teams_df = self.list_active_teams()
        if teams_df.empty:
            return None
        matches = teams_df[teams_df["full_name"] == team_name]
        if matches.empty:
            return None
        return int(matches.iloc[0]["id"])

    def load_player_game_log(
        self,
        player_id: int,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Fetch and clean a player's game log for a given season.
        
        Note: Full NHL API integration pending. This method returns empty DataFrame
        until NHL API endpoints are properly configured.
        """
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        # TODO: Implement NHL API call when endpoints are finalized
        # Placeholder for future implementation
        return pd.DataFrame()

    def load_team_game_log(
        self,
        team_id: int,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Fetch and clean a team's game log for a given season.
        
        Note: Full NHL API integration pending. This method returns empty DataFrame
        until NHL API endpoints are properly configured.
        """
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        # TODO: Implement NHL API call when endpoints are finalized
        # Placeholder for future implementation
        return pd.DataFrame()

    def load_league_player_stats(
        self,
        season: str = None,
        season_type: str = None,
    ) -> pd.DataFrame:
        """Load league-wide player stats for similarity comparisons.
        
        Note: Full NHL API integration pending. This method returns empty DataFrame
        until NHL API endpoints are properly configured.
        """
        if season is None:
            season = self.DEFAULT_SEASON
        if season_type is None:
            season_type = self.DEFAULT_SEASON_TYPE

        # TODO: Implement NHL API call when endpoints are finalized
        # Placeholder for future implementation
        return pd.DataFrame()

    def get_stat_columns(self) -> dict[str, list[str]]:
        """Return NHL-specific stat column mappings."""
        return {
            "skater_basic": ["goals", "assists", "points", "plusMinus", "shots"],
            "skater_advanced": ["timeOnIce", "faceoffPct", "hits", "blocks"],
            "goalie_basic": ["saves", "savePct", "goalsAgainstAvg", "shutouts"],
            "goalie_advanced": ["qualityStarts", "goalsAgainst", "shotsAgainst"],
            "display_names": {
                "goals": "Goals",
                "assists": "Assists",
                "points": "Points",
                "plusMinus": "+/-",
                "shots": "Shots",
                "timeOnIce": "TOI",
                "savePct": "SV%",
                "goalsAgainstAvg": "GAA",
            },
        }

    def _clean_game_log(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize game log fields for downstream analytics."""
        cleaned = data.copy()

        # Convert game date if present
        if "gameDate" in cleaned.columns:
            cleaned["GAME_DATE"] = pd.to_datetime(
                cleaned["gameDate"],
                errors="coerce",
            )

        # Standardize numeric columns
        numeric_cols = ["goals", "assists", "points", "shots", "plusMinus", "timeOnIce"]
        for col in numeric_cols:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

        return cleaned
