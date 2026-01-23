"""Configuration for multi-sport analytics."""

from __future__ import annotations


class SportConfig:
    """Configuration for different sports."""

    NBA = {
        "name": "NBA",
        "display_name": "NBA Basketball",
        "seasons": ["2023-24", "2022-23", "2021-22"],
        "season_format": "YYYY-YY",
        "primary_color": "#1D428A",  # NBA Blue
        "accent_color": "#00FFAA",  # Teal
        "metrics": {
            "primary": ["Points", "Assists", "Rebounds", "Minutes"],
            "shooting": ["FG%", "3P%", "FT%"],
            "advanced": ["PER", "TS%", "USG%", "VORP"],
        },
    }

    NHL = {
        "name": "NHL",
        "display_name": "NHL Hockey",
        "seasons": ["2023-24", "2022-23", "2021-22"],
        "season_format": "YYYY-YY",
        "primary_color": "#C8102E",  # NHL Red
        "accent_color": "#FFFFFF",  # White
        "metrics": {
            "skater_primary": ["Goals", "Assists", "Points", "+/-"],
            "skater_advanced": ["TOI", "Shots", "Hits", "Blocks"],
            "goalie_primary": ["SV%", "GAA", "Saves", "Shutouts"],
            "goalie_advanced": ["Quality Starts", "High Danger Saves"],
        },
    }

    @classmethod
    def get_sport_config(cls, sport: str) -> dict:
        """Get configuration for a specific sport."""
        if sport == "NBA":
            return cls.NBA
        elif sport == "NHL":
            return cls.NHL
        else:
            raise ValueError(f"Unknown sport: {sport}")

    @classmethod
    def get_available_sports(cls) -> list[str]:
        """Get list of available sports."""
        return ["NBA", "NHL"]
