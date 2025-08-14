import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Electric_Vehicle_Population_Data.csv")
    return df

df = load_data()

# ===== Sidebar Filters =====
st.sidebar.header("Filter")
cafv_filter = st.sidebar.selectbox("CAFV Eligibility", options=["All"] + sorted(df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique()))
type_filter = st.sidebar.selectbox("Electric Vehicle Type", options=["All"] + sorted(df['Electric Vehicle Type'].unique()))
model_filter = st.sidebar.selectbox("Model", options=["All"] + sorted(df['Model'].unique()))
make_filter = st.sidebar.selectbox("Make", options=["All"] + sorted(df['Make'].unique()))
state_filter = st.sidebar.selectbox("State", options=["All"] + sorted(df['State'].unique()))

# Apply filters
filtered_df = df.copy()
if cafv_filter != "All":
    filtered_df = filtered_df[filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == cafv_filter]
if type_filter != "All":
    filtered_df = filtered_df[filtered_df['Electric Vehicle Type'] == type_filter]
if model_filter != "All":
    filtered_df = filtered_df[filtered_df['Model'] == model_filter]
if make_filter != "All":
    filtered_df = filtered_df[filtered_df['Make'] == make_filter]
if state_filter != "All":
    filtered_df = filtered_df[filtered_df['State'] == state_filter]

# ===== KPI Metrics =====
total_vehicles = len(filtered_df)
avg_range = filtered_df['Electric Range'].mean()
bev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains("BEV")])
phev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains("PHEV")])

st.markdown("## 🚗 Electric Vehicle Data Analysis")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Vehicles", f"{total_vehicles:,}")
col2.metric("Avg Electric Range (km)", f"{avg_range:.2f}")
col3.metric("Total BEV Vehicles", f"{bev_count:,}", f"{(bev_count/total_vehicles)*100:.2f}%")
col4.metric("Total PHEV Vehicles", f"{phev_count:,}", f"{(phev_count/total_vehicles)*100:.2f}%")

# ===== Charts =====
# Vehicles by Model Year
yearly = filtered_df.groupby('Model Year').size().reset_index(name='Count')
fig_year = px.line(yearly, x='Model Year', y='Count', markers=True, title="Vehicles Registered by Model Year")
st.plotly_chart(fig_year, use_container_width=True)

# Map - Vehicles by State
state_count = filtered_df.groupby('State').size().reset_index(name='Count')
fig_map = px.choropleth(state_count, locations='State', locationmode="USA-states", color='Count',
                        scope="usa", title="Vehicles by State", color_continuous_scale="Greens")
st.plotly_chart(fig_map, use_container_width=True)

# Top N Vehicles by Make
top_make = filtered_df['Make'].value_counts().reset_index()
top_make.columns = ['Make', 'Count']
fig_make = px.bar(top_make.head(10), x='Make', y='Count', title="Top 10 Vehicles by Make")
st.plotly_chart(fig_make, use_container_width=True)

# CAFV Pie Chart
cafv_count = filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().reset_index()
cafv_count.columns = ['CAFV Status', 'Count']
fig_pie = px.pie(cafv_count, names='CAFV Status', values='Count', title="CAFV Eligibility")
st.plotly_chart(fig_pie, use_container_width=True)

# Vehicles by Model Table
top_model = filtered_df.groupby(['Model', 'Make', 'Electric Vehicle Type']).size().reset_index(name='Count')
top_model['% of Total'] = (top_model['Count'] / total_vehicles) * 100
top_model = top_model.sort_values(by='Count', ascending=False).head(10)
st.write("### Vehicles by Model")
st.dataframe(top_model)
