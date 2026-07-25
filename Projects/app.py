import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.categorize import classify_dataframe
from src.metrics import wasted_spend_total, spend_by_category, waste_pct_of_income, months_to_goal

st.set_page_config(page_title="Ryan's Spending Insights", layout="wide", page_icon="💰")

DELOITTE_GREEN = "#86BC25"
DELOITTE_DARK = "#53565A"
DELOITTE_GREY = "#9A9A9A"

st.markdown(f"""
    <style>
    div[data-testid="stMetric"] {{
        background-color: #1C1F26;
        border-left: 6px solid {DELOITTE_GREEN};
        border-radius: 8px;
        padding: 15px 10px;
    }}
    div[data-testid="stMetricLabel"] {{
        color: #FFFFFF;
        font-weight: 600;
    }}
    div[data-testid="stMetricValue"] {{
        color: {DELOITTE_GREEN};
    }}
    h1, h2, h3 {{
        color: #FFFFFF;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("Personal Spending Intelligence Dashboard")
st.caption("May 2026 Spending Analysis — Ryan D'Souza, TD Chequing")

df = pd.read_csv("data/ryan_dsouza_may2026_TD_statement.csv")
df = classify_dataframe(df)
df["category"] = df["category"].replace("fee", "wasteful")
df.loc[df["Description"].str.contains("ROGERS", na=False), "category"] = "essential"
df["Date"] = pd.to_datetime(df["Date"])
df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0)

st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Category", options=df["category"].unique(), default=df["category"].unique()
)
date_range = st.sidebar.date_input("Date range", [df["Date"].min(), df["Date"].max()])
filtered = df[
    (df["category"].isin(categories)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
].copy()

wasteful_total = filtered[filtered["category"] == "wasteful"]["Debit"].sum()
unclear_cash_total = filtered[filtered["category"] == "unclear_cash"]["Debit"].sum()
total_waste = wasteful_total + unclear_cash_total

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Confirmed Wasteful Spend",
    f"${wasteful_total:,.2f}",
    help="Sum of spending on low-value subscriptions (GoodLife, LinkedIn Premium, Crave TV, Disney Plus, Amazon Prime) plus the overdraft fee. Calculated by filtering all transactions tagged 'wasteful' and summing the Debit column."
)

col2.metric(
    "Unclear Cash Withdrawals",
    f"${unclear_cash_total:,.2f}",
    help="Total ATM withdrawals for the month where the spending purpose can't be traced. Calculated by summing all Debit amounts for transactions tagged 'unclear_cash' (ABM withdrawals)."
)

col3.metric(
    "% of Take-Home Pay",
    f"{waste_pct_of_income(filtered)}%",
    help="Confirmed wasteful spend plus unclear cash, divided by total monthly take-home income ($3,950), multiplied by 100. Shows what share of Ryan's paycheque is lost to waste or untracked cash."
)

col4.metric(
    "Months to $3,000 Goal",
    months_to_goal(total_waste),
    help="Assumes Ryan redirects his combined wasteful spend and unclear cash into savings every month. Calculated as $3,000 divided by that monthly total."
)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Trends Over Time", "Savings Projection", "Flagged Transactions", "Raw Data"]
)

custom_colors = [DELOITTE_GREEN, DELOITTE_DARK, DELOITTE_GREY, "#C4D600", "#0076A8", "#43B02A"]

with tab1:
    left, right = st.columns(2)

    with right:
        filtered_pie = filtered.copy()
        filtered_pie["category"] = filtered_pie["category"].replace("fee", "wasteful")
        filtered_pie = filtered_pie[filtered_pie["category"] != "income"]

        cat_totals = filtered_pie.groupby("category")["Debit"].sum().reset_index()
        cat_totals = cat_totals.sort_values("Debit", ascending=False)

        fig_pie = px.pie(
            cat_totals, names="category", values="Debit",
            title="Spend Breakdown by Category",
            hole=0.4,
            category_orders={"category": cat_totals["category"].tolist()},
            color="category",
            color_discrete_map={
                "discretionary": DELOITTE_GREEN,
                "essential": "#4A4E57",
                "unclear_cash": "#A9A9A9",
                "wasteful": "#D4E600",
                "essential_sub": "#3CA55C",
            }
        )
        fig_pie.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="#FFFFFF",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with left:
        filtered_bar = filtered.copy()
        filtered_bar["category"] = filtered_bar["category"].replace("fee", "wasteful")

        category_totals = filtered_bar.groupby("category", as_index=False)["Debit"].sum()
        category_totals = category_totals[category_totals["category"] != "income"]
        category_totals = category_totals.sort_values("Debit", ascending=False)

        fig = px.bar(
            category_totals,
            x="category",
            y="Debit",
            color="category",
            title="Total Spend by Category",
            category_orders={"category": category_totals["category"].tolist()},
            color_discrete_map={
                "discretionary": DELOITTE_GREEN,
                "essential": "#4A4E57",
                "unclear_cash": "#A9A9A9",
                "wasteful": "#D4E600",
                "essential_sub": "#3CA55C",
            }
        )
        fig.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="#FFFFFF",
        )

        selected = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            key="category_bar_chart"
        )

        if selected and selected.get("selection") and selected["selection"].get("points"):
            clicked_category = selected["selection"]["points"][0]["x"]
            st.subheader(f"Transactions in: {clicked_category}")

            drilldown_df = filtered.copy()
            drilldown_df["category"] = drilldown_df["category"].replace("fee", "wasteful")
            filtered_df = drilldown_df[drilldown_df["category"] == clicked_category]

            st.dataframe(
                filtered_df[["Date", "Description", "Debit", "Credit", "category"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Click a bar above to see the transactions in that category.")

with tab2:
    daily = filtered.groupby("Date")["Debit"].sum().reset_index()
    daily["Balance"] = filtered.groupby("Date")["Balance"].last().values

    fig_line = px.line(daily, x="Date", y="Balance", title="Ryan's Balance Over the Month", markers=True,
                        color_discrete_sequence=[DELOITTE_GREEN])
    fig_line.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Overdraft Line")
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Daily Spending (click a bar to see that day's transactions)")

    fig_daily_spend = px.bar(daily, x="Date", y="Debit", title="Daily Spending",
                              color_discrete_sequence=[DELOITTE_GREEN])
    fig_daily_spend.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="#FFFFFF",
        title_font_size=20,
    )

    event = st.plotly_chart(fig_daily_spend, use_container_width=True, on_select="rerun", key="daily_chart")

    if event and event.selection and event.selection.points:
        clicked_x = event.selection.points[0]["x"]
        clicked_date = pd.to_datetime(clicked_x)
        st.success(f"Showing transactions for {clicked_date.strftime('%B %d, %Y')}")
        day_transactions = filtered[filtered["Date"] == clicked_date]
        st.dataframe(day_transactions[["Date", "Description", "Debit", "category"]], use_container_width=True)
    else:
        st.info("Click any bar above to drill into that day's transactions.")

with tab3:

    st.subheader("Projected Emergency Fund Growth")
    months = np.arange(0, 7)
    monthly_saving = total_waste if total_waste > 0 else 1
    projected = monthly_saving * months
    fig_savings = px.line(x=months, y=projected, labels={"x": "Months", "y": "Savings ($)"},
                           title="Path to Ryan's $3,000 Goal", markers=True,
                           color_discrete_sequence=[DELOITTE_GREEN])
    fig_savings.add_hline(y=3000, line_dash="dash", line_color="#0076A8", annotation_text="$3,000 Goal")
    st.plotly_chart(fig_savings, use_container_width=True)

    goal_months = months_to_goal(total_waste)
    if goal_months:
        st.success(f"If Ryan redirects his wasted spend, he reaches his $3,000 goal in approximately {goal_months} months.")

    st.caption(
        f"Calculation: monthly savings = confirmed wasteful spend (${wasteful_total:,.2f}) + unclear cash withdrawals "
        f"(${unclear_cash_total:,.2f}) = ${total_waste:,.2f} per month. Months to goal = $3,000 ÷ ${total_waste:,.2f} "
        f"= {goal_months} months. This projection assumes Ryan redirects the full amount every month with no interest, "
        f"no other spending changes, and doesn't yet account for his negative ending balance in May."
    )

with tab4:
    st.subheader("Flagged Waste and Unclear Cash")
    flagged = filtered.copy()
    flagged["category"] = flagged["category"].replace("fee", "wasteful")
    flagged = flagged[flagged["category"].isin(["wasteful", "unclear_cash"])]
    st.dataframe(flagged, use_container_width=True)

with tab5:
    st.subheader("All Transactions")
    st.dataframe(filtered, use_container_width=True)
