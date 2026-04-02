import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, load_data, section_header, insight, divider,
    flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS
)

st.set_page_config(page_title="Finance vs Performance", page_icon="⚽", layout="wide")
inject_css()

st.markdown("""
<style>
/* Selectbox label */
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] p {
    color: #c8d8f0 !important;
    font-weight: 600 !important;
}

/* Closed select box */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,179,255,0.18) !important;
    border-radius: 10px !important;
    color: #c8d8f0 !important;
}

/* Text shown in closed box */
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #c8d8f0 !important;
}

/* Dropdown menu surface */
div[role="listbox"],
ul[role="listbox"] {
    background: #142a63 !important;
    border: 1px solid rgba(99,179,255,0.18) !important;
}

/* Each option row */
div[role="option"],
li[role="option"] {
    background: #142a63 !important;
    color: #c8d8f0 !important;
}

/* Text inside each option */
div[role="option"] div,
div[role="option"] span,
li[role="option"] div,
li[role="option"] span {
    color: #c8d8f0 !important;
    fill: #c8d8f0 !important;
}

/* Hover / selected */
div[role="option"]:hover,
li[role="option"]:hover {
    background: rgba(77,166,255,0.18) !important;
}

/* Strong fallback for BaseWeb menu portal */
body [data-baseweb="menu"] *,
body ul[role="listbox"] *,
body div[role="listbox"] * {
    color: #c8d8f0 !important;
}
</style>
""", unsafe_allow_html=True)

df = load_data()

section_header(
    "Finance vs Performance",
    "Financial Power & Performance Outcomes",
    "Explore how financial strength relates to on-pitch outcomes across leagues, seasons, and clubs."
)

dff = df.copy()

# ── Plotly scatter ────────────────────────────────────────────────────────────
st.markdown("#### Explore the Data")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    scatter_league = st.selectbox(
        "League",
        ["All"] + list(LEAGUE_LABELS.values())
    )

with col_b:
    scatter_season = st.selectbox(
        "Season",
        ["All"] + sorted(df["season"].unique())
    )

with col_c:
    col_x = st.selectbox(
        "Financial Metric",
        ["svalue_m", "spending_m"],
        format_func=lambda x: "Squad Value (€M)" if x == "svalue_m" else "Transfer Spending (€M)"
    )

with col_d:
    col_y = st.selectbox(
        "Performance Metric",
        ["points", "wins", "goal_difference", "position"],
        format_func=lambda x: {
            "points": "Points",
            "wins": "Wins",
            "goal_difference": "Goal Difference",
            "position": "League Position"
        }[x]
    )

scatter_df = dff.copy()
if scatter_league != "All":
    scatter_df = scatter_df[scatter_df["league_label"] == scatter_league]

if scatter_season != "All":
    scatter_df = scatter_df[scatter_df["season"] == scatter_season]

    season_text = "" if scatter_season == "All" else f" ({scatter_season})"

scatter_title = f"{'Squad Value' if col_x == 'svalue_m' else 'Transfer Spending'} vs {col_y.replace('_', ' ').title()}"

if scatter_league == "All":
    fig_sc = px.scatter(
        scatter_df,
        x=col_x,
        y=col_y,
        color="league",
        color_discrete_map=LEAGUE_COLORS,
        hover_data=["club_name", "season", "league"],
        trendline="ols",
        labels={
            col_x: "Squad Value (€M)" if col_x == "svalue_m" else "Transfer Spending (€M)",
            col_y: col_y.replace("_", " ").title()
        },
        title=scatter_title
    )
    fig_sc.update_layout(showlegend=True)
else:
    league_key = next((k for k, v in LEAGUE_LABELS.items() if v == scatter_league), None)
    single_color = LEAGUE_COLORS.get(league_key, "#00e5cc")

    fig_sc = px.scatter(
        scatter_df,
        x=col_x,
        y=col_y,
        hover_data=["club_name", "season", "league"],
        trendline="ols",
        labels={
            col_x: "Squad Value (€M)" if col_x == "svalue_m" else "Transfer Spending (€M)",
            col_y: col_y.replace("_", " ").title()
        },
        title=scatter_title
    )
    fig_sc.update_traces(marker=dict(color=single_color))
    fig_sc.update_layout(showlegend=False)

apply_template(fig_sc)
fig_sc.update_traces(marker=dict(size=7, opacity=0.75))
st.plotly_chart(fig_sc, use_container_width=True)

divider()

# ── Correlation heatmap ───────────────────────────────────────────────────────
st.markdown("#### Correlation Matrix - Finance & Performance")
corr_cols = [
    "squad_market_value", "transfer_spending", "points", "wins",
    "goals_for", "goal_difference", "position"
]
corr = dff[corr_cols].corr().round(2)

fig_heat = go.Figure(go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale=[[0, "#1246c4"], [0.5, "#0a0e1a"], [1, "#00e5cc"]],
    zmid=0,
    text=corr.values,
    texttemplate="%{text}",
    showscale=True,
))
fig_heat.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#c8d8f0"),
    margin=dict(t=20, b=20, l=20, r=20),
    height=420,
)
st.plotly_chart(fig_heat, use_container_width=True)
insight("Squad value has the strongest correlation with points (~0.63) and wins. Transfer spending alone is a weaker predictor (~0.44).")

divider()

# ── Correlation by league ─────────────────────────────────────────────────────
st.markdown("#### How Important is Finance in Each League?")
corr_league = df.groupby("league").apply(
    lambda x: pd.Series({
        "Squad Value vs Points": x["squad_market_value"].corr(x["points"]).round(3),
        "Transfer Spend vs Points": x["transfer_spending"].corr(x["points"]).round(3),
    })
).reset_index()

corr_league["label"] = corr_league["league"].map(LEAGUE_LABELS)
corr_melt = corr_league.melt(
    id_vars=["league", "label"],
    var_name="Metric",
    value_name="Correlation"
)

# Sort leagues by strongest correlation (Squad Value vs Points)
order = (
    corr_league.sort_values("Squad Value vs Points", ascending=False)["label"]
    .tolist()
)

fig_corr = px.bar(
    corr_melt,
    x="label",
    y="Correlation",
    category_orders={"label": order},
    color="Metric",
    barmode="group",
    color_discrete_sequence=["#00e5cc", "#4da6ff"],
    labels={"label": " ", "Correlation": "Correlation"},
    title="Correlation Between Finance and Points by League"
)
apply_template(fig_corr)
st.plotly_chart(fig_corr, use_container_width=True)
insight("Serie A shows the strongest squad-value-to-points relationship (~0.74), while the La Liga Bundesliga’s weaker link suggests a more balanced competition where financial advantage translates less directly into results")