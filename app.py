"""Streamlit app entry point for Signal Sports Analytics."""

from __future__ import annotations

import importlib.util

import pandas as pd
import streamlit as st

import data_loader
import models
from config.sport_config import SportConfig
from services.shared.data_loader_factory import DataLoaderFactory
from styles.glassmorphism import get_glassmorphism_css
from utils import format_season_label, safe_mean


st.set_page_config(
    page_title="Signal Sports Analytics",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


def require_dependency(module_name: str, install_hint: str) -> None:
    """Ensure a dependency is available before importing it."""
    if importlib.util.find_spec(module_name) is None:
        st.error(f"Missing dependency: `{module_name}`. {install_hint}")
        st.stop()


require_dependency("plotly", "Install it with `pip install plotly` and restart the app.")
import plotly.express as px
import plotly.graph_objects as go


# Initialize session state for sport selection
if "sport" not in st.session_state:
    st.session_state.sport = "NBA"


@st.cache_data(ttl=3600)
def load_active_players(sport: str) -> pd.DataFrame:
    """Load active players for the specified sport."""
    if sport == "NBA":
        return data_loader.list_active_players()
    else:
        # For NHL and other sports, use the data loader factory
        loader = DataLoaderFactory.create_loader(sport)
        return loader.list_active_players()


@st.cache_data(ttl=3600)
def load_active_teams(sport: str) -> pd.DataFrame:
    """Load active teams for the specified sport."""
    if sport == "NBA":
        return data_loader.list_active_teams()
    else:
        loader = DataLoaderFactory.create_loader(sport)
        return loader.list_active_teams()


@st.cache_data(ttl=1800)
def load_league_stats(sport: str, season: str) -> pd.DataFrame:
    """Load league stats for the specified sport."""
    if sport == "NBA":
        return data_loader.load_league_player_stats(season=season)
    else:
        loader = DataLoaderFactory.create_loader(sport)
        return loader.load_league_player_stats(season=season)


@st.cache_data(ttl=900)
def load_player_log(sport: str, player_id: int, season: str) -> pd.DataFrame:
    """Load player game log for the specified sport."""
    if sport == "NBA":
        return data_loader.load_player_game_log(player_id=player_id, season=season)
    else:
        loader = DataLoaderFactory.create_loader(sport)
        return loader.load_player_game_log(player_id=player_id, season=season)


@st.cache_data(ttl=900)
def load_team_log(sport: str, team_id: int, season: str) -> pd.DataFrame:
    """Load team game log for the specified sport."""
    if sport == "NBA":
        return data_loader.load_team_game_log(team_id=team_id, season=season)
    else:
        loader = DataLoaderFactory.create_loader(sport)
        return loader.load_team_game_log(team_id=team_id, season=season)



# Sidebar configuration with sport selector
with st.sidebar:
    st.markdown("## 🏆 Sport Selection")
    
    # Sport selector with improved UI
    available_sports = SportConfig.get_available_sports()
    sport_labels = {
        "NBA": "🏀 NBA Basketball",
        "NHL": "🏒 NHL Hockey"
    }
    
    selected_sport_label = st.radio(
        "Select Sport",
        options=[sport_labels[s] for s in available_sports],
        index=0,
        label_visibility="collapsed"
    )
    
    # Extract sport code from label
    sport = "NBA" if "NBA" in selected_sport_label else "NHL"
    st.session_state.sport = sport
    
    # Get sport-specific configuration
    sport_config = SportConfig.get_sport_config(sport)
    
    st.markdown("---")
    st.markdown("## 📊 League Settings")
    
    # Season selection
    seasons = sport_config["seasons"]
    season = st.selectbox("Season", seasons, index=0, format_func=format_season_label)

    # Load teams for selected sport
    teams_df = load_active_teams(sport)
    if teams_df.empty:
        st.error(f"Unable to load {sport} teams. Please check your connectivity.")
        st.stop()
    team_name = st.selectbox("Team", teams_df["full_name"].sort_values().tolist())

    # Load players for selected sport
    players_df = load_active_players(sport)
    
    # For NHL, show a message about player data
    if sport == "NHL" and players_df.empty:
        st.info("🚧 NHL player data is being loaded. Currently showing teams only.")
        st.markdown("*Full NHL player integration coming soon*")
        # Create a dummy player for demo purposes
        player_name = "Demo Player"
    else:
        if players_df.empty:
            st.error(f"Unable to load {sport} players. Please check your connectivity.")
            st.stop()
        player_name = st.selectbox("Player", players_df["full_name"].sort_values().tolist())


# Apply glassmorphism CSS based on selected sport
st.markdown(get_glassmorphism_css(sport), unsafe_allow_html=True)


# Hero Section with Sport-Specific Branding
st.markdown(
    f"""
    <div class='hero-section fade-in'>
        <div class='sport-badge'>{sport_config['display_name']}</div>
        <div class='signal-title'>Signal Sports Analytics</div>
        <div class='signal-subtitle'>
            Bloomberg-grade {sport} intelligence for performance, fatigue, and trends.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Get player and team IDs (NBA only for now, NHL will be implemented)
if sport == "NBA":
    player_id = data_loader.get_player_id(player_name)
    team_id = data_loader.get_team_id(team_name)
else:  # NHL
    # For demo purposes, use placeholder
    player_id = None
    loader = DataLoaderFactory.create_loader(sport)
    team_id = loader.get_team_id(team_name)


# Skip detailed analytics for NHL demo (data integration in progress)
if sport == "NHL":
    st.info("🚧 **NHL Analytics Dashboard - Demo Mode**")
    st.markdown("""
    ### Welcome to NHL Integration Preview!
    
    The NHL module is currently in **demo mode** with team data available. Full player analytics are being integrated.
    
    #### ✅ Currently Available:
    - NHL team listings (32 teams)
    - Sport-specific UI theming
    - Modular architecture ready for data integration
    
    #### 🔜 Coming Soon:
    **Skater Metrics**
    - Goals, Assists, Points, +/-, Shots
    - Time on Ice, Faceoff %, Hits, Blocks
    
    **Goalie Metrics**
    - Saves, Save %, GAA, Shutouts
    - Quality Starts, High Danger Saves
    
    **Advanced Stats**
    - Corsi, Fenwick, Expected Goals (xG)
    - PDO, CF%, Zone Starts
    
    **Team Analysis**
    - Power play/penalty kill stats
    - Lineup combinations
    - Shot charts and heat maps
    
    **Switch to NBA** to see the full analytics platform in action with live data!
    """)
    
    # Show team info for NHL
    st.markdown(f"### 🏒 {team_name}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Team ID", team_id if team_id else "N/A")
    with col2:
        st.metric("Season", season)
    with col3:
        st.metric("League", "NHL")
    with col4:
        st.metric("Teams", "32")
    
    st.markdown("---")
    st.caption("Signal Sports Analytics • Multi-Sport Platform • NHL Integration in Progress")
    st.stop()


# NBA Analytics (existing functionality)
if player_id is None:
    st.error("Player not found. Try another selection.")
    st.stop()

with st.spinner("Loading player analytics..."):
    player_log = load_player_log(sport, player_id, season)
if player_log.empty:
    st.warning("No game log data available for this player/season.")

league_stats = load_league_stats(sport, season)

team_log = pd.DataFrame()
if team_id is not None:
    team_log = load_team_log(sport, team_id, season)


# Enhanced metric cards with animation
st.markdown("<div class='section-header'>📈 Performance Metrics</div>", unsafe_allow_html=True)
metrics_cols = st.columns(4)
if not player_log.empty:
    points_avg = safe_mean(player_log["PTS"])
    assists_avg = safe_mean(player_log["AST"])
    rebounds_avg = safe_mean(player_log["REB"])
    minutes_avg = safe_mean(player_log["MIN"])
    recent_points = safe_mean(player_log.sort_values("GAME_DATE").tail(5)["PTS"])
    recent_assists = safe_mean(player_log.sort_values("GAME_DATE").tail(5)["AST"])
    recent_rebounds = safe_mean(player_log.sort_values("GAME_DATE").tail(5)["REB"])
    recent_minutes = safe_mean(player_log.sort_values("GAME_DATE").tail(5)["MIN"])
    points_delta = f"{recent_points - points_avg:+.1f}"
    assists_delta = f"{recent_assists - assists_avg:+.1f}"
    rebounds_delta = f"{recent_rebounds - rebounds_avg:+.1f}"
    minutes_delta = f"{recent_minutes - minutes_avg:+.1f}"
else:
    points_avg = assists_avg = rebounds_avg = minutes_avg = 0.0
    points_delta = assists_delta = rebounds_delta = minutes_delta = "+0.0"

metrics_cols[0].metric("Points", f"{points_avg:.1f}", points_delta)
metrics_cols[1].metric("Assists", f"{assists_avg:.1f}", assists_delta)
metrics_cols[2].metric("Rebounds", f"{rebounds_avg:.1f}", rebounds_delta)
metrics_cols[3].metric("Minutes", f"{minutes_avg:.1f}", minutes_delta)


left_col, right_col = st.columns([1.1, 1])

with left_col:
    st.markdown("### Fatigue Factor")
    if not team_log.empty:
        latest_game = team_log.sort_values("GAME_DATE").iloc[-1]
        
        # Safely calculate rest days with null checking
        game_date = latest_game["GAME_DATE"]
        if pd.notna(game_date):
            try:
                game_date_ts = pd.Timestamp(game_date)
                rest_days = max((pd.Timestamp.utcnow().date() - game_date_ts.date()).days, 0)
            except (TypeError, AttributeError, ValueError):
                rest_days = 1  # Default fallback
        else:
            rest_days = 1  # Default if date is NaT/missing
        
        fatigue_inputs = models.FatigueInputs(
            rest_days=rest_days,
            is_home=bool(latest_game.get("IS_HOME", True)),
            minutes_last_game=minutes_avg,
        )
        fatigue_score = models.calculate_fatigue_score(fatigue_inputs)
    else:
        fatigue_score = 0.0

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=fatigue_score,
            number={"font": {"color": "#FAFAFA"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#FF4B4B"},
                "steps": [
                    {"range": [0, 40], "color": "#00FFAA"},
                    {"range": [40, 70], "color": "#FFD166"},
                    {"range": [70, 100], "color": "#FF4B4B"},
                ],
            },
        )
    )
    gauge.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="#0E1117")
    st.plotly_chart(gauge, width="stretch")

with right_col:
    st.markdown("### 🎲 Prop Validator (Anomaly Detection)")
    prop_data = models.build_prop_validator(player_log, stat_col="PTS")
    if prop_data.empty:
        st.info("No prop validator data available.")
    else:
        display_cols = ["GAME_DATE", "PTS", "Rolling_Avg", "Season_Avg", "Signal"]
        prop_table = prop_data[display_cols].copy()

        def highlight_signal(row: pd.Series) -> list[str]:
            color = ""
            if row["Signal"] == "Hot Streak":
                color = "background-color: rgba(0, 255, 170, 0.2)"
            elif row["Signal"] == "Cold Streak":
                color = "background-color: rgba(255, 75, 75, 0.2)"
            return [color] * len(row)

        styled = prop_table.tail(10).style.apply(highlight_signal, axis=1)
        st.dataframe(styled, use_container_width=True)


st.markdown("---")  # Visual separator

trends_tab, advanced_tab, analytics_tab, comparisons_tab = st.tabs(
    ["📈 Trends", "🎯 Advanced Stats", "📊 Analytics", "⚖️ Comparisons"]
)

with trends_tab:
    st.markdown("<div class='section-header'>Player Performance Trends</div>", unsafe_allow_html=True)
    if player_log.empty:
        st.info("No recent games available.")
    else:
        # Import enhanced visualizations
        from components.shared.visualizations import (
            create_performance_trend_chart,
            create_distribution_chart,
            create_multi_stat_comparison,
        )

        # Performance trend chart
        trend_fig = create_performance_trend_chart(
            player_log, "PTS", player_name, sport, show_rolling_avg=True
        )
        st.plotly_chart(trend_fig, use_container_width=True)

        # Multi-stat comparison
        col1, col2 = st.columns([1, 1])
        with col1:
            multi_stat_fig = create_multi_stat_comparison(
                player_log, ["PTS", "AST", "REB", "MIN"], player_name, sport
            )
            st.plotly_chart(multi_stat_fig, use_container_width=True)

        with col2:
            # Distribution chart
            dist_fig = create_distribution_chart(player_log, "PTS", player_name, sport)
            st.plotly_chart(dist_fig, use_container_width=True)

with advanced_tab:
    st.markdown("<div class='section-header'>Player vs League Average Radar</div>", unsafe_allow_html=True)
    if league_stats.empty or not feature_cols:
        st.info("League stats not available.")
    else:
        from components.shared.visualizations import create_enhanced_radar_chart

        player_row = league_stats[league_stats["Player"] == player_name]
        league_avg = league_stats[feature_cols].mean(numeric_only=True)
        if player_row.empty:
            st.info("Player not found in league stats.")
        else:
            player_values = player_row.iloc[0][feature_cols]
            
            # Enhanced radar chart
            radar_fig = create_enhanced_radar_chart(
                player_values, league_avg, feature_cols, player_name, sport
            )
            st.plotly_chart(radar_fig, use_container_width=True)

            # Advanced stats table
            st.markdown("### 📊 Detailed Statistics")
            stats_df = pd.DataFrame(
                {
                    "Metric": feature_cols,
                    "Player": player_values.values,
                    "League Avg": league_avg.values,
                    "Percentile": [
                        (league_stats[col] < player_values[col]).sum() / len(league_stats) * 100
                        for col in feature_cols
                    ],
                }
            )
            stats_df["Percentile"] = stats_df["Percentile"].apply(lambda x: f"{x:.0f}%")
            st.dataframe(stats_df, use_container_width=True)

with analytics_tab:
    st.markdown("<div class='section-header'>Performance Analytics</div>", unsafe_allow_html=True)
    if player_log.empty:
        st.info("No game data available for analytics.")
    else:
        from components.shared.visualizations import create_home_away_comparison

        # Home vs Away performance
        home_away_fig = create_home_away_comparison(
            player_log, ["PTS", "AST", "REB"], player_name, sport
        )
        st.plotly_chart(home_away_fig, use_container_width=True)

        # Recent form analysis
        st.markdown("### 🔥 Recent Form")
        last_5 = player_log.sort_values("GAME_DATE").tail(5)
        last_10 = player_log.sort_values("GAME_DATE").tail(10)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Last 5 Games PPG",
                f"{safe_mean(last_5['PTS']):.1f}",
                f"{safe_mean(last_5['PTS']) - points_avg:+.1f}",
            )
        with col2:
            st.metric(
                "Last 10 Games PPG",
                f"{safe_mean(last_10['PTS']):.1f}",
                f"{safe_mean(last_10['PTS']) - points_avg:+.1f}",
            )
        with col3:
            hot_streak = (last_5["PTS"] > points_avg).sum()
            st.metric("Hot Games (Last 5)", f"{hot_streak}/5")

with comparisons_tab:
    st.markdown("<div class='section-header'>Player Comparisons & Similarity</div>", unsafe_allow_html=True)
    
    # Player Similarity Engine
    desired_features = ["Points", "Assists", "Rebounds", "UsageRate", "TrueShootingPct"]
    feature_cols = [col for col in desired_features if col in league_stats.columns]
    comps = models.find_player_comps(league_stats, player_name, feature_cols)
    
    if comps.empty:
        st.info("Similarity comps are not available for this player yet.")
    else:
        st.markdown("### 🎯 Similar Players")
        st.dataframe(
            comps[["Player", "Team", "Points", "Assists", "Rebounds", "SimilarityScore"]]
            .sort_values("SimilarityScore", ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
        )

st.caption("Signal Sports Analytics • MVP build for portfolio")
