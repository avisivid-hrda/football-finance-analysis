import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

# ── Constants ─────────────────────────────────────────────────────────────────
LEAGUE_COLORS = {
    "premier-league": "#00e5cc",
    "laliga":         "#4da6ff",
    "serie-a":        "#ff6b9d",
    "bundesliga":     "#f7c36a",
    "ligue-1":        "#a78bfa",
}
LEAGUE_LABELS = {
    "premier-league": "Premier League 🇬🇧",
    "laliga":         "La Liga 🇪🇸",
    "serie-a":        "Serie A 🇮🇹",
    "bundesliga":     "Bundesliga 🇩🇪",
    "ligue-1":        "Ligue 1 🇫🇷",
}

# ── CSS ───────────────────────────────────────────────────────────────────────
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b3e 40%, #0b2d7a 75%, #1246c4 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
}
[data-testid="stHeader"] { background: transparent !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101f 0%, #0a1a3a 100%) !important;
    border-right: 1px solid rgba(99,179,255,0.15) !important;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    margin: 2px 8px !important;
    transition: background 0.2s !important;
    font-size: 0.92rem !important;
}
[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,198,180,0.25), rgba(18,70,196,0.35)) !important;
    color: #00e5cc !important;
}
/* Hide default streamlit page icon in nav */
[data-testid="stSidebarNavLink"] svg { display: none !important; }

h1, h2, h3, h4, h5, h6, p, li, span, label, div {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00e5cc, #4da6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.page-title {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -0.01em;
    line-height: 1.1;
    color: #ffffff !important;
    margin-bottom: 6px;
}
.page-subtitle {
    font-size: 1rem;
    color: rgba(200,216,240,0.75) !important;
    margin-bottom: 32px;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0;
}
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,255,0.18);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: rgba(0,229,204,0.4); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, linear-gradient(90deg,#00e5cc,#4da6ff));
    border-radius: 16px 16px 0 0;
}
.kpi-icon { font-size: 1.5rem; margin-bottom: 8px; }
.kpi-label {
    font-size: 0.78rem !important;
    color: rgba(200,216,240,0.65) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1;
}
.insight-box {
    background: rgba(0,229,204,0.07);
    border-left: 3px solid #00e5cc;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.92rem;
    color: rgba(220,235,255,0.9) !important;
}
.flourish-placeholder {
    background: rgba(255,255,255,0.03);
    border: 2px dashed rgba(99,179,255,0.3);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    color: rgba(200,216,240,0.5) !important;
    font-size: 0.88rem;
}
.flourish-placeholder b { color: #4da6ff !important; }
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,255,0.3), transparent);
    margin: 32px 0;
}
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(99,179,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,255,0.18);
    border-radius: 14px;
    padding: 16px;
}
[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: rgba(200,216,240,0.65) !important; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
/* Tabs */
[data-testid="stTabs"] button {
    color: rgba(200,216,240,0.6) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00e5cc !important;
    border-bottom-color: #00e5cc !important;
}
</style>
"""

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    # works whether run from app/ or repo root
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "final", "master_football_engineered.csv")
    df = pd.read_csv(path)
    df["spending_m"] = df["transfer_spending"] / 1e6
    df["svalue_m"]   = df["squad_market_value"] / 1e6
    df["league_label"] = df["league"].map(LEAGUE_LABELS)
    return df

@st.cache_data
def compute_residuals(_df):
    d = _df.copy()
    X = d[["squad_market_value"]].fillna(0)
    y = d["points"]
    model = LinearRegression().fit(X, y)
    d["predicted_points"] = model.predict(X).round(1)
    d["residual"] = (d["points"] - d["predicted_points"]).round(1)

    d2 = d[d["transfer_spending"] > 0].copy()
    X2 = d2[["transfer_spending"]]
    y2 = d2["points"]
    m2 = LinearRegression().fit(X2, y2)
    d2["pred_pts_spend"] = m2.predict(X2).round(1)
    d2["residual_spend"] = (d2["points"] - d2["pred_pts_spend"]).round(1)
    d = d.merge(d2[["club_id","year","pred_pts_spend","residual_spend"]], on=["club_id","year"], how="left")
    return d

# ── Helper functions ──────────────────────────────────────────────────────────
def inject_css():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def section_header(label, title, subtitle=""):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">⚽ {title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

def flourish_embed(url, height=500, caption=""):
    if url.startswith("PLACEHOLDER"):
        st.markdown(f"""
        <div class="flourish-placeholder">
            <b>📊 Flourish Chart — Paste your embed URL here</b><br><br>
            <code style="color:#00e5cc;background:rgba(0,229,204,0.1);padding:4px 8px;border-radius:6px;">{url}</code>
            {f'<br><br><em>{caption}</em>' if caption else ''}
        </div>""", unsafe_allow_html=True)
    else:
        st.components.v1.iframe(url, height=height, scrolling=False)

def apply_template(fig):
    fig.update_layout(
        template="plotly_dark",  # ensures consistent base styling

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",

        font=dict(
            family="Inter",
            color="#c8d8f0"
        ),

        # ✅ Reliable title styling
        title=dict(
            font=dict(
                color="#eaf2ff",
                size=20
            )
        ),

        xaxis=dict(
            gridcolor="rgba(99,179,255,0.10)",
            zerolinecolor="rgba(99,179,255,0.10)",
            title_font=dict(color="#c8d8f0"),
            tickfont=dict(color="#c8d8f0")
        ),

        yaxis=dict(
            gridcolor="rgba(99,179,255,0.10)",
            zerolinecolor="rgba(99,179,255,0.10)",
            title_font=dict(color="#c8d8f0"),
            tickfont=dict(color="#c8d8f0")
        ),

        legend=dict(
            font=dict(color="#c8d8f0")
        )
    )
    return fig