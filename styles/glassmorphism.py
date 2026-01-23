"""Modern CSS styles for Signal Sports Analytics."""


def get_glassmorphism_css(sport: str = "NBA") -> str:
    """Return glassmorphism CSS with sport-specific theming.

    Args:
        sport: Sport name (NBA or NHL) for color theming

    Returns:
        CSS string with modern glassmorphism design
    """
    # Sport-specific colors
    if sport == "NHL":
        primary_color = "#C8102E"  # NHL Red
        accent_color = "#FFFFFF"  # White
        gradient_start = "#C8102E"
        gradient_end = "#8B0000"
    else:  # NBA default
        primary_color = "#1D428A"  # NBA Blue
        accent_color = "#00FFAA"  # Teal
        gradient_start = "#1D428A"
        gradient_end = "#00FFAA"

    return f"""
    <style>
        /* Base App Styling */
        .stApp {{
            background: linear-gradient(135deg, #0E1117 0%, #1a1f2e 100%);
            color: #FAFAFA;
        }}

        /* Glassmorphism Container */
        .glass-container {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s ease;
        }}

        .glass-container:hover {{
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
            transform: translateY(-2px);
        }}

        /* Modern Metric Cards */
        .metric-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {gradient_start} 0%, {gradient_end} 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .metric-card:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
        }}

        .metric-card:hover::before {{
            opacity: 1;
        }}

        /* Enhanced Typography */
        .signal-title {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
            animation: fadeInUp 0.6s ease-out;
        }}

        .signal-subtitle {{
            color: #9aa0a6;
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease-out;
        }}

        /* Metric Value Styling */
        [data-testid="stMetricValue"] {{
            color: {accent_color};
            font-weight: 700;
            font-size: 2rem;
            text-shadow: 0 0 20px {accent_color}40;
        }}

        [data-testid="stMetricDelta"] {{
            color: #FF4B4B;
            font-weight: 600;
        }}

        .metric-label {{
            color: #FAFAFA;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.85rem;
            opacity: 0.8;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1a1f2e 0%, #0E1117 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        [data-testid="stSidebar"] .block-container {{
            padding-top: 2rem;
        }}

        /* Modern Buttons and Inputs */
        .stSelectbox, .stMultiSelect {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}

        .stSelectbox:hover, .stMultiSelect:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: {accent_color};
        }}

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            color: #9aa0a6;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: none;
            transition: all 0.3s ease;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background: rgba(255, 255, 255, 0.08);
            color: #FAFAFA;
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background: linear-gradient(135deg, {gradient_start}40 0%, {gradient_end}40 100%);
            color: {accent_color};
            border-color: {accent_color};
        }}

        /* Dataframe Styling */
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* Loading Animation */
        .stSpinner > div {{
            border-top-color: {accent_color} !important;
        }}

        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideInRight {{
            from {{
                opacity: 0;
                transform: translateX(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        .fade-in {{
            animation: fadeInUp 0.6s ease-out;
        }}

        /* Chart Container */
        .chart-container {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 1rem 0;
        }}

        /* Hero Section */
        .hero-section {{
            background: linear-gradient(135deg, {gradient_start}20 0%, {gradient_end}20 100%);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}

        /* Sport Badge */
        .sport-badge {{
            display: inline-block;
            background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px {gradient_start}60;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .signal-title {{
                font-size: 2rem;
            }}

            .signal-subtitle {{
                font-size: 0.9rem;
            }}

            .metric-card {{
                padding: 1rem;
            }}
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb {{
            background: {accent_color}60;
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {accent_color};
        }}

        /* Block Container */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}

        /* Section Headers */
        .section-header {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {accent_color};
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {accent_color}40;
        }}
    </style>
    """
