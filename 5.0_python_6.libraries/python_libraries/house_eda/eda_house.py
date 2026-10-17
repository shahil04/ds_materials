import pandas as pd
import plotly.express as px
import gradio as gr

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("clean_data_EDA.csv")

# -----------------------------
# Basic Cleaning (Safety)
# -----------------------------
df['location'] = df['location'].astype(str).str.strip()
df['society'] = df['society'].astype(str).str.strip().fillna("unknown")
df['availability'] = df['availability'].astype(str).str.strip()

# Ensure numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['total_sqft'] = pd.to_numeric(df['total_sqft'], errors='coerce')
df['price_per_sqft'] = pd.to_numeric(df['price_per_sqft'], errors='coerce')

# Drop nulls
df = df.dropna(subset=['price', 'total_sqft', 'price_per_sqft'])

# -----------------------------
# Filter Function
# -----------------------------
def filter_data(location, society, availability, price_range):
    data = df.copy()

    if location != "All":
        data = data[data['location'] == location]

    if society != "All":
        data = data[data['society'] == society]

    if availability != "All":
        data = data[data['availability'] == availability]

    min_price, max_price = price_range

    data = data[
        (data['price'] >= min_price) &
        (data['price'] <= max_price)
    ]

    return data

# -----------------------------
# Dashboard Function
# -----------------------------
def update_dashboard(location, society, availability, price_range):

    data = filter_data(location, society, availability, price_range)

    import plotly.graph_objects as go

    if data.empty:
        # Placeholder plots with message
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data for selected filters", xref="paper", yref="paper", showarrow=False, font=dict(size=18))
        empty_fig.update_layout(title="No Data")
        return empty_fig, empty_fig, empty_fig, empty_fig

    # Ensure 'size' column exists for color
    color_col = "size" if "size" in data.columns else None

    # Scatter Plot
    fig1 = px.scatter(
        data,
        x="total_sqft",
        y="price",
        color=color_col,
        title="Price vs Total Sqft"
    )

    # BHK / Size Distribution
    fig2 = px.histogram(
        data,
        x="size" if "size" in data.columns else data.columns[0],
        title="BHK Distribution"
    )

    # Price per Sqft
    fig3 = px.box(
        data,
        y="price_per_sqft",
        title="Price per Sqft Distribution"
    )

    # Top Locations
    if not data.empty and "location" in data.columns:
        top_loc = data.groupby('location')['price'].mean().sort_values(ascending=False).head(10)
        fig4 = px.bar(
            x=top_loc.index,
            y=top_loc.values,
            title="Top Locations by Avg Price"
        )
    else:
        fig4 = go.Figure()
        fig4.add_annotation(text="No data for locations", xref="paper", yref="paper", showarrow=False, font=dict(size=18))
        fig4.update_layout(title="No Data")

    return fig1, fig2, fig3, fig4

# -----------------------------
# Dropdown Values
# -----------------------------
locations = ["All"] + sorted(df['location'].unique().tolist())
societies = ["All"] + sorted(df['society'].unique().tolist())
availability_list = ["All"] + sorted(df['availability'].unique().tolist())

# Price Range
min_price = int(df['price'].min())
max_price = int(df['price'].max())

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks() as demo:

    gr.Markdown("# 🏠 Bangalore Housing EDA Dashboard")

    with gr.Row():
        location_dd = gr.Dropdown(locations, value="All", label="Location")
        society_dd = gr.Dropdown(societies, value="All", label="Society")
        availability_dd = gr.Dropdown(availability_list, value="All", label="Availability")

    min_price_slider = gr.Slider(
        minimum=min_price,
        maximum=max_price,
        value=min_price,
        step=1,
        label="Min Price (Lakhs)"
    )
    max_price_slider = gr.Slider(
        minimum=min_price,
        maximum=max_price,
        value=max_price,
        step=1,
        label="Max Price (Lakhs)"
    )

    btn = gr.Button("Apply Filters")

    with gr.Row():
        plot1 = gr.Plot()
        plot2 = gr.Plot()

    with gr.Row():
        plot3 = gr.Plot()
        plot4 = gr.Plot()

    def dashboard_wrapper(location, society, availability, min_p, max_p):
        return update_dashboard(location, society, availability, (min_p, max_p))

    btn.click(
        fn=dashboard_wrapper,
        inputs=[location_dd, society_dd, availability_dd, min_price_slider, max_price_slider],
        outputs=[plot1, plot2, plot3, plot4]
    )

demo.launch()