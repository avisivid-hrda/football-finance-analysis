import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (inject_css, load_data, section_header, insight, divider,
                   flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS)

st.set_page_config(page_title="Chasing Glory", page_icon="⚽", layout="wide")
inject_css()

st.markdown("""
<style>
/* Tab row */
div[data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid rgba(99,179,255,0.18);
    padding-bottom: 6px;
}

/* Individual tabs */
button[data-baseweb="tab"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,179,255,0.14) !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 18px !important;
    color: #c8d8f0 !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

/* Kill Streamlit default highlight lines */
button[data-baseweb="tab"]::before,
button[data-baseweb="tab"]::after {
    display: none !important;
    content: none !important;
}

button[data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
    color: inherit !important;
    font-size: 1rem !important;
}

/* Active tab */
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(99,179,255,0.28) !important;
    color: #ffffff !important;
    box-shadow: inset 0 -3px 0 #00e5cc !important;
}

/* Remove any red bottom border from tab highlight wrappers */
div[data-baseweb="tab-highlight"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

df = load_data()

# Pre-compute buckets
df["spending_bucket"] = pd.cut(df["spending_rank"],
    bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])
df["value_bucket"] = pd.cut(df["value_rank"],
    bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])

section_header("Titles, Top 4 & Relegation", "Chasing Glory",
               "Not everyone can afford the finish line")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏆 Title Winners", "⭐ Top 4 (UCL)", "⬇️ Relegation"])

# ── TAB 1: Titles ─────────────────────────────────────────────────────────────
with tab1:
    title_df = df[df["title_won"] == 1]
    spend_dist = title_df["spending_rank"].value_counts().reset_index()
    spend_dist.columns = ["Spending Rank","Count"]
    spend_dist["Rank Group"] = spend_dist["Spending Rank"].apply(
        lambda x: "Rank 1" if x==1 else ("Top 3" if x<=3 else ("Top 6" if x<=6 else "7+"))
    )
    group_agg = spend_dist.groupby("Rank Group")["Count"].sum().reset_index()
    order = ["Rank 1","Top 3","Top 6","7+"]
    group_agg["Rank Group"] = pd.Categorical(group_agg["Rank Group"], categories=order, ordered=True)
    group_agg = group_agg.sort_values("Rank Group")

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = go.Figure(go.Pie(
            labels=group_agg["Rank Group"], values=group_agg["Count"],
            marker_colors=["#00e5cc","#4da6ff","#a78bfa","#f7c36a"],
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(color="#ffffff", size=13),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#c8d8f0"),
            title=dict(
                text="Title Wins by Spending Rank Group",
                font=dict(color="white", size=20)
    ),
        margin=dict(t=70, b=20, l=20, r=40),
        height=430,
        showlegend=False,
    )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        win_rate = df.groupby("spending_rank").agg(
            titles=("title_won","sum"), total=("title_won","count"),
        ).reset_index()
        win_rate["win_rate"] = (win_rate["titles"] / win_rate["total"] * 100).round(1)
        win_rate = win_rate[win_rate["spending_rank"] <= 10]

        fig_wr = go.Figure(go.Bar(
            x=win_rate["spending_rank"], y=win_rate["win_rate"],
            marker_color=["#00e5cc" if r<=3 else "#4da6ff" if r<=6 else "#a78bfa" for r in win_rate["spending_rank"]],
            text=win_rate["win_rate"].apply(lambda x: f"{x}%"), textposition="outside",
        ))
        fig_wr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Inter",color="#c8d8f0"),
            xaxis=dict(title="Spending Rank", dtick=1, gridcolor="rgba(99,179,255,0.1)"),
            yaxis=dict(title="Title Win Rate (%)", gridcolor="rgba(99,179,255,0.1)"),
            margin=dict(t=70, b=20, l=20, r=40), height=430, showlegend=False,
            title=dict(
                text="Title Win Rate by Spending Rank",
                font=dict(color="white", size=20)
            )
        )
        st.plotly_chart(fig_wr, use_container_width=True)

    insight("The highest-spending team each season won 30% of titles (vs 5% by chance). Yet 70% of titles were won outside the top spender, proving money helps but doesn't guarantee.")

# ── TAB 2: Top 4 ──────────────────────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        top4_spend = df.groupby("spending_bucket", observed=True)["top4_finish"].mean().reset_index()
        top4_spend["rate"] = (top4_spend["top4_finish"] * 100).round(1)
        fig_t4s = px.bar(top4_spend, x="spending_bucket", y="rate",
                         color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#00e5cc"]],
                         labels={"spending_bucket":"Spending Rank Bucket","rate":"Top 4 Rate (%)"},
                         title="Top 4 Finish Rate by Transfer Spending Rank")
        apply_template(fig_t4s)
        fig_t4s.update_layout(showlegend=False, coloraxis_showscale=False)
        fig_t4s.update_traces(text=top4_spend["rate"].apply(lambda x: f"{x}%"), textposition="outside")
        fig_t4s.update_layout(
            margin=dict(t=80, b=20, l=20, r=20),
            height=430
        )
        fig_t4s.update_yaxes(range=[0, top4_spend["rate"].max() + 8])
        st.plotly_chart(fig_t4s, use_container_width=True)

    with col2:
        top4_val = df.groupby("value_bucket", observed=True)["top4_finish"].mean().reset_index()
        top4_val["rate"] = (top4_val["top4_finish"] * 100).round(1)
        fig_t4v = px.bar(top4_val, x="value_bucket", y="rate",
                         color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#4da6ff"]],
                         labels={"value_bucket":"Squad Value Rank Bucket","rate":"Top 4 Rate (%)"},
                         title="Top 4 Finish Rate by Squad Value Rank")
        apply_template(fig_t4v)
        fig_t4v.update_layout(showlegend=False, coloraxis_showscale=False)
        fig_t4v.update_traces(text=top4_val["rate"].apply(lambda x: f"{x}%"), textposition="outside")
        fig_t4v.update_layout(
        margin=dict(t=80, b=20, l=20, r=20),
        height=430
        )
        fig_t4v.update_yaxes(range=[0, top4_val["rate"].max() + 8])
        st.plotly_chart(fig_t4v, use_container_width=True)

    insight("Top 3 spenders finish in the Champions League places ~70–80% of the time. Beyond the top 6, the drop-off is steep - mid-table spenders rarely qualify.")

# ── TAB 3: Relegation ─────────────────────────────────────────────────────────
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        rel_spend = df.groupby("spending_bucket", observed=True)["relegated"].mean().reset_index()
        rel_spend["rate"] = (rel_spend["relegated"] * 100).round(1)
        fig_rs = px.bar(rel_spend, x="spending_bucket", y="rate",
                        color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#ff6b9d"]],
                        labels={"spending_bucket":"Spending Rank Bucket","rate":"Relegation Rate (%)"},
                        title="Relegation Rate by Transfer Spending Rank")
        apply_template(fig_rs)
        fig_rs.update_layout(showlegend=False, coloraxis_showscale=False)
        fig_rs.update_traces(text=rel_spend["rate"].apply(lambda x: f"{x}%"), textposition="outside")
        fig_rs.update_layout(
        margin=dict(t=80, b=20, l=20, r=20),
        height=430
        )
        fig_rs.update_yaxes(range=[0, rel_spend["rate"].max() + 8])
        st.plotly_chart(fig_rs, use_container_width=True)

    with col2:
        rel_val = df.groupby("value_bucket", observed=True)["relegated"].mean().reset_index()
        rel_val["rate"] = (rel_val["relegated"] * 100).round(1)
        fig_rv = px.bar(rel_val, x="value_bucket", y="rate",
                        color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#f7c36a"]],
                        labels={"value_bucket":"Squad Value Rank Bucket","rate":"Relegation Rate (%)"},
                        title="Relegation Rate by Squad Value Rank")
        apply_template(fig_rv)
        fig_rv.update_layout(showlegend=False, coloraxis_showscale=False)
        fig_rv.update_traces(text=rel_val["rate"].apply(lambda x: f"{x}%"), textposition="outside")
        fig_rv.update_layout(
        margin=dict(t=80, b=20, l=20, r=20),
        height=430
        )
        fig_rv.update_yaxes(range=[0, rel_val["rate"].max() + 8])
        st.plotly_chart(fig_rv, use_container_width=True)
    insight("No club ranked in the top 3 by squad value has ever been relegated in this dataset. Bottom 5 spenders face dramatically higher relegation risk. Financial weakness directly threatens survival.")