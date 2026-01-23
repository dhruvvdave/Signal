"""Data loader factory for multi-sport support."""

from __future__ import annotations

from services.nba.nba_data_loader import NBADataLoader
from services.nhl.nhl_data_loader import NHLDataLoader
from services.shared.base_data_loader import BaseDataLoader


class DataLoaderFactory:
    """Factory for creating sport-specific data loaders."""

    @staticmethod
    def create_loader(sport: str) -> BaseDataLoader:
        """Create a data loader for the specified sport.

        Args:
            sport: Sport name (e.g., "NBA", "NHL")

        Returns:
            Sport-specific data loader instance

        Raises:
            ValueError: If sport is not supported
        """
        if sport == "NBA":
            return NBADataLoader()
        elif sport == "NHL":
            return NHLDataLoader()
        else:
            raise ValueError(f"Unsupported sport: {sport}. Available sports: NBA, NHL")
