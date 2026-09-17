import pandas as pd
from pathlib import Path

# -----------------------------
# Dataset supplied by the user
# -----------------------------
data = [
    ["FizzyCo",1197831,"25-08-2023","South","Alabama","Birmingham","Coca-Cola",0.07,2240,157,74,47],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Sprite",0.07,1050,74,31,42],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Fanta",0.07,1110,78,36,46],
    ["West Soda",1197831,"19-03-2023","South","Oklahoma","Oklahoma City","Sprite",0.07,830,58,26,45],
    ["Walmart",1197831,"19-03-2023","South","Arkansas","Little Rock","Sprite",0.08,1120,90,40,45],
    ["FizzyCo",1197831,"25-08-2023","South","Alabama","Birmingham","Coca-Cola",0.09,2030,183,108,59],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Sprite",0.09,910,82,41,50],
    ["West Soda",1197831,"19-03-2023","South","Oklahoma","Oklahoma City","Sprite",0.09,800,72,36,50],
    ["Target",1197831,"12-03-2023","Midwest","Kansas","Wichita","Sprite",0.09,750,68,31,46],
    ["BevCo",1185732,"05-03-2023","Midwest","Iowa","Des Moines","Sprite",0.09,650,59,23,40],
    ["West Soda",1185732,"02-03-2023","Midwest","Wisconsin","Milwaukee","Sprite",0.09,590,53,23,44],
    ["West Soda",1185732,"03-04-2023","Midwest","Wisconsin","Milwaukee","Sprite",0.09,410,37,16,43],
    ["FizzyCo",1197831,"25-08-2023","South","Alabama","Birmingham","Coca-Cola",0.10,7000,700,315,45],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Fanta",0.10,880,88,45,51],
    ["Walmart",1197831,"19-03-2023","South","Arkansas","Little Rock","Sprite",0.10,880,88,48,54],
    ["BevCo",1185732,"06-04-2023","Midwest","Iowa","Des Moines","Sprite",0.10,530,53,23,44],
    ["West Soda",1185732,"11-04-2023","West","Utah","Salt Lake City","Sprite",0.10,1070,107,44,41],
    ["West Soda",1197831,"23-01-2023","South","Arkansas","Little Rock","Sprite",0.10,1310,131,56,43],
    ["West Soda",1197831,"20-04-2023","South","Oklahoma","Oklahoma City","Sprite",0.10,700,70,32,46],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Sprite",0.10,3500,350,123,35],
    ["West Soda",1185732,"12-09-2023","West","Utah","Salt Lake City","Fanta",0.10,3250,325,130,40],
]
cols = [
    "Retailer","Retailer ID","Invoice Date","Region","State","City",
    "Beverage Brand","Price per Unit","Units Sold","Total Sales",
    "Operating Profit","Operating Margin"
]
df = pd.DataFrame(data, columns=cols)
df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], dayfirst=True)
df["Year"] = df["Invoice Date"].dt.year
df["Quarter"] = "Q" + df["Invoice Date"].dt.quarter.astype(str)

CSV_PATH = Path(__file__).with_name("coca_cola_retail_sales.csv")
if not CSV_PATH.exists():
    df.to_csv(CSV_PATH, index=False)

import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Coca-Cola USA Retailer Dashboard",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main {background-color: #f5f7fb;}
        .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
        .dashboard-title {
            background: linear-gradient(90deg, #0b2b5b, #123f78);
            color: white;
            padding: 18px 24px;
            border-radius: 8px;
            margin-bottom: 18px;
        }
        .dashboard-title h1 {margin:0; font-size: 30px;}
        .dashboard-title p {margin:5px 0 0; opacity:.85;}
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e1e6ef;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,.06);
        }
        .section-title {
            background:#0b2b5b;
            color:white;
            padding:8px 12px;
            border-radius:5px;
            font-weight:700;
            margin: 8px 0 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    data_frame = pd.read_csv(CSV_PATH)
    data_frame["Invoice Date"] = pd.to_datetime(data_frame["Invoice Date"])
    data_frame["Year"] = data_frame["Invoice Date"].dt.year
    data_frame["Quarter"] = "Q" + data_frame["Invoice Date"].dt.quarter.astype(str)
    return data_frame


dashboard_df = load_data()

st.markdown(
    """
    <div class="dashboard-title">
        <h1>🥤 Coca-Cola USA Retailer Dashboard</h1>
        <p>Retail sales, units sold and operating-profit analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("🔎 Dashboard Filters")


def multi_filter(label, column):
    options = sorted(dashboard_df[column].dropna().unique().tolist())
    return st.sidebar.multiselect(label, options, default=options)

regions = multi_filter("Region", "Region")
retailers = multi_filter("Retailer", "Retailer")
brands = multi_filter("Beverage Brand", "Beverage Brand")
years = multi_filter("Year", "Year")

filtered = dashboard_df[
    dashboard_df["Region"].isin(regions)
    & dashboard_df["Retailer"].isin(retailers)
    & dashboard_df["Beverage Brand"].isin(brands)
    & dashboard_df["Year"].isin(years)
].copy()

states = sorted(filtered["State"].unique().tolist())
cities = sorted(filtered["City"].unique().tolist())

selected_states = st.sidebar.multiselect("State", states, default=states)
selected_cities = st.sidebar.multiselect("City", cities, default=cities)

filtered = filtered[
    filtered["State"].isin(selected_states) & filtered["City"].isin(selected_cities)
].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"Rows after filters: {len(filtered):,}")

if filtered.empty:
    st.warning("No data matches the selected filters. Please change the filters.")
    st.stop()

total_sales = filtered["Total Sales"].sum()
units = filtered["Units Sold"].sum()
avg_price = filtered["Price per Unit"].mean()
profit = filtered["Operating Profit"].sum()
margin = (profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", f"${total_sales:,.0f}")
k2.metric("Units Sold", f"{units:,.0f}")
k3.metric("Average Price", f"${avg_price:.2f}")
k4.metric("Operating Profit", f"${profit:,.0f}")
k5.metric("Operating Margin", f"{margin:.1f}%")

left, right = st.columns(2)

with left:
    st.markdown('<div class="section-title">Sales by Beverage Brand</div>', unsafe_allow_html=True)
    brand = (
        filtered.groupby("Beverage Brand", as_index=False)
        .agg(
            Sales=("Total Sales", "sum"),
            Units=("Units Sold", "sum"),
            Avg_Price=("Price per Unit", "mean"),
            Operating_Profit=("Operating Profit", "sum"),
        )
    )
    brand["Margin"] = brand["Operating_Profit"] / brand["Sales"] * 100
    brand = brand.sort_values("Sales", ascending=False)
    st.dataframe(
        brand.style.format(
            {
                "Sales": "${:,.0f}",
                "Units": "{:,.0f}",
                "Avg_Price": "${:.2f}",
                "Operating_Profit": "${:,.0f}",
                "Margin": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.markdown('<div class="section-title">Sales by Retailer</div>', unsafe_allow_html=True)
    retailer = (
        filtered.groupby("Retailer", as_index=False)
        .agg(
            Sales=("Total Sales", "sum"),
            Units=("Units Sold", "sum"),
            Operating_Profit=("Operating Profit", "sum"),
        )
    )
    retailer["Margin"] = retailer["Operating_Profit"] / retailer["Sales"] * 100
    retailer = retailer.sort_values("Sales", ascending=False)
    st.dataframe(
        retailer.style.format(
            {
                "Sales": "${:,.0f}",
                "Units": "{:,.0f}",
                "Operating_Profit": "${:,.0f}",
                "Margin": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown('<div class="section-title">Sales and Operating Profit Margin by Quarter</div>', unsafe_allow_html=True)
quarter = (
    filtered.groupby(["Year", "Quarter"], as_index=False)
    .agg(Sales=("Total Sales", "sum"), Operating_Profit=("Operating Profit", "sum"))
)
quarter["Margin"] = quarter["Operating_Profit"] / quarter["Sales"] * 100
quarter["Quarter_Label"] = quarter["Year"].astype(str) + " " + quarter["Quarter"]
quarter = quarter.sort_values(["Year", "Quarter"])

c1, c2 = st.columns(2)

with c1:
    fig_sales = px.bar(
        quarter,
        x="Quarter_Label",
        y="Sales",
        text_auto=".2s",
        title="Quarterly Sales",
    )
    fig_sales.update_layout(
        xaxis_title="",
        yaxis_title="Sales ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_sales, use_container_width=True)

with c2:
    fig_margin = px.line(
        quarter,
        x="Quarter_Label",
        y="Margin",
        markers=True,
        title="Quarterly Operating Margin",
    )
    fig_margin.update_traces(line_width=3)
    fig_margin.update_layout(
        xaxis_title="",
        yaxis_title="Operating Margin (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_margin, use_container_width=True)

st.markdown('<div class="section-title">Regional Performance</div>', unsafe_allow_html=True)
geo = (
    filtered.groupby("Region", as_index=False)
    .agg(
        Sales=("Total Sales", "sum"),
        Units=("Units Sold", "sum"),
        Profit=("Operating Profit", "sum"),
    )
)
geo["Margin"] = geo["Profit"] / geo["Sales"] * 100

g1, g2 = st.columns(2)

with g1:
    fig_region = px.bar(
        geo.sort_values("Sales", ascending=True),
        x="Sales",
        y="Region",
        orientation="h",
        text_auto=".2s",
        title="Sales by Region",
    )
    fig_region.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig_region, use_container_width=True)

with g2:
    fig_region_margin = px.bar(
        geo.sort_values("Margin", ascending=True),
        x="Margin",
        y="Region",
        orientation="h",
        text_auto=".1f",
        title="Operating Margin by Region",
    )
    fig_region_margin.update_layout(
        xaxis_title="Margin (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig_region_margin, use_container_width=True)

with st.expander("📋 View filtered transaction data"):
    display_df = filtered.sort_values("Invoice Date", ascending=False).copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Download Filtered Data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_coca_cola_sales.csv",
    mime="text/csv",
)

st.caption(
    "Dashboard created from the transaction data supplied by the user. The sample contains 2023 transactions, so year comparisons are generated only when multiple years exist in the data."
)

