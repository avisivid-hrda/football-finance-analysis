import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import (inject_css, load_data, compute_residuals, section_header,
                   insight, divider, flourish_embed, apply_template, LEAGUE_COLORS)

st.set_page_config(page_title="Overperformers", page_icon="⚽", layout="wide")
inject_css()

df = load_data()
dres = compute_residuals(df)

section_header("Overperformers & Underperformers", "Performance Exceeding vs Missing Expectations",
               "Residual analysis - comparing actual points to what a club's squad value predicted.")

# ── Residual basis selector ───────────────────────────────────────────────────
residual_basis = st.radio("Residual Basis", ["Squad Value", "Transfer Spending"], horizontal=True)
res_col = "residual" if residual_basis == "Squad Value" else "residual_spend"
pred_col = "predicted_points" if residual_basis == "Squad Value" else "pred_pts_spend"
sub = dres.dropna(subset=[res_col])

# ── Over / Under performers ───────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🚀 Top 10 Overperformers")
    top_over = sub.nlargest(10, res_col)[["club_name","league","season","points", res_col]].copy()
    top_over[res_col] = top_over[res_col].round(1)
    top_over["label"] = top_over["club_name"] + "\n" + top_over["season"]

    fig_ov = go.Figure(go.Bar(
        x=top_over[res_col], y=top_over["label"],
        orientation="h", marker_color="#00e5cc",
        text=top_over[res_col].apply(lambda x: f"+{x}"), textposition="outside",
    ))
    fig_ov.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title="Points above expectation"),
        yaxis=dict(autorange="reversed"),
        margin=dict(t=10,b=20,l=20,r=60), height=400, showlegend=False,
    )
    st.plotly_chart(fig_ov, use_container_width=True)

with col2:
    st.markdown("##### 💸 Top 10 Underperformers")
    top_under = sub.nsmallest(10, res_col)[["club_name","league","season","points", res_col]].copy()
    top_under[res_col] = top_under[res_col].round(1)
    top_under["label"] = top_under["club_name"] + "\n" + top_under["season"]

    fig_un = go.Figure(go.Bar(
        x=top_under[res_col], y=top_under["label"],
        orientation="h", marker_color="#ff6b9d",
        text=top_under[res_col], textposition="outside",
    ))
    fig_un.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title="Points below expectation"),
        yaxis=dict(autorange="reversed"),
        margin=dict(t=10,b=20,l=20,r=60), height=400, showlegend=False,
    )
    st.plotly_chart(fig_un, use_container_width=True)

col1i, col2i = st.columns(2)
with col1i:
    insight("Monaco 2016/17 - won Ligue 1 with 95 points despite a modest squad value. The 'Mbappé/Lemar generation' before the selloff.")
with col2i:
    insight("Chelsea 2022/23 - worst underperformer: €574M spent, only 44 pts. The most extreme waste of resources in the entire dataset.")

divider()

# ── Middle East ownership ─────────────────────────────────────────────────────
st.markdown("#### 🏦 Middle East Owned Clubs - Performance vs Expectations Over Time")
me = dres[dres["middle_east_owned"] == 1].sort_values("year")

fig_me = px.line(me, x="year", y=res_col, color="club_name",
                 color_discrete_sequence=["#00e5cc","#4da6ff","#f7c36a"],
                 markers=True,
                 labels={"year":"Year", res_col:"Residual (Actual − Predicted Points)", "club_name":"Club"},
                 title="Residual Points - Middle East Owned Clubs")
apply_template(fig_me)
fig_me.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Expected")
fig_me.update_traces(line_width=2.5)
st.plotly_chart(fig_me, use_container_width=True)
insight("Man City and PSG initially overperformed heavily. As their squads became the most expensive in their leagues, their residuals converged to zero. Great performance now simply meets inflated expectations.")