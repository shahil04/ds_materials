import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Electric Vehicle Data Analysis",
    layout="wide",
    page_icon="🚗"
)

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Electric_Vehicle_Population_Data.csv")

df = load_data()

# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.title("🔍 Filters")

cafv = st.sidebar.multiselect(
    "CAFV Eligibility",
    df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].unique(),
    default=df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].unique()
)

ev_type = st.sidebar.multiselect(
    "Electric Vehicle Type",
    df["Electric Vehicle Type"].unique(),
    default=df["Electric Vehicle Type"].unique()
)

make = st.sidebar.multiselect(
    "Make",
    df["Make"].unique(),
    default=df["Make"].unique()
)

state = st.sidebar.multiselect(
    "State",
    df["State"].unique(),
    default=df["State"].unique()
)

# ------------------------------
# Apply Filters
# ------------------------------
filtered_df = df[
    (df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].isin(cafv)) &
    (df["Electric Vehicle Type"].isin(ev_type)) &
    (df["Make"].isin(make)) &
    (df["State"].isin(state))
]

# ------------------------------
# KPI Calculations
# ------------------------------
total_vehicles = len(filtered_df)
avg_range = round(filtered_df["Electric Range"].mean(), 2)

bev_count = filtered_df[
    filtered_df["Electric Vehicle Type"].str.contains("BEV")
].shape[0]

phev_count = filtered_df[
    filtered_df["Electric Vehicle Type"].str.contains("PHEV")
].shape[0]

bev_pct = round((bev_count / total_vehicles) * 100, 2) if total_vehicles else 0
phev_pct = round((phev_count / total_vehicles) * 100, 2) if total_vehicles else 0

# ------------------------------
# KPI Cards
# ------------------------------
st.markdown("## ⚡ Electric Vehicle Data Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚘 Total Vehicles", f"{total_vehicles:,}")
col2.metric("🔋 Avg Electric Range (Km)", avg_range)
col3.metric("⚡ Total BEV Vehicles", f"{bev_count:,}", f"{bev_pct}%")
col4.metric("🔌 Total PHEV Vehicles", f"{phev_count:,}", f"{phev_pct}%")

# ------------------------------
# Charts Row 1
# ------------------------------
col5, col6 = st.columns(2)

# Vehicles by Model Year (Area Chart)
year_df = (
    filtered_df[filtered_df["Model Year"] >= 2010]
    .groupby("Model Year")
    .size()
    .reset_index(name="Vehicles")
)

fig_year = px.area(
    year_df,
    x="Model Year",
    y="Vehicles",
    title="📈 Electric Vehicles Registered by Model Year",
    markers=True
)
col5.plotly_chart(fig_year, use_container_width=True)

# Vehicles by State (Map)
state_df = filtered_df.groupby("State").size().reset_index(name="Vehicles")

fig_map = px.choropleth(
    state_df,
    locations="State",
    locationmode="USA-states",
    color="Vehicles",
    scope="usa",
    title="🗺️ Electric Vehicles by State",
    color_continuous_scale="Greens"
)
col6.plotly_chart(fig_map, use_container_width=True)

# ------------------------------
# Charts Row 2
# ------------------------------
col7, col8 = st.columns(2)

# Top 10 Makes (Bar Chart)
make_df = (
    filtered_df.groupby("Make")
    .size()
    .reset_index(name="Vehicles")
    .sort_values(by="Vehicles", ascending=False)
    .head(10)
)

fig_make = px.bar(
    make_df,
    x="Vehicles",
    y="Make",
    orientation="h",
    title="🏭 Top 10 Vehicles by Make",
    text="Vehicles"
)
col7.plotly_chart(fig_make, use_container_width=True)

# CAFV Eligibility (Donut Chart)
cafv_df = (
    filtered_df.groupby("Clean Alternative Fuel Vehicle (CAFV) Eligibility")
    .size()
    .reset_index(name="Vehicles")
)

fig_cafv = px.pie(
    cafv_df,
    values="Vehicles",
    names="Clean Alternative Fuel Vehicle (CAFV) Eligibility",
    hole=0.5,
    title="♻️ Vehicles Eligibility for CAFV"
)
col8.plotly_chart(fig_cafv, use_container_width=True)

# ------------------------------
# Tree Map – Top 10 Models
# ------------------------------
model_df = (
    filtered_df.groupby(["Model", "Make"])
    .size()
    .reset_index(name="Vehicles")
    .sort_values(by="Vehicles", ascending=False)
    .head(10)
)

fig_tree = px.treemap(
    model_df,
    path=["Make", "Model"],
    values="Vehicles",
    title="🚘 Top 10 Vehicles by Model"
)

st.plotly_chart(fig_tree, use_container_width=True)
