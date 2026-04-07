import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import (inject_css, load_data, section_header, insight, divider,
                   flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS)

st.set_page_config(page_title="Returns on the Pitch", page_icon="🚀", layout="wide")
inject_css()

df = load_data()

section_header("Efficiency Analysis", "Returns on the Pitch",
               "Some clubs buy success; others just buy players")

# ── Metric selector ───────────────────────────────────────────────────────────
metric = st.radio("Efficiency Metric",
                  ["Points per €100M Squad Value", "Points per €10M Transfer Spend"],
                  horizontal=True)

if metric == "Points per €100M Squad Value":
    eff_df = df[df["squad_market_value"] >= 100_000_000].copy()
    eff_df["efficiency"] = eff_df["points"] / (eff_df["squad_market_value"] / 1e8)
    xlabel = "Points per €100M Squad Value"
else:
    eff_df = df[df["transfer_spending"] >= 10_000_000].copy()
    eff_df["efficiency"] = eff_df["points"] / (eff_df["transfer_spending"] / 1e7)
    xlabel = "Points per €10M Transfer Spend"

# ── Top / Bottom 15 ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

insight("Smaller, well-organised clubs consistently outperform on efficiency. RB Leipzig 🇩🇪 and Sassuolo 🇮🇹 regularly appear as best-value clubs in their respective leagues.")

with col1:
    st.markdown("##### 🏅 Top 15 Most Efficient Clubs")
    top_eff = eff_df.nlargest(15, "efficiency").copy()
    top_eff["label"] = top_eff["club_name"] + "  " + top_eff["season"]
    top_eff["efficiency"] = top_eff["efficiency"].round(2)

    fig_top = go.Figure(go.Bar(
        x=top_eff["efficiency"], y=top_eff["label"],
        orientation="h", marker_color="#00e5cc",
        text=top_eff["efficiency"], textposition="outside",
    ))
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title=xlabel),
        yaxis=dict(autorange="reversed"),
        margin=dict(t=10,b=20,l=20,r=60), height=500, showlegend=False,
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    st.markdown(f"##### ⬇️ 15 Least Efficient Clubs")
    bot_eff = eff_df.nsmallest(15, "efficiency").copy()
    bot_eff = bot_eff.sort_values("efficiency", ascending=True)
    bot_eff["label"] = bot_eff["club_name"] + "  " + bot_eff["season"]
    bot_eff["efficiency"] = bot_eff["efficiency"].round(2)

    fig_bot = go.Figure(go.Bar(
        x=bot_eff["efficiency"], y=bot_eff["label"],
        orientation="h", marker_color="#ff6b9d",
        text=bot_eff["efficiency"], textposition="outside",
    ))
    fig_bot.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title=xlabel),
        margin=dict(t=10, b=20, l=20, r=60), height=500, showlegend=False,
    )
    st.plotly_chart(fig_bot, use_container_width=True)


divider()

# ── Efficiency by league ──────────────────────────────────────────────────────
st.markdown("#### Efficiency across Leagues")
dist_metric = st.radio(
    "Select efficiency basis",
    ["Squad Value", "Transfer Spending"],
    horizontal=True
)
if dist_metric == "Squad Value":
    dist_df = df[df["squad_market_value"] >= 100_000_000].copy()
    dist_df["efficiency"] = dist_df["points"] / (dist_df["squad_market_value"] / 1e8)
    xlabel = "Points per €100M Squad Value"
else:
    dist_df = df[df["transfer_spending"] >= 10_000_000].copy()
    dist_df["efficiency"] = dist_df["points"] / (dist_df["transfer_spending"] / 1e7)
    xlabel = "Points per €10M Transfer Spend"
fig_box = px.box(
    dist_df,
    y="league_label",          
    x="efficiency",            
    color="league",
    color_discrete_map=LEAGUE_COLORS,
    orientation="h",           
    labels={"efficiency": xlabel, "league_label": " "},
    title=f"{xlabel} — Distribution by League"
)
apply_template(fig_box)
fig_box.update_layout(showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)
insight("In La Liga and Ligue 1, the gap between smart and wasteful spending is wide; in Premier League, bigger budgets rarely translate into better value.")