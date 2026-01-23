"""Enhanced visualization components for Signal Sports Analytics."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_performance_trend_chart(
    data: pd.DataFrame,
    stat_col: str,
    player_name: str,
    sport: str = "NBA",
    show_rolling_avg: bool = True,
) -> go.Figure:
    """Create an enhanced performance trend chart with rolling averages.

    Args:
        data: Game log DataFrame
        stat_col: Statistic column to plot (e.g., "PTS", "goals")
        player_name: Player name for title
        sport: Sport name for theming
        show_rolling_avg: Whether to show rolling average line

    Returns:
        Plotly figure object
    """
    if data.empty or stat_col not in data.columns:
        return go.Figure()

    # Sort by date
    plot_data = data.sort_values("GAME_DATE").tail(20).copy()

    # Calculate rolling average
    if show_rolling_avg:
        plot_data["Rolling_5"] = plot_data[stat_col].rolling(window=5, min_periods=1).mean()
        plot_data["Rolling_10"] = plot_data[stat_col].rolling(window=10, min_periods=1).mean()

    # Create figure
    fig = go.Figure()

    # Add actual performance
    fig.add_trace(
        go.Scatter(
            x=plot_data["GAME_DATE"],
            y=plot_data[stat_col],
            mode="lines+markers",
            name="Actual",
            line=dict(color="#00FFAA", width=2),
            marker=dict(size=8, color="#00FFAA"),
            hovertemplate="<b>%{x|%b %d}</b><br>" + f"{stat_col}: %{{y:.1f}}<extra></extra>",
        )
    )

    # Add rolling averages
    if show_rolling_avg:
        fig.add_trace(
            go.Scatter(
                x=plot_data["GAME_DATE"],
                y=plot_data["Rolling_5"],
                mode="lines",
                name="5-Game Avg",
                line=dict(color="#FFD166", width=2, dash="dash"),
                hovertemplate="<b>%{x|%b %d}</b><br>5-Game Avg: %{y:.1f}<extra></extra>",
            )
        )

    # Calculate season average
    season_avg = plot_data[stat_col].mean()
    fig.add_hline(
        y=season_avg,
        line_dash="dot",
        line_color="#FF4B4B",
        annotation_text=f"Season Avg: {season_avg:.1f}",
        annotation_position="right",
    )

    # Update layout
    fig.update_layout(
        title=f"{player_name} - {stat_col} Trend (Last 20 Games)",
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        hovermode="x unified",
        xaxis=dict(
            title="Game Date",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            title=stat_col,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig


def create_distribution_chart(
    data: pd.DataFrame,
    stat_col: str,
    player_name: str,
    sport: str = "NBA",
) -> go.Figure:
    """Create a distribution/histogram chart for a stat.

    Args:
        data: Game log DataFrame
        stat_col: Statistic column to plot
        player_name: Player name for title
        sport: Sport name for theming

    Returns:
        Plotly figure object
    """
    if data.empty or stat_col not in data.columns:
        return go.Figure()

    values = data[stat_col].dropna()
    if values.empty:
        return go.Figure()

    # Create histogram
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=values,
            nbinsx=15,
            name=stat_col,
            marker=dict(
                color="#00FFAA",
                line=dict(color="#FFFFFF", width=1),
            ),
            hovertemplate="%{x} " + stat_col + "<br>Count: %{y}<extra></extra>",
        )
    )

    # Add mean line
    mean_val = values.mean()
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#FFD166",
        annotation_text=f"Mean: {mean_val:.1f}",
        annotation_position="top",
    )

    # Add median line
    median_val = values.median()
    fig.add_vline(
        x=median_val,
        line_dash="dot",
        line_color="#FF4B4B",
        annotation_text=f"Median: {median_val:.1f}",
        annotation_position="bottom",
    )

    fig.update_layout(
        title=f"{player_name} - {stat_col} Distribution",
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis=dict(title=stat_col),
        yaxis=dict(title="Frequency"),
        showlegend=False,
    )

    return fig


def create_multi_stat_comparison(
    data: pd.DataFrame,
    stat_cols: list[str],
    player_name: str,
    sport: str = "NBA",
) -> go.Figure:
    """Create a multi-stat comparison chart.

    Args:
        data: Game log DataFrame
        stat_cols: List of statistic columns to compare
        player_name: Player name for title
        sport: Sport name for theming

    Returns:
        Plotly figure object with subplots
    """
    if data.empty:
        return go.Figure()

    # Filter available columns
    available_cols = [col for col in stat_cols if col in data.columns]
    if not available_cols:
        return go.Figure()

    plot_data = data.sort_values("GAME_DATE").tail(15).copy()

    # Create subplots
    rows = (len(available_cols) + 1) // 2
    fig = make_subplots(
        rows=rows,
        cols=2,
        subplot_titles=[col for col in available_cols],
        vertical_spacing=0.12,
        horizontal_spacing=0.1,
    )

    colors = ["#00FFAA", "#FFD166", "#FF4B4B", "#1D428A", "#C8102E"]

    for idx, col in enumerate(available_cols):
        row = (idx // 2) + 1
        col_pos = (idx % 2) + 1

        fig.add_trace(
            go.Scatter(
                x=plot_data["GAME_DATE"],
                y=plot_data[col],
                mode="lines+markers",
                name=col,
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=6),
                showlegend=False,
            ),
            row=row,
            col=col_pos,
        )

    fig.update_layout(
        title=f"{player_name} - Multi-Stat Trends (Last 15 Games)",
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400 * rows,
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")

    return fig


def create_home_away_comparison(
    data: pd.DataFrame,
    stat_cols: list[str],
    player_name: str,
    sport: str = "NBA",
) -> go.Figure:
    """Create a home vs away performance comparison chart.

    Args:
        data: Game log DataFrame with IS_HOME column
        stat_cols: List of statistic columns to compare
        player_name: Player name for title
        sport: Sport name for theming

    Returns:
        Plotly figure object
    """
    if data.empty or "IS_HOME" not in data.columns:
        return go.Figure()

    # Filter available columns
    available_cols = [col for col in stat_cols if col in data.columns]
    if not available_cols:
        return go.Figure()

    # Calculate averages
    home_data = data[data["IS_HOME"] == True]
    away_data = data[data["IS_HOME"] == False]

    home_avgs = [home_data[col].mean() if not home_data.empty else 0 for col in available_cols]
    away_avgs = [away_data[col].mean() if not away_data.empty else 0 for col in available_cols]

    # Create grouped bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=available_cols,
            y=home_avgs,
            name="Home",
            marker=dict(color="#00FFAA"),
            text=[f"{v:.1f}" for v in home_avgs],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            x=available_cols,
            y=away_avgs,
            name="Away",
            marker=dict(color="#FF4B4B"),
            text=[f"{v:.1f}" for v in away_avgs],
            textposition="outside",
        )
    )

    fig.update_layout(
        title=f"{player_name} - Home vs Away Performance",
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        barmode="group",
        xaxis=dict(title="Stat"),
        yaxis=dict(title="Average"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig


def create_enhanced_radar_chart(
    player_data: pd.Series,
    league_avg: pd.Series,
    stat_cols: list[str],
    player_name: str,
    sport: str = "NBA",
) -> go.Figure:
    """Create an enhanced radar chart comparing player to league average.

    Args:
        player_data: Player statistics Series
        league_avg: League average statistics Series
        stat_cols: List of statistic columns
        player_name: Player name for title
        sport: Sport name for theming

    Returns:
        Plotly figure object
    """
    if player_data.empty or league_avg.empty:
        return go.Figure()

    # Normalize values to 0-100 scale for better visualization
    max_vals = league_avg * 2  # Use 2x league average as max
    player_normalized = ((player_data / max_vals) * 100).clip(0, 100)
    league_normalized = ((league_avg / max_vals) * 100).clip(0, 100)

    fig = go.Figure()

    # Player trace
    fig.add_trace(
        go.Scatterpolar(
            r=player_normalized.values,
            theta=stat_cols,
            fill="toself",
            name=player_name,
            line=dict(color="#00FFAA", width=2),
            fillcolor="rgba(0, 255, 170, 0.3)",
        )
    )

    # League average trace
    fig.add_trace(
        go.Scatterpolar(
            r=league_normalized.values,
            theta=stat_cols,
            fill="toself",
            name="League Avg",
            line=dict(color="#FF4B4B", width=2),
            fillcolor="rgba(255, 75, 75, 0.2)",
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor="rgba(255,255,255,0.2)",
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.2)",
            ),
        ),
        showlegend=True,
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        height=450,
        title=f"{player_name} vs League Average",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig
