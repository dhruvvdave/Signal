# Signal Sports Analytics

<div align="center">

![Signal Sports Analytics](https://img.shields.io/badge/Signal-Sports%20Analytics-00FFAA?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-1D428A?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Bloomberg-grade multi-sport analytics platform** combining modern data engineering with stunning UI/UX design.

[Live Demo](#) • [Features](#features) • [Tech Stack](#tech-stack) • [Setup](#local-setup)

</div>

---

## 🚀 Overview

Signal Sports Analytics is a **portfolio-grade, multi-sport analytics dashboard** that delivers professional-level insights for NBA and NHL. Built with a modern glassmorphism design system, it provides fatigue analysis, player comparisons, performance trends, and advanced statistical modeling—all wrapped in an intuitive, Bloomberg-inspired interface.

## ✨ Features

### 🏀 Multi-Sport Support
- **NBA Basketball**: Full player stats, game logs, advanced metrics
- **NHL Hockey**: Team data, player integration (in progress)
- Seamless sport switching with sport-specific theming
- Extensible architecture for adding more sports

### 🎨 Modern UI/UX Design
- **Glassmorphism** design with frosted glass effects and backdrop blur
- **Gradient accents** with sport-specific color schemes
- **Animated metric cards** with hover effects and smooth transitions
- **Responsive design** optimized for desktop, tablet, and mobile
- **Dark mode** with professional contrast ratios
- **Custom scrollbars** and loading states

### 📊 Advanced Analytics

#### Performance Metrics
- Season averages with 5-game trends
- Real-time performance deltas
- Home vs Away splits
- Recent form analysis (Last 5, Last 10 games)
- Hot/cold streak detection

#### Fatigue Factor Analysis
- Rest days calculation
- Home/away travel component
- Minutes played impact
- Visual gauge with color-coded risk levels

#### Player Similarity Engine
- KNN-based player comparisons
- Multi-dimensional feature matching
- Similarity scores with league context
- Find comparable players across the league

#### Prop Validator
- Anomaly detection for betting props
- Rolling averages vs season averages
- Hot/cold streak identification
- Visual signal indicators

### 📈 Enhanced Visualizations
- **Performance Trends**: Interactive line charts with rolling averages
- **Distribution Charts**: Histograms with mean/median indicators
- **Multi-Stat Comparisons**: Subplot grids for comprehensive analysis
- **Enhanced Radar Charts**: Normalized player vs league comparisons
- **Home/Away Analysis**: Grouped bar charts for venue performance
- **Interactive Tooltips**: Hover for detailed statistics
- **Chart Customization**: Sport-specific theming and colors

### 🎯 Advanced Features
- **4-Tab Navigation System**:
  - 📈 **Trends**: Performance over time with rolling averages
  - 🎯 **Advanced Stats**: Radar charts and percentile rankings
  - 📊 **Analytics**: Home/away splits and recent form
  - ⚖️ **Comparisons**: Player similarity and league standings
- **League Percentile Rankings**: See where players rank
- **Detailed Statistics Tables**: Comprehensive stat breakdowns
- **Dynamic Data Caching**: 15-60 minute TTL for optimal performance

## 🛠 Tech Stack

### Frontend & UI
- **Streamlit 1.36+**: Modern Python web framework
- **Custom CSS**: Glassmorphism, animations, responsive design
- **Plotly 5.22+**: Interactive, publication-quality charts
- **Streamlit Components**: Enhanced UI elements

### Data & Analytics
- **NBA API (nba_api)**: Official NBA statistics
- **NHL API (nhl-api-py)**: Hockey data integration
- **Pandas 2.2+**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Machine Learning
- **scikit-learn 1.5+**: KNN for player similarity
- **StandardScaler**: Feature normalization
- **SciPy**: Statistical analysis
- **statsmodels**: Advanced statistical modeling

### Deployment
- **Python 3.9+**: Modern Python runtime
- **Git**: Version control
- **Streamlit Cloud**: Easy deployment (recommended)
- **Docker-ready**: Container support (optional)

## 📦 Local Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/dhruvvdave/Signal.git
cd Signal
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
Navigate to `http://localhost:8501`

## 🎨 Design Philosophy

Signal Sports Analytics draws inspiration from:
- **Bloomberg Terminal**: Professional, data-dense layouts
- **Modern SaaS Dashboards**: Clean, minimal aesthetics  
- **ESPN Stats & Info**: Clear data presentation
- **Trading Platforms**: Real-time updates and multi-view layouts

### Color Palette
- **NBA Theme**: Modern blues (#1D428A) and teals (#00FFAA)
- **NHL Theme**: Bold reds (#C8102E) and whites
- **Accent Colors**: Vibrant highlights for key metrics
- **Dark Mode**: Professional contrast with #0E1117 base

## 📂 Project Structure

```
Signal/
├── app.py                      # Main application entry point
├── data_loader.py              # Legacy NBA data loading
├── models.py                   # Analytics models (fatigue, similarity, prop validator)
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment
├── config/
│   └── sport_config.py         # Sport-specific configurations
├── services/
│   ├── nba/
│   │   └── nba_data_loader.py  # NBA data service
│   ├── nhl/
│   │   └── nhl_data_loader.py  # NHL data service
│   └── shared/
│       ├── base_data_loader.py # Abstract base class
│       └── data_loader_factory.py # Sport loader factory
├── components/
│   └── shared/
│       └── visualizations.py   # Enhanced chart components
└── styles/
    └── glassmorphism.py        # Modern CSS styling system
```

## 🌐 Deployment Options

### Streamlit Community Cloud (Recommended)
1. Push this repo to GitHub
2. Connect at [streamlit.io/cloud](https://streamlit.io/cloud)
3. Deploy with `app.py` as entry point
4. **No configuration needed!**

### Heroku
```bash
# Add Procfile
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

# Deploy
heroku create signal-sports-analytics
git push heroku main
```

### Render
1. Create new Web Service
2. Build: `pip install -r requirements.txt`
3. Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🚧 Roadmap

### Phase 1: NHL Full Integration ✅ (In Progress)
- [x] NHL team data
- [x] Multi-sport architecture
- [ ] NHL player game logs
- [ ] NHL-specific metrics (Corsi, Fenwick, xG)
- [ ] Goalie statistics

### Phase 2: Advanced Features
- [ ] Predictive models (next game projections)
- [ ] Playoff probability calculator
- [ ] Injury impact analysis
- [ ] Matchup analysis (head-to-head)
- [ ] Travel distance calculations

### Phase 3: Enhanced Visualizations
- [ ] Heat maps (shot charts, ice time)
- [ ] Correlation matrices
- [ ] Time series with range selectors
- [ ] Distribution plots (box plots)
- [ ] Export functionality (PNG, CSV, PDF)

### Phase 4: Real-Time Features
- [ ] Live score ticker
- [ ] Game status indicators
- [ ] Today's games dashboard
- [ ] Recent highlights section

### Phase 5: Team & Roster Analysis
- [ ] Team statistics dashboard
- [ ] Lineup combinations
- [ ] Power rankings
- [ ] Offensive/defensive ratings

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/dhruvvdave/Signal/issues).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NBA API**: [swar/nba_api](https://github.com/swar/nba_api) for comprehensive NBA data
- **NHL API**: NHL's official API for hockey statistics
- **Streamlit**: For the amazing web framework
- **Plotly**: For interactive visualization capabilities

## 📧 Contact

**Dhruv Dave** - Portfolio Project

- GitHub: [@dhruvvdave](https://github.com/dhruvvdave)
- Project Link: [https://github.com/dhruvvdave/Signal](https://github.com/dhruvvdave/Signal)

---

<div align="center">

**Signal Sports Analytics** • Built with ❤️ for the game

</div>
