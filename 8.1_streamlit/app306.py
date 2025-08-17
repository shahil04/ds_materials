# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px


# st.header("Title")
# st.write("this is a normal text")

# data = pd.read_csv("Electric_Vehicle_Population_Data.csv")

# st.sidebar.title("This is side bar")


# st.dataframe(data.head())

# # bar chart 
# bar_chart_data = data[["Make","Model Year"]].head()

# if st.button("demo button"):
#     st.bar_chart(bar_chart_data, x="Make", y="Model Year")

# else:
#     st.write("NAN  ")

# # Create some sample data
# d = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c']
# )

# # Display the line chart
# st.line_chart(d)


# # Example data
# d2 = {'x': [1, 2, 3, 4, 5],
#         'y': [5, 4, 3, 2, 1],
#         'z': [2, 4, 1, 5, 3]}
# df = pd.DataFrame(d2)

# fig = px.scatter_3d(df, x='x', y='y', z='z', 
#                     title='My 3D Scatter Plot',
#                     color='x', # Example: color points based on x-value
#                     size='y')  # Example: size points based on y-value

# st.plotly_chart(fig)



import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Load Data
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Electric_Vehicle_Population_Data.csv")
    return df

df = load_data()

# ------------------------
# Dashboard Title
# ------------------------
st.set_page_config(layout="wide")
st.title("🔋 Electric Vehicle Data Analysis")

# ------------------------
# KPI Section
# ------------------------
total_vehicles = df.shape[0]
avg_range = df["Electric Range"].mean()
bev_count = df[df["Electric Vehicle Type"].str.contains("BEV", na=False)].shape[0]
phev_count = df[df["Electric Vehicle Type"].str.contains("PHEV", na=False)].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Vehicles", f"{total_vehicles:,}")
col2.metric("Avg Electric Range", f"{avg_range:.2f} Km")
col3.metric("Total BEV Vehicles", f"{bev_count:,}", f"{(bev_count/total_vehicles)*100:.2f}%")
col4.metric("Total PHEV Vehicles", f"{phev_count:,}", f"{(phev_count/total_vehicles)*100:.2f}%")

st.markdown("---")

# ------------------------
# Filters
# ------------------------
st.sidebar.header("🔍 Filter Options")
cafv_filter = st.sidebar.selectbox("CAFV Eligibility", ["All"] + sorted(df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].unique()))
ev_type_filter = st.sidebar.selectbox("EV Type", ["All"] + sorted(df["Electric Vehicle Type"].unique()))
make_filter = st.sidebar.selectbox("Make", ["All"] + sorted(df["Make"].unique()))
state_filter = st.sidebar.selectbox("State", ["All"] + sorted(df["State"].unique()))

filtered_df = df.copy()
if cafv_filter != "All":
    filtered_df = filtered_df[filtered_df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"] == cafv_filter]
if ev_type_filter != "All":
    filtered_df = filtered_df[filtered_df["Electric Vehicle Type"] == ev_type_filter]
if make_filter != "All":
    filtered_df = filtered_df[filtered_df["Make"] == make_filter]
if state_filter != "All":
    filtered_df = filtered_df[filtered_df["State"] == state_filter]

# ------------------------
# Charts
# ------------------------
# 1. Vehicles by Model Year
year_chart = filtered_df.groupby("Model Year").size().reset_index(name="Count")
fig_year = px.line(year_chart, x="Model Year", y="Count", markers=True, title="Number of EVs Registered by Model Year")

# 2. Vehicles by State
state_chart = filtered_df.groupby("State").size().reset_index(name="Count")
fig_state = px.choropleth(state_chart,
                          locations="State",
                          locationmode="USA-states",
                          color="Count",
                          scope="usa",
                          title="Number of Vehicles by State")

# 3. Top 10 Vehicles by Make
make_chart = filtered_df.groupby("Make").size().reset_index(name="Count").sort_values(by="Count", ascending=False).head(10)
fig_make = px.bar(make_chart, x="Make", y="Count", title="Top 10 # of Vehicles by Make", text="Count")

# 4. CAFV Eligibility Pie
caf_chart = filtered_df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].value_counts().reset_index()
fig_cafv = px.pie(caf_chart, values="count", names="Clean Alternative Fuel Vehicle (CAFV) Eligibility", title="CAFV Eligibility")

# 5. Vehicles by Model
model_chart = filtered_df.groupby(["Model", "Make", "Electric Vehicle Type"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False).head(10)

# ------------------------
# Layout
# ------------------------
left_col, right_col = st.columns([2, 1])
with left_col:
    st.plotly_chart(fig_year, use_container_width=True)
with right_col:
    st.plotly_chart(fig_state, use_container_width=True)

colA, colB = st.columns(2)
colA.plotly_chart(fig_make, use_container_width=True)
colB.plotly_chart(fig_cafv, use_container_width=True)

st.subheader("Top 10 Vehicles by Model")
st.dataframe(model_chart)
