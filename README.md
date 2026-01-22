# Signal Sports Analytics

A portfolio-ready NBA analytics dashboard that blends modern data engineering with a Bloomberg-inspired UI. The app pulls NBA data via `nba_api`, computes fatigue and anomaly signals, and surfaces interactive visuals for player performance trends and comparisons.

## Features
- **Fatigue Factor** gauge based on rest, travel, and starter minutes.
- **Player Similarity Engine** using KNN + StandardScaler for comps.
- **Prop Validator** to flag hot/cold streaks from rolling averages.
- **Trends + Advanced Views** with Plotly charts and a radar comparison.

## Tech Stack
- **Python 3.9+**
- **Streamlit** UI (`st.set_page_config(layout="wide")`)
- **NBA API** (`nba_api`)
- **Scikit-Learn** (KNN + scaling)
- **Plotly** for charts
- **SQLite-ready** (optional) and cached data access via `st.cache_data`

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run app.py
```

## Troubleshooting
- **ModuleNotFoundError: plotly**: confirm `requirements.txt` is installed and redeploy. If hosting on Streamlit Cloud, trigger a reboot after updating dependencies.

## Portfolio Deployment Options
- **Streamlit Community Cloud** (fastest)
  1. Push this repo to GitHub.
  2. Connect it at https://streamlit.io/cloud.
  3. Deploy with `app.py` as the entry point.

- **Hugging Face Spaces** (public demo)
  1. Create a new Space (Streamlit).
  2. Upload this repo content.
  3. Set the entry command to `streamlit run app.py`.

- **Render** (custom domain)
  1. Create a new web service.
  2. Set the build command to `pip install -r requirements.txt`.
  3. Set the start command to `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

## Tips for Portfolio Presentation
- Add a short **case study** section on your portfolio describing the data sources, modeling approach, and design inspiration.
- Include screenshots or a short GIF demo of the dashboard.
- Link directly to the live app and GitHub repository for credibility.

---

**Signal Sports Analytics** — Bloomberg-grade insights for player performance and fatigue.
