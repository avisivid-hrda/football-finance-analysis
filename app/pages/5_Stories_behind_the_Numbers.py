import streamlit as st
import pandas as pd
from utils import inject_css, load_data, section_header, LEAGUE_LABELS

st.set_page_config(page_title="Club Case Studies", page_icon="🔍", layout="wide")
inject_css()

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}

/* ========== CLOSED SELECTBOX ========== */
div[data-baseweb="select"] > div {
    background: #2a3f73 !important;
    border: 1px solid rgba(99,179,255,0.28) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] input {
    color: #ffffff !important;
}

div[data-baseweb="select"] span {
    color: #ffffff !important;
}

div[data-baseweb="select"] svg {
    fill: #dbe7ff !important;
}

/* Focus state */
div[data-baseweb="select"] > div:focus-within {
    border: 1px solid #63b3ff !important;
    box-shadow: 0 0 0 1px #63b3ff !important;
}

/* ========== OPEN DROPDOWN PANEL ========== */
div[data-baseweb="popover"] > div {
    background: #1c3270 !important;
    border: 1px solid rgba(99,179,255,0.28) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28) !important;
}

/* List container */
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] [role="listbox"] {
    background: #1c3270 !important;
    padding: 4px !important;
    margin: 0 !important;
}

/* Each option */
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] [role="option"] {
    background: transparent !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    margin: 2px 0 !important;
}

/* Hovered option */
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover {
    background: rgba(255,255,255,0.10) !important;
    color: #ffffff !important;
}

/* Selected option */
div[data-baseweb="popover"] li[aria-selected="true"],
div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
}

/* Highlighted / keyboard-focused option */
div[data-baseweb="popover"] li[aria-current="true"],
div[data-baseweb="popover"] [role="option"][aria-current="true"] {
    background: rgba(255,255,255,0.10) !important;
    color: #ffffff !important;
}

/* ========== EXISTING CARDS ========== */
.case-card {
    background: linear-gradient(135deg, rgba(18,70,196,0.20), rgba(0,229,204,0.08));
    border: 1px solid rgba(99,179,255,0.18);
    border-radius: 18px;
    padding: 24px 24px 18px 24px;
    margin-bottom: 18px;
}

.case-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 14px;
    margin: 16px 0 16px 0;
}

.case-kpi {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,255,0.12);
    border-radius: 14px;
    padding: 14px 16px;
}

.case-kpi-label {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(200,216,240,0.68);
    margin-bottom: 8px;
}

.case-kpi-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #ffffff;
}

.story-box {
    background: rgba(255,255,255,0.03);
    border-left: 4px solid #00e5cc;
    border-radius: 10px;
    padding: 16px 18px;
    color: rgba(200,216,240,0.88);
    line-height: 1.7;
    margin-top: 10px;
}

.story-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #00e5cc;
    font-weight: 700;
    margin-bottom: 6px;
}

.small-note {
    color: rgba(200,216,240,0.72);
    font-size: 0.92rem;
    line-height: 1.7;
    margin-top: 8px;
    margin-bottom: 18px;
}

@media (max-width: 900px) {
    .case-kpi-grid {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }
}
</style>
""", unsafe_allow_html=True)

df = load_data().copy()

# ── Prep ──────────────────────────────────────────────────────────────────────
for c in ["transfer_spending", "squad_market_value", "points", "position"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

df["spending_m"] = df["transfer_spending"] / 1e6
df["svalue_m"] = df["squad_market_value"] / 1e6
df["league_label"] = df["league"].map(LEAGUE_LABELS).fillna(df["league"])

# max points by league format
df["max_points"] = 114
df.loc[df["league"].astype(str).str.lower().str.contains("bundesliga", na=False), "max_points"] = 102

league_season = (
    df.groupby(["league", "season"], as_index=False)
      .agg(
          league_avg_points=("points", "mean"),
          league_avg_spend=("spending_m", "mean"),
          league_avg_value=("svalue_m", "mean")
      )
)

df = df.merge(league_season, on=["league", "season"], how="left")
df["points_vs_avg"] = df["points"] - df["league_avg_points"]
df["spend_vs_avg_pct"] = ((df["spending_m"] / df["league_avg_spend"]) - 1) * 100
df["value_vs_avg_pct"] = ((df["svalue_m"] / df["league_avg_value"]) - 1) * 100

section_header(
    "Club Case Studies",
    "The Stories Behind the Numbers",
    "Club-level deep-dives into success, failure, and everything in between"
)

featured = {
    "Monaco 2016/17": {
        "club": "Monaco FC",
        "season": "2016/17",
        "tag": "Did more with less",
        "story": "Monaco turned a relatively modest squad into a title-winning side, finishing with 95 of a possible 114 points and breaking PSG’s grip on Ligue 1.",
        "accent": "#00e5cc",
    },
    "Leicester 2015/16": {
        "club": "Leicester City",
        "season": "2015/16",
        "tag": "Broke the pattern",
        "story": "Leicester remains the great outlier: a team built without elite financial power that still went all the way to the title.",
        "accent": "#4da6ff",
    },
    "RB Leipzig 2019/20": {
        "club": "RB Leipzig",
        "season": "2019/20",
        "tag": "Smart model",
        "story": "RB Leipzig showed a different route to success—strong results built on smart recruitment and development rather than simply outspending rivals.",
        "accent": "#34d399",
    },
    "Liverpool 2019/20": {
        "club": "Liverpool",
        "season": "2019/20",
        "tag": "Spent well and delivered",
        "story": "Liverpool turned targeted investment into dominance, converting spending into one of the most decisive title wins in the dataset.",
        "accent": "#a78bfa",
    },
    "Manchester City 2017/18": {
        "club": "Manchester City",
        "season": "2017/18",
        "tag": "Power + payoff",
        "story": "This is what financial power looks like when it works: major investment, a valuable squad, and results that fully matched the bill.",
        "accent": "#4da6ff",
    },
    "Real Madrid 2018/19": {
        "club": "Real Madrid FC",
        "season": "2018/19",
        "tag": "Fell short of expectations",
        "story": "Real Madrid had one of the most valuable squads in the dataset, but results fell well short, making it the clearest underperformance relative to squad value.",
        "accent": "#f7c36a",
    },
    "Chelsea 2022/23": {
        "club": "Chelsea",
        "season": "2022/23",
        "tag": "Spent big and failed",
        "story": "Chelsea spent heavily but finished with only 44 points, turning one of the biggest transfer outlays in the dataset into one of its poorest returns.",
        "accent": "#ff6b9d",
    },
}

def get_case_row(club, season):
    sub = df[(df["club_name"] == club) & (df["season"].astype(str) == str(season))].copy()
    if sub.empty:
        return None
    return sub.iloc[0]

def fmt_money(v):
    if pd.isna(v):
        return "—"
    return f"€{v:,.0f}M"

def fmt_pct(v):
    if pd.isna(v):
        return "—"
    return f"{v:+.0f}%"

def outcome_label(row):
    if row.get("title_won", 0) == 1:
        return "Champions"
    if row.get("top4_finish", 0) == 1:
        return "Top 4"
    if row.get("relegated", 0) == 1:
        return "Relegated"
    if pd.notna(row.get("position")):
        return f"{int(row['position'])}th place"
    return "League finish"

# ── Featured case selector ────────────────────────────────────────────────────
case_choice = st.selectbox("Choose a featured case", list(featured.keys()))
meta = featured[case_choice]
row = get_case_row(meta["club"], meta["season"])

if row is None:
    st.warning(f"{meta['club']} {meta['season']} not found in the dataset.")
else:
    st.markdown(f"""
    <div class="case-card">
        <div style="font-size:0.78rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
            color:{meta['accent']};margin-bottom:8px;">
            {meta['tag']}
        </div>
        <div style="font-size:2rem;font-weight:900;line-height:1.1;color:#fff;margin-bottom:6px;">
            {row["club_name"]} <span style="color:rgba(200,216,240,0.72);font-weight:700;">{row["season"]}</span>
        </div>
        <div style="font-size:1rem;color:rgba(200,216,240,0.80);margin-bottom:8px;">
            {row["league_label"]} • {outcome_label(row)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="case-kpi-grid">
        <div class="case-kpi">
            <div class="case-kpi-label">Points</div>
            <div class="case-kpi-value">{int(row["points"])}/{int(row["max_points"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Position</div>
            <div class="case-kpi-value">{int(row["position"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Squad Value</div>
            <div class="case-kpi-value">{fmt_money(row["svalue_m"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Transfer Spend</div>
            <div class="case-kpi-value">{fmt_money(row["spending_m"])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="story-box" style="border-left-color:{meta['accent']};">
        <div class="story-label">The story</div>
        {meta["story"]}
    </div>
    """, unsafe_allow_html=True)

# ── Explorer ──────────────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
    background:linear-gradient(90deg,#00e5cc,#4da6ff);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:10px;">
    Explore Any Club-Season
</div>
""", unsafe_allow_html=True)

clubs = sorted(df["club_name"].dropna().unique().tolist())
default_club_idx = clubs.index("Chelsea") if "Chelsea" in clubs else 0
club_pick = st.selectbox("Choose a club", clubs, index=default_club_idx)

club_seasons = (
    df[df["club_name"] == club_pick]["season"]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
    .tolist()
)
season_pick = st.selectbox("Choose a season", club_seasons, index=len(club_seasons)-1)

row = get_case_row(club_pick, season_pick)

if row is not None:
    st.markdown(f"""
    <div class="case-card">
        <div style="font-size:1.5rem;font-weight:850;color:#fff;margin-bottom:6px;">
            {row["club_name"]} {row["season"]}
        </div>
        <div style="color:rgba(200,216,240,0.78);margin-bottom:8px;">
            {row["league_label"]} • {outcome_label(row)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="case-kpi-grid">
        <div class="case-kpi">
            <div class="case-kpi-label">Points</div>
            <div class="case-kpi-value">{int(row["points"])}/{int(row["max_points"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Position</div>
            <div class="case-kpi-value">{int(row["position"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Squad Value</div>
            <div class="case-kpi-value">{fmt_money(row["svalue_m"])}</div>
        </div>
        <div class="case-kpi">
            <div class="case-kpi-label">Transfer Spend</div>
            <div class="case-kpi-value">{fmt_money(row["spending_m"])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
