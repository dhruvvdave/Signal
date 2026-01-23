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
        .block-container { padding-top: 2rem; max-width: 1440px; }
        .signal-title { font-size: 2.6rem; font-weight: 700; letter-spacing: 0.6px; }
        .signal-subtitle { color: #9aa0a6; font-size: 1rem; margin-top: 0.25rem; }
        .hero { background: linear-gradient(135deg, rgba(0,255,170,0.08), rgba(255,75,75,0.08)); padding: 1.5rem; border-radius: 18px; border: 1px solid #1f2937; }
        .hero-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
        .section-card { background: #111827; padding: 1.25rem; border-radius: 16px; border: 1px solid #1f2937; }
        .card-label { color: #9aa0a6; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08rem; }
        .card-value { font-size: 1.6rem; font-weight: 700; color: #FAFAFA; }
        .kpi-card { background: #0f172a; padding: 1rem; border-radius: 14px; border: 1px solid #1f2937; }
        .kpi-delta { font-size: 0.85rem; }
        .kpi-delta.positive { color: #00FFAA; }
        .kpi-delta.negative { color: #FF4B4B; }
        .tag { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem; }
        .tag-live { background: rgba(0, 255, 170, 0.15); color: #00FFAA; }
        [data-testid="stMetricValue"] { color: #00FFAA; }
        [data-testid="stMetricDelta"] { color: #FF4B4B; }
    </style>
    """,
    unsafe_allow_html=True,
)

nba_available = data_loader.NBA_API_AVAILABLE


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


@st.cache_data(ttl=1800)
def load_nhl_standings() -> pd.DataFrame:
    return data_loader.load_nhl_standings()


@st.cache_data(ttl=1800)
def load_nhl_team_stats() -> pd.DataFrame:
    return data_loader.load_nhl_team_stats()

def render_kpi(label: str, value: str, delta: str) -> None:
    delta_class = "positive" if delta.startswith("+") else "negative"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="kpi-delta {delta_class}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

seasons = ["2025-26", "2024-25"]

with st.sidebar:
    st.markdown("## League Console")
    season = st.selectbox("NBA Season", seasons, index=0, format_func=format_season_label)

    if nba_available:
        teams_df = load_active_teams()
        players_df = load_active_players()
        if teams_df.empty or players_df.empty:
            st.warning("NBA data unavailable. Check nba_api connectivity.")
        team_name = st.selectbox(
            "NBA Team",
            teams_df["full_name"].sort_values().tolist() if not teams_df.empty else [],
        )
        player_name = st.selectbox(
            "NBA Player",
            players_df["full_name"].sort_values().tolist() if not players_df.empty else [],
        )
    else:
        st.warning("nba_api not installed. NBA widgets disabled.")
        team_name = None
        player_name = None

    st.markdown("---")
    st.markdown("## NHL Controls")
    nhl_standings = load_nhl_standings()
    nhl_team_stats = load_nhl_team_stats()
    nhl_team_name = st.selectbox(
        "NHL Team",
        nhl_team_stats["Team"].sort_values().tolist() if not nhl_team_stats.empty else [],
    )


st.markdown(
    """
    <div class="hero">
        <div class="hero-row">
            <div>
                <div class="signal-title">Signal Sports Analytics</div>
                <div class="signal-subtitle">Portfolio-grade intelligence for NBA and NHL performance trends.</div>
            </div>
            <span class="tag tag-live">Live Data</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("")
tabs = st.tabs(["NBA Intelligence", "NHL Intelligence"])

with tabs[0]:
    st.markdown("#### NBA Intelligence Hub")
    if not nba_available:
        st.error("nba_api not installed. Enable NBA insights by installing nba_api.")
    elif not player_name:
        st.info("Select an NBA player in the sidebar to load insights.")
    else:
        player_id = data_loader.get_player_id(player_name)
        team_id = data_loader.get_team_id(team_name) if team_name else None
        if player_id is None:
            st.error("Player not found. Try another selection.")
            st.stop()

        with st.spinner("Loading player analytics..."):
            player_log = load_player_log(player_id, season)
        if player_log.empty:
            st.warning("No game log data available for this player/season.")

        league_stats = load_league_stats(season)
        desired_features = ["Points", "Assists", "Rebounds", "UsageRate", "TrueShootingPct"]
        if league_stats.empty:
            league_stats = pd.DataFrame(columns=["Player", "Team", *desired_features])
        else:
            for col in desired_features:
                if col not in league_stats.columns:
                    league_stats[col] = 0.0

        team_log = pd.DataFrame()
        if team_id is not None:
            team_log = load_team_log(team_id, season)

        card_cols = st.columns(4)
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

        with card_cols[0]:
            render_kpi("Points", f"{points_avg:.1f}", points_delta)
        with card_cols[1]:
            render_kpi("Assists", f"{assists_avg:.1f}", assists_delta)
        with card_cols[2]:
            render_kpi("Rebounds", f"{rebounds_avg:.1f}", rebounds_delta)
        with card_cols[3]:
            render_kpi("Minutes", f"{minutes_avg:.1f}", minutes_delta)

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
            feature_cols = [col for col in desired_features if col in league_stats.columns]
            comps = models.find_player_comps(league_stats, player_name, feature_cols)
            if comps.empty:
                st.info("Similarity comps are not available for this player yet.")
            else:
                display_cols = ["Player", "Team", "Points", "Assists", "Rebounds", "SimilarityScore"]
                display_cols = [col for col in display_cols if col in comps.columns]
                st.dataframe(
                    comps[display_cols]
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

with tabs[1]:
    st.markdown("#### NHL Snapshot")
    if nhl_standings.empty or nhl_team_stats.empty:
        st.warning("Unable to load NHL data. Check API connectivity.")
    else:
        nhl_summary_cols = st.columns(3)
        total_teams = nhl_team_stats["Team"].nunique()
        avg_gpg = nhl_team_stats["GoalsPerGame"].mean()
        avg_pk = nhl_team_stats["PenaltyKillPct"].mean()
        with nhl_summary_cols[0]:
            render_kpi("Teams tracked", f"{total_teams}", "+0.0")
        with nhl_summary_cols[1]:
            render_kpi("Avg Goals/Game", f"{avg_gpg:.2f}", "+0.0")
        with nhl_summary_cols[2]:
            render_kpi("Avg PK%", f"{avg_pk:.1f}", "+0.0")

        st.markdown("### League Standings")
        standings_view = nhl_standings.sort_values(["Points", "GoalDiff"], ascending=False)
        st.dataframe(standings_view, width="stretch")

        st.markdown("### Team Performance Profile")
        if nhl_team_name:
            selected_team = nhl_team_stats[nhl_team_stats["Team"] == nhl_team_name]
            if not selected_team.empty:
                profile = selected_team.iloc[0]
                profile_cols = st.columns(4)
                profile_cols[0].metric("Goals/Game", f"{profile['GoalsPerGame']:.2f}")
                profile_cols[1].metric("Goals Against", f"{profile['GoalsAgainstPerGame']:.2f}")
                profile_cols[2].metric("Shots/Game", f"{profile['ShotsPerGame']:.1f}")
                profile_cols[3].metric("Power Play %", f"{profile['PowerPlayPct']:.1f}")

        chart = px.bar(
            nhl_team_stats.sort_values("GoalsPerGame", ascending=False).head(12),
            x="GoalsPerGame",
            y="Team",
            orientation="h",
            title="Top Offenses (Goals per Game)",
            color="GoalsPerGame",
            color_continuous_scale="Turbo",
        )
        chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            height=360,
        )
        st.plotly_chart(chart, width="stretch")

st.caption("Signal Sports Analytics • Portfolio-grade multi-league intelligence")
