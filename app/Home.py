import streamlit as st
import plotly.graph_objects as go
from utils import (inject_css, load_data, divider, LEAGUE_COLORS, LEAGUE_LABELS, apply_template)

st.set_page_config(
    page_title="The Price of Victory",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.markdown("""
<style>
.block-container { padding-top: 1rem; }

.finding-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 14px;
    margin-bottom: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,179,255,0.10);
    border-radius: 12px;
    color: rgba(200,216,240,0.85);
    font-size: 0.92rem;
    line-height: 1.6;
}

.finding-item:last-child {
    margin-bottom: 0;
}

.finding-icon {
    font-size: 1.15rem;
    line-height: 1;
}

.finding-strong {
    color: #ffffff;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.image("../assets/banner.png", use_container_width=True)

df = load_data()

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg,rgba(18,70,196,0.6),rgba(0,229,204,0.2));
    border:1px solid rgba(99,179,255,0.2);
    border-radius:20px;
    padding:48px 40px 40px 40px;
    margin-bottom:28px;
    overflow:hidden;
">
    <div style="font-size:2.8rem;font-weight:900;letter-spacing:-0.02em;line-height:1;color:#fff;margin-bottom:16px;">
        THE PRICE OF VICTORY
    </div>
    <div style="display:inline-block;background:linear-gradient(90deg,#00e5cc,#4da6ff);
        border-radius:8px;padding:10px 20px;font-weight:700;font-size:1rem;color:#0a0e1a;">
        Does Financial Power Drive Success in European Football?
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#00e5cc,#4da6ff)">
        <div class="kpi-icon">🏟️</div>
        <div class="kpi-label">Total Clubs</div>
        <div class="kpi-value">160</div>
    </div>
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#4da6ff,#a78bfa)">
        <div class="kpi-icon">🗓️</div>
        <div class="kpi-label">Seasons Covered</div>
        <div class="kpi-value">10</div>
    </div>
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#a78bfa,#ff6b9d)">
        <div class="kpi-icon">🌍</div>
        <div class="kpi-label">Leagues Analysed</div>
        <div class="kpi-value">5</div>
    </div>
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#f7c36a,#00e5cc)">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Avg Squad Value</div>
        <div class="kpi-value">€599.5M</div>
    </div>
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#ff6b9d,#f7c36a)">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">Avg Transfer Spend</div>
        <div class="kpi-value">€39.0M</div>
    </div>
    <div class="kpi-card" style="--accent:linear-gradient(90deg,#34d399,#4da6ff)">
        <div class="kpi-icon">📊</div>
        <div class="kpi-label">Total Records</div>
        <div class="kpi-value">978</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Research question ─────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
    background:linear-gradient(90deg,#00e5cc,#4da6ff);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:8px;">
    Research Question
</div>
<div style="font-size:1.7rem;font-weight:800;line-height:1.25;color:#fff;margin-bottom:16px;">
    Does spending more money guarantee winning more games?
</div>
<p style="color:rgba(200,216,240,0.75);font-size:0.95rem;line-height:1.7;">
    This project analyses a decade of financial and performance data across Europe's top 5 leagues -
    the Premier League, La Liga, Serie A, Bundesliga, and Ligue 1, <br> to understand how Squad Value
    and Transfer Spending relate to performance outcomes.
</p>
<p style="color:rgba(200,216,240,0.75);font-size:0.95rem;line-height:1.7;margin-bottom:28px;">
    Rather than relying on simple correlations, this analysis reveals which clubs outperform their financial means,
    which ones fail despite heavy investment, <br> and how the connection between money and success shifts across different footballing environments.
</p>
""", unsafe_allow_html=True)

# ── Key findings ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
    background:linear-gradient(90deg,#00e5cc,#4da6ff);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:14px;margin-top:10px;">
    Key Findings
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">🇬🇧</span>
    <span>Premier League spends <span class="finding-strong">3× more</span> than Bundesliga on average</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">📉</span>
    <span><span class="finding-strong">Squad value</span> predicts points better than transfer spend</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">⚡</span>
    <span><span class="finding-strong">30%</span> of titles were won by the single highest spender</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">🦁</span>
    <span>Leicester City and Monaco emerged as standout overperformers</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">💸</span>
    <span>Chelsea 2022/23 recorded the worst ROI — <span class="finding-strong">€574M</span> spent for just <span class="finding-strong">44 points</span></span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="finding-item">
    <span class="finding-icon">🏦</span>
    <span>State-backed clubs initially overperform, then plateau over time</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)