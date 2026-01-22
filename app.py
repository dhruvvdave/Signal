"""Streamlit app entry point for Signal Sports Analytics."""

from __future__ import annotations

import importlib.util

import pandas as pd
import streamlit as st

import data_loader
import models
from utils import format_season_label, safe_mean


st.set_page_config(
    page_title="Signal Sports Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .block-container { padding-top: 2rem; }
        .metric-label { color: #FAFAFA; }
        .signal-title { font-size: 2.2rem; font-weight: 700; }
        .signal-subtitle { color: #9aa0a6; font-size: 1rem; }
        [data-testid="stMetricValue"] { color: #00FFAA; }
        [data-testid="stMetricDelta"] { color: #FF4B4B; }
    </style>
    """,
    unsafe_allow_html=True,
)


def require_dependency(module_name: str, install_hint: str) -> None:
    """Ensure a dependency is available before importing it."""
    if importlib.util.find_spec(module_name) is None:
        st.error(f"Missing dependency: `{module_name}`. {install_hint}")
        st.stop()


require_dependency("plotly", "Install it with `pip install plotly` and restart the app.")
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data(ttl=3600)
def load_active_players() -> pd.DataFrame:
    return data_loader.list_active_players()


@st.cache_data(ttl=3600)
def load_active_teams() -> pd.DataFrame:
    return data_loader.list_active_teams()


@st.cache_data(ttl=1800)
def load_league_stats(season: str) -> pd.DataFrame:
    return data_loader.load_league_player_stats(season=season)


@st.cache_data(ttl=900)
def load_player_log(player_id: int, season: str) -> pd.DataFrame:
    return data_loader.load_player_game_log(player_id=player_id, season=season)


@st.cache_data(ttl=900)
def load_team_log(team_id: int, season: str) -> pd.DataFrame:
    return data_loader.load_team_game_log(team_id=team_id, season=season)


seasons = ["2023-24", "2022-23", "2021-22"]

with st.sidebar:
    st.markdown("## League Settings")
    league = st.selectbox("League", ["NBA"], index=0)
    season = st.selectbox("Season", seasons, index=0, format_func=format_season_label)

    teams_df = load_active_teams()
    if teams_df.empty:
        st.error("Unable to load teams. Please check your NBA API connectivity.")
        st.stop()
    team_name = st.selectbox("Team", teams_df["full_name"].sort_values().tolist())

    players_df = load_active_players()
    if players_df.empty:
        st.error("Unable to load players. Please check your NBA API connectivity.")
        st.stop()
    player_name = st.selectbox("Player", players_df["full_name"].sort_values().tolist())


st.markdown("<div class='signal-title'>Signal Sports Analytics</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='signal-subtitle'>Bloomberg-grade NBA intelligence for performance, fatigue, and trends.</div>",
    unsafe_allow_html=True,
)

player_id = data_loader.get_player_id(player_name)
team_id = data_loader.get_team_id(team_name)

if player_id is None:
    st.error("Player not found. Try another selection.")
    st.stop()

with st.spinner("Loading player analytics..."):
    player_log = load_player_log(player_id, season)
if player_log.empty:
    st.warning("No game log data available for this player/season.")

league_stats = load_league_stats(season)

team_log = pd.DataFrame()
if team_id is not None:
    team_log = load_team_log(team_id, season)


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
        rest_days = max((pd.Timestamp.utcnow().date() - latest_game["GAME_DATE"].date()).days, 0)
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
    st.markdown("### Player Similarity (Comp Engine)")
    desired_features = ["Points", "Assists", "Rebounds", "UsageRate", "TrueShootingPct"]
    feature_cols = [col for col in desired_features if col in league_stats.columns]
    comps = models.find_player_comps(league_stats, player_name, feature_cols)
    if comps.empty:
        st.info("Similarity comps are not available for this player yet.")
    else:
        st.dataframe(
            comps[["Player", "Team", "Points", "Assists", "Rebounds", "SimilarityScore"]]
            .sort_values("SimilarityScore", ascending=False)
            .reset_index(drop=True),
            width="stretch",
        )


st.markdown("### Prop Validator (Anomaly Detection)")
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

    styled = prop_table.style.apply(highlight_signal, axis=1)
    st.dataframe(styled, width="stretch")


trends_tab, advanced_tab = st.tabs(["Trends", "Advanced"])

with trends_tab:
    st.markdown("### Player Performance Trends")
    if player_log.empty:
        st.info("No recent games available.")
    else:
        last_10 = player_log.sort_values("GAME_DATE").tail(10)
        fig = px.line(
            last_10,
            x="GAME_DATE",
            y="PTS",
            markers=True,
            title=f"{player_name} - Points (Last 10 Games)",
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=320,
        )
        st.plotly_chart(fig, width="stretch")

with advanced_tab:
    st.markdown("### Player vs League Average Radar")
    if league_stats.empty or not feature_cols:
        st.info("League stats not available.")
    else:
        player_row = league_stats[league_stats["Player"] == player_name]
        league_avg = league_stats[feature_cols].mean(numeric_only=True)
        if player_row.empty:
            st.info("Player not found in league stats.")
        else:
            player_values = player_row.iloc[0][feature_cols]
            radar_df = pd.DataFrame(
                {
                    "Metric": feature_cols,
                    "Player": player_values.values,
                    "League Average": league_avg.values,
                }
            )
            radar_fig = go.Figure()
            radar_fig.add_trace(
                go.Scatterpolar(
                    r=radar_df["Player"],
                    theta=radar_df["Metric"],
                    fill="toself",
                    name=player_name,
                    line_color="#00FFAA",
                )
            )
            radar_fig.add_trace(
                go.Scatterpolar(
                    r=radar_df["League Average"],
                    theta=radar_df["Metric"],
                    fill="toself",
                    name="League Avg",
                    line_color="#FF4B4B",
                )
            )
            radar_fig.update_layout(
                polar=dict(bgcolor="#0E1117"),
                showlegend=True,
                template="plotly_dark",
                height=360,
                margin=dict(l=40, r=40, t=40, b=40),
            )
            st.plotly_chart(radar_fig, width="stretch")

st.caption("Signal Sports Analytics • MVP build for portfolio")
