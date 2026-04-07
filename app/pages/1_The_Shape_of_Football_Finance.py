import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import (inject_css, load_data, section_header, insight, divider,
                   flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS)

st.set_page_config(page_title="The Shape of Football Finance", page_icon="💰", layout="wide")
inject_css()

st.markdown("""
<style>
/* Label */
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

/* Text inside each option — this is the part your current CSS misses */
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

/* High-specificity fallback for BaseWeb-rendered menu items */
body [data-baseweb="menu"] * {
    color: #0a0e1a !important;
},
body ul[role="listbox"] *,
body div[role="listbox"] * {
    color: #c8d8f0 !important;
}
</style>
""", unsafe_allow_html=True)

df = load_data()

section_header("The Overview", "The Shape of Football Finance",
               "A small group of clubs dominate football’s wealth")

# ── Distributions ─────────────────────────────────────────────────────────────
st.markdown("#### Distribution of Squad Market Value & Transfer Spending")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df,
        x="svalue_m",
        nbins=40,
        color_discrete_sequence=["#4da6ff"],
        labels={"svalue_m": "Squad Value (€M)"},
        title="Squad Market Value Distribution"
    )
    fig1.update_traces(opacity=0.8)
    apply_template(fig1)
    # 🔑 FORCE axis + color AFTER template
    fig1.layout.yaxis.title.text = "No. of Teams"
    fig1.update_traces(marker=dict(color="#4da6ff"))
    st.plotly_chart(fig1, use_container_width=True)
    insight("61% of clubs fall under €500M; a small cluster of clubs account for much higher values.")

with col2:
    fig2 = px.histogram(
        df[df["spending_m"] > 0],
        x="spending_m",
        nbins=40,
        color_discrete_sequence=["#00e5cc"],
        labels={"spending_m": "Transfer Spending (€M)"},
        title="Transfer Spending Distribution"
    )
    fig2.update_traces(opacity=0.8)
    apply_template(fig2)
    # 🔑 FORCE axis + color AFTER template
    fig2.layout.yaxis.title.text = "No. of Teams"
    fig2.update_traces(marker=dict(color="#00e5cc"))
    st.plotly_chart(fig2, use_container_width=True)
    insight("About 90% spend below €100M; a small number of clubs spend heavily.")

divider()

# ── Box plots by league ───────────────────────────────────────────────────────
st.markdown("#### Squad Value &  Spending by League")
tab1, tab2 = st.tabs(["🏟️ Squad Value", "💰 Transfer Spending"])

league_color_map = {v: LEAGUE_COLORS[k] for k, v in LEAGUE_LABELS.items()}

with tab1:
    fig4 = px.box(
        df,
        y="league_label",
        x="svalue_m",
        color="league",
        color_discrete_map=LEAGUE_COLORS,
        orientation="h",
        labels={"svalue_m": "Squad Value (€M)", "league_label": " "},
        title="Squad Value Distribution by League"
    )
    apply_template(fig4)
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    insight("Premier League squads are worth nearly 2× La Liga on average, reflecting their TV revenue dominance.")

with tab2:
    fig3 = px.box(
        df,
        y="league_label",
        x="spending_m",
        color="league",
        color_discrete_map=LEAGUE_COLORS,
        orientation="h",
        labels={"spending_m": "Transfer Spend (€M)", "league_label": " "},
        title="Transfer Spending Distribution by League"
    )
    apply_template(fig3)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    insight("The Premier League spends over 3× the Bundesliga on average, while Ligue 1 shows extreme inequality driven by PSG.")

divider()

# ── Time trend ────────────────────────────────────────────────────────────────
st.markdown("#### Financial Growth Over Time")
metric_choice = st.selectbox("Select metric", ["Squad Value (€M)", "Transfer Spending (€M)"])
col_map = {"Squad Value (€M)": "svalue_m", "Transfer Spending (€M)": "spending_m"}
col = col_map[metric_choice]

trend = df.groupby(["year","league"])[col].mean().reset_index()
trend["league_label"] = trend["league"].map(LEAGUE_LABELS)

fig5 = px.line(trend, x="year", y=col, color="league",
               color_discrete_map=LEAGUE_COLORS,
               labels={"year":" ", col: metric_choice},
               title=f"Average {metric_choice} by League Over Time",
               markers=True)
apply_template(fig5)
fig5.update_traces(line_width=2.5)
st.plotly_chart(fig5, use_container_width=True)
insight("Squad values have inflated 2–3× across all leagues since 2014. The Premier League gap has widened every season.")

divider()

# ── Financial inequality ──────────────────────────────────────────────────────
st.markdown("#### Financial Inequality")
tab1, tab2 = st.tabs(["🏟️ Squad Value", "💰 Transfer Spending"])

with tab1:
    cv_sv = (df.groupby("league")["svalue_m"].std() /
             df.groupby("league")["svalue_m"].mean()).reset_index()
    cv_sv.columns = ["league", "cv"]
    cv_sv = cv_sv.sort_values("cv", ascending=True)
    cv_sv["label"] = cv_sv["league"].map(LEAGUE_LABELS)
    cv_sv["color"] = cv_sv["league"].map(LEAGUE_COLORS)

    fig6a = go.Figure(go.Bar(
        x=cv_sv["cv"].round(2),
        y=cv_sv["label"],
        orientation="h",
        marker_color=cv_sv["color"].tolist(),
        text=cv_sv["cv"].round(2),
        textposition="outside",
    ))

    apply_template(fig6a)
    fig6a.update_layout(
        title=dict(
            text="Squad Value Inequality by League (Higher = More Unequal)",
            font=dict(color="#eaf2ff", size=20)
        ),
        xaxis=dict(title="Coefficient of Variation"),
        yaxis=dict(linecolor="rgba(99,179,255,0.2)"),
        margin=dict(t=40, b=20, l=20, r=60),
        height=320,
        showlegend=False,
    )

    st.plotly_chart(fig6a, use_container_width=True)
    insight("Ligue 1 is the most unequal, with PSG far ahead, while the Premier League is the most evenly distributed.")

with tab2:
    cv_ts = (df.groupby("league")["transfer_spending"].std() /
             df.groupby("league")["transfer_spending"].mean()).reset_index()
    cv_ts.columns = ["league", "cv"]
    cv_ts = cv_ts.sort_values("cv", ascending=True)
    cv_ts["label"] = cv_ts["league"].map(LEAGUE_LABELS)
    cv_ts["color"] = cv_ts["league"].map(LEAGUE_COLORS)

    fig6b = go.Figure(go.Bar(
        x=cv_ts["cv"].round(2),
        y=cv_ts["label"],
        orientation="h",
        marker_color=cv_ts["color"].tolist(),
        text=cv_ts["cv"].round(2),
        textposition="outside",
    ))

    apply_template(fig6b)
    fig6b.update_layout(
        title=dict(
            text="Transfer Spending Inequality by League (Higher = More Unequal)",
            font=dict(color="#eaf2ff", size=20)
        ),
        xaxis=dict(title="Coefficient of Variation"),
        yaxis=dict(linecolor="rgba(99,179,255,0.2)"),
        margin=dict(t=40, b=20, l=20, r=60),
        height=320,
        showlegend=False,
    )

    st.plotly_chart(fig6b, use_container_width=True)
    insight("Ligue 1 is the most financially unequal league - PSG's dominance distorts the entire competition. The Premier League is ironically the most equal despite its size.")