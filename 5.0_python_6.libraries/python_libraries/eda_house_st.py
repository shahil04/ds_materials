import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Housing Dashboard", layout="wide")

st.title("🏠 Bangalore Housing EDA Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("clean_data_EDA.csv")

# -----------------------------
# Data Cleaning
# -----------------------------
df['location'] = df['location'].astype(str).str.strip()
df['society'] = df['society'].astype(str).str.strip().fillna("unknown")
df['availability'] = df['availability'].astype(str).str.strip()

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['total_sqft'] = pd.to_numeric(df['total_sqft'], errors='coerce')
df['price_per_sqft'] = pd.to_numeric(df['price_per_sqft'], errors='coerce')

df = df.dropna(subset=['price', 'total_sqft', 'price_per_sqft'])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

locations = ["All"] + sorted(df['location'].unique().tolist())
societies = ["All"] + sorted(df['society'].unique().tolist())
availability_list = ["All"] + sorted(df['availability'].unique().tolist())

location = st.sidebar.selectbox("Location", locations)
society = st.sidebar.selectbox("Society", societies)
availability = st.sidebar.selectbox("Availability", availability_list)

min_price = int(df['price'].min())
max_price = int(df['price'].max())

price_range = st.sidebar.slider(
    "Price Range (Lakhs)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['location'] == location]

if society != "All":
    filtered_df = filtered_df[filtered_df['society'] == society]

if availability != "All":
    filtered_df = filtered_df[filtered_df['availability'] == availability]

filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) &
    (filtered_df['price'] <= price_range[1])
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📊 Key Metrics")

total_sales = filtered_df['price'].sum()
total_count = filtered_df.shape[0]
avg_price = filtered_df['price'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales (Lakhs)", f"{total_sales:,.2f}")
col2.metric("🏠 Total Properties", total_count)
col3.metric("📈 Avg Price", f"{avg_price:,.2f}")

# -----------------------------
# Charts Section
# -----------------------------
st.subheader("📈 Analysis")

col1, col2 = st.columns(2)

# Top 5 Expensive Cities
top5 = filtered_df.groupby('location')['price'].mean().sort_values(ascending=False).head(5)
fig1 = px.bar(x=top5.index, y=top5.values, title="Top 5 Expensive Locations")
col1.plotly_chart(fig1, use_container_width=True)

# Low Expensive Cities
low5 = filtered_df.groupby('location')['price'].mean().sort_values(ascending=True).head(5)
fig2 = px.bar(x=low5.index, y=low5.values, title="Top 5 Affordable Locations")
col2.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Avg Sales per City
# -----------------------------
st.subheader("🏙️ Avg Price per Location")

avg_city = filtered_df.groupby('location')['price'].mean().sort_values(ascending=False)
fig3 = px.bar(avg_city, title="Average Price per Location")
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Contribution Analysis
# -----------------------------
st.subheader("📊 City-wise Contribution")

contribution = filtered_df.groupby('location')['price'].sum().reset_index()
total = contribution['price'].sum()

contribution['% Contribution'] = (contribution['price'] / total) * 100

fig4 = px.pie(
    contribution,
    names='location',
    values='price',
    title="City-wise Sales Contribution"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Scatter Plot
# -----------------------------
st.subheader("📌 Price vs Sqft")

fig5 = px.scatter(
    filtered_df,
    x="total_sqft",
    y="price",
    color="size" if "size" in filtered_df.columns else None,
    title="Price vs Total Sqft"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📋 Filtered Data")

st.dataframe(filtered_df)