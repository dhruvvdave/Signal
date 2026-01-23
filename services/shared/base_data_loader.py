"""Base data loader interface for multi-sport support."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class BaseDataLoader(ABC):
    """Abstract base class for sport-specific data loaders."""

    @abstractmethod
    def list_active_players(self) -> pd.DataFrame:
        """Return a DataFrame of active players."""
        pass

    @abstractmethod
    def list_active_teams(self) -> pd.DataFrame:
        """Return a DataFrame of teams."""
        pass

    @abstractmethod
    def get_player_id(self, player_name: str) -> Optional[int]:
        """Return the player ID for a given full name."""
        pass

    @abstractmethod
    def get_team_id(self, team_name: str) -> Optional[int]:
        """Return the team ID for a given full name."""
        pass

    @abstractmethod
    def load_player_game_log(
        self,
        player_id: int,
        season: str,
        season_type: str = "Regular Season",
    ) -> pd.DataFrame:
        """Fetch and clean a player's game log for a given season."""
        pass

    @abstractmethod
    def load_team_game_log(
        self,
        team_id: int,
        season: str,
        season_type: str = "Regular Season",
    ) -> pd.DataFrame:
        """Fetch and clean a team's game log for a given season."""
        pass

    @abstractmethod
    def load_league_player_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
    ) -> pd.DataFrame:
        """Load league-wide player stats for similarity comparisons."""
        pass

    @abstractmethod
    def get_stat_columns(self) -> dict[str, list[str]]:
        """Return sport-specific stat column mappings."""
        pass
