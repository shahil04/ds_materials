import pandas as pd
import plotly.express as px
import gradio as gr

df = pd.read_csv("clean_data_EDA.csv")

for column in ["location", "society", "availability"]:
    df[column] = df[column].fillna("Unknown").astype(str).str.strip()

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["total_sqft"] = pd.to_numeric(df["total_sqft"], errors="coerce")
df["price_per_sqft"] = pd.to_numeric(df["price_per_sqft"], errors="coerce")
df["bhk"] = pd.to_numeric(df["size"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
df = df.dropna(subset=["price", "total_sqft", "price_per_sqft", "bhk"])
df["bhk_label"] = df["bhk"].astype(int).astype(str) + " BHK"

locations = ["All locations"] + sorted(df["location"].unique().tolist())
societies = ["All societies"] + sorted(df["society"].unique().tolist())
availability_options = ["All availability"] + sorted(df["availability"].unique().tolist())
bhk_options = ["All BHK"] + sorted(df["bhk_label"].unique(), key=lambda value: int(value.split()[0]))
min_price = int(df["price"].min())
max_price = int(df["price"].max())

location_coordinates = {
    "Whitefield": (12.9698, 77.7499), "Electronic City": (12.8399, 77.6770),
    "Electronic City Phase II": (12.8452, 77.6636), "Sarjapur Road": (12.9100, 77.6870),
    "Marathahalli": (12.9591, 77.6974), "Koramangala": (12.9352, 77.6245),
    "Indiranagar": (12.9784, 77.6408), "HSR Layout": (12.9116, 77.6389),
    "Jayanagar": (12.9250, 77.5938), "Rajaji Nagar": (12.9911, 77.5521),
    "Yelahanka": (13.1007, 77.5963), "Hebbal": (13.0358, 77.5970),
    "Banashankari": (12.9255, 77.5468), "Kanakapura Road": (12.8746, 77.5750),
    "Bannerghatta Road": (12.8772, 77.5970), "Bellandur": (12.9304, 77.6784),
    "Kengeri": (12.9081, 77.4871), "Uttarahalli": (12.8980, 77.5283),
}
city_center = (12.9716, 77.5946)
df["latitude"] = df["location"].map(lambda value: location_coordinates.get(value, city_center)[0])
df["longitude"] = df["location"].map(lambda value: location_coordinates.get(value, city_center)[1])


def filter_data(location, society, availability, bhk, lower_price, upper_price):
    data = df.copy()
    if location != "All locations":
        data = data[data["location"] == location]
    if society != "All societies":
        data = data[data["society"] == society]
    if availability != "All availability":
        data = data[data["availability"] == availability]
    if bhk != "All BHK":
        data = data[data["bhk_label"] == bhk]
    lower_price, upper_price = sorted([lower_price, upper_price])
    return data[data["price"].between(lower_price, upper_price)]


def empty_chart(title, message="No properties match these filters"):
    figure = px.scatter(title=title)
    figure.add_annotation(text=message, showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper")
    figure.update_xaxes(visible=False)
    figure.update_yaxes(visible=False)
    return figure


def create_map(data):
    if data.empty:
        return empty_chart("Property map")
    map_summary = data.groupby(["location", "latitude", "longitude"], as_index=False).agg(
        listings=("price", "size"), average_price=("price", "mean"), average_price_per_sqft=("price_per_sqft", "mean")
    )
    figure = px.scatter_mapbox(
        map_summary, lat="latitude", lon="longitude", size="listings", hover_name="location",
        hover_data={"listings": True, "average_price": ":.1f", "average_price_per_sqft": ":.0f", "latitude": False, "longitude": False},
        color_discrete_sequence=["#111111"], size_max=32, opacity=0.78, zoom=10,
        center={"lat": city_center[0], "lon": city_center[1]}, mapbox_style="open-street-map",
        title="Property demand by location"
    )
    figure.update_layout(margin={"l": 0, "r": 0, "t": 55, "b": 0})
    return figure


def update_dashboard(location, society, availability, bhk, lower_price, upper_price):
    data = filter_data(location, society, availability, bhk, lower_price, upper_price)
    if data.empty:
        empty_kpis = """<div class='kpi-grid'><div class='kpi'><span>Properties</span><strong>0</strong></div><div class='kpi'><span>Average Price</span><strong>--</strong></div><div class='kpi'><span>Avg Price / Sqft</span><strong>--</strong></div><div class='kpi'><span>Top Location</span><strong>--</strong></div></div>"""
        empty_figures = [empty_chart(title) for title in ["Price vs Area", "BHK Mix", "Price / Sqft", "Top Locations"]]
        return empty_kpis, *empty_figures, empty_chart("Property map")

    average_price = data["price"].mean()
    average_price_per_sqft = data["price_per_sqft"].mean()
    top_location = data["location"].value_counts().index[0]
    kpis = f"""<div class='kpi-grid'><div class='kpi'><span>Properties</span><strong>{len(data):,}</strong><small>matching listings</small></div><div class='kpi'><span>Average Price</span><strong>₹{average_price:,.1f} L</strong><small>market midpoint</small></div><div class='kpi'><span>Avg Price / Sqft</span><strong>₹{average_price_per_sqft:,.0f}</strong><small>location-adjusted view</small></div><div class='kpi'><span>Top Location</span><strong>{top_location}</strong><small>most listings in view</small></div></div>"""

    chart_template = "plotly_white"
    figure1 = px.scatter(data, x="total_sqft", y="price", color="bhk_label", hover_data=["location", "bath"], title="Price vs Built-up Area", labels={"total_sqft": "Area (sqft)", "price": "Price (₹ Lakhs)", "bhk_label": "Configuration"}, template=chart_template)
    figure2 = px.histogram(data, x="bhk_label", color="bhk_label", category_orders={"bhk_label": bhk_options[1:]}, title="Configuration Mix", labels={"bhk_label": "Configuration", "count": "Listings"}, template=chart_template)
    figure3 = px.box(data, x="bhk_label", y="price_per_sqft", color="bhk_label", title="Price per Sqft by Configuration", labels={"bhk_label": "Configuration", "price_per_sqft": "₹ / sqft"}, template=chart_template)
    location_summary = data.groupby("location", as_index=False).agg(average_price=("price", "mean"), listings=("price", "size")).sort_values("average_price", ascending=False).head(10)
    figure4 = px.bar(location_summary, x="average_price", y="location", orientation="h", text="listings", title="Top Locations by Average Price", labels={"average_price": "Average Price (₹ Lakhs)", "location": "Location", "listings": "Listings"}, template=chart_template)
    figure4.update_layout(yaxis={"categoryorder": "total ascending"})
    for figure in [figure1, figure2, figure3, figure4]:
        figure.update_layout(margin={"l": 30, "r": 20, "t": 55, "b": 35}, legend_title_text="")
    return kpis, figure1, figure2, figure3, figure4, create_map(data)

# -----------------------------
# Interview analysis pages
# -----------------------------
location_prices = df.groupby("location", as_index=False).agg(average_price=("price", "mean"), listings=("price", "size")).query("listings >= 5").sort_values("average_price", ascending=False).head(15)
location_price_chart = px.bar(location_prices, x="average_price", y="location", orientation="h", text="listings", title="Average property price by location", labels={"average_price": "Average price (₹ Lakhs)", "location": "Location", "listings": "Listings"}, template="plotly_white")
location_price_chart.update_layout(yaxis={"categoryorder": "total ascending"})

price_sqft_chart = px.scatter(df, x="price_per_sqft", y="price", color="bhk_label", hover_data=["location", "total_sqft"], title="Price per sqft trend", labels={"price_per_sqft": "Price per sqft (₹)", "price": "Price (₹ Lakhs)", "bhk_label": "Configuration"}, template="plotly_white")
bhk_price_chart = px.box(df, x="bhk_label", y="price", color="bhk_label", title="Does BHK affect price?", labels={"bhk_label": "Configuration", "price": "Price (₹ Lakhs)"}, template="plotly_white")
area_price_chart = px.scatter(df, x="total_sqft", y="price", color="bhk_label", hover_data=["location", "bath", "balcony"], title="How does area impact price?", labels={"total_sqft": "Area (sqft)", "price": "Price (₹ Lakhs)"}, template="plotly_white")
amenity_chart = px.scatter(df, x="bath", y="price", size="balcony", color="bhk_label", hover_data=["location", "total_sqft"], title="Bathrooms, balconies, and price", labels={"bath": "Bathrooms", "price": "Price (₹ Lakhs)", "bhk_label": "Configuration"}, template="plotly_white")
availability_summary = df.groupby("availability", as_index=False).agg(listings=("price", "size"), average_price=("price", "mean"))
availability_chart = px.bar(availability_summary, x="availability", y="listings", color="availability", text="listings", title="Availability mix", labels={"availability": "Availability", "listings": "Listings"}, template="plotly_white")
value_summary = df.groupby("location", as_index=False).agg(listings=("price", "size"), average_price_per_sqft=("price_per_sqft", "mean")).query("listings >= 5").sort_values("average_price_per_sqft").head(15)
value_chart = px.bar(value_summary, x="average_price_per_sqft", y="location", orientation="h", text="listings", title="Best value locations by price per sqft", labels={"average_price_per_sqft": "Average price per sqft (₹)", "location": "Location"}, template="plotly_white")
value_chart.update_layout(yaxis={"categoryorder": "total descending"})

q1, q3 = df["price_per_sqft"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[(df["price_per_sqft"] < q1 - 1.5 * iqr) | (df["price_per_sqft"] > q3 + 1.5 * iqr)]
outlier_chart = px.scatter(outliers, x="total_sqft", y="price_per_sqft", color="location", hover_data=["price", "bhk_label"], title="Suspicious price-per-sqft outliers", labels={"total_sqft": "Area (sqft)", "price_per_sqft": "Price per sqft (₹)"}, template="plotly_white")

quality_table = pd.DataFrame({
    "Check": ["Total rows", "Missing values", "Non-numeric total_sqft", "Price-per-sqft outliers"],
    "Result": [len(df), int(df.isna().sum().sum()), int(pd.to_numeric(df["total_sqft"], errors="coerce").isna().sum()), len(outliers)],
    "Interpretation": ["Rows available after cleaning", "Remaining null cells", "Values requiring conversion or review", "Listings outside the 1.5 IQR rule"]
})

css = """
body { background: #eef2f5; }
.gradio-container { max-width: 1440px !important; background: #eef2f5; }
.hero { background: #e8f1f5; color: #17324d; padding: 28px 34px; border-radius: 14px; margin-bottom: 18px; border: 1px solid #c7dce4; }
.hero h1 { margin: 0 0 6px; font-size: 31px; }
.hero p { margin: 0; color: #526b7a; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 0 0 18px; }
.kpi { background: white; border-left: 5px solid #f4a261; border-radius: 10px; padding: 16px 18px; min-height: 82px; box-shadow: 0 2px 8px #102a4312; }
.kpi span, .kpi small { display: block; color: #607080; font-size: 12px; }
.kpi strong { display: block; color: #102a43; font-size: 21px; margin: 7px 0 3px; }
.insight-page { background: white; padding: 24px 30px; border-radius: 12px; border: 1px solid #d7e2e8; }
.insight-page h2 { color: #17324d; margin-top: 4px; }
.insight-page h3 { color: #c46b2d; margin-top: 24px; }
.insight-page li { margin: 10px 0; color: #425466; }
@media (max-width: 800px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
"""

with gr.Blocks(css=css, title="Bangalore Property Intelligence") as demo:
    gr.HTML("<div class='hero'><h1>Bangalore Property Intelligence</h1><p>Explore pricing, demand, and value across the residential market.</p></div>")
    with gr.Tabs():
        with gr.Tab("Dashboard"):
            with gr.Row():
                with gr.Column(scale=1, min_width=220):
                    gr.Markdown("### Market slicers")
                    location_filter = gr.Dropdown(locations, value="All locations", label="Location")
                    society_filter = gr.Dropdown(societies, value="All societies", label="Society")
                    availability_filter = gr.Dropdown(availability_options, value="All availability", label="Availability")
                    bhk_filter = gr.Dropdown(bhk_options, value="All BHK", label="Configuration")
                    lower_price = gr.Slider(minimum=min_price, maximum=max_price, value=min_price, step=1, label="Minimum price (₹ Lakhs)")
                    upper_price = gr.Slider(minimum=min_price, maximum=max_price, value=max_price, step=1, label="Maximum price (₹ Lakhs)")
                    apply_button = gr.Button("Apply filters", variant="primary")
                with gr.Column(scale=4):
                    kpi_output = gr.HTML()
                    with gr.Row():
                        price_area_plot = gr.Plot()
                        configuration_plot = gr.Plot()
                    with gr.Row():
                        value_plot = gr.Plot()
                        location_plot = gr.Plot()
        with gr.Tab("EDA Steps"):
            gr.Markdown("### EDA workflow used in this project")
            gr.HTML("""
            <div class='insight-page'>
                <h2>Exploratory Data Analysis workflow</h2>
                <ol>
                    <li><strong>Data loading:</strong> read the Bangalore housing dataset and inspect its structure.</li>
                    <li><strong>Data quality checks:</strong> find missing values, duplicate records, and inconsistent formats.</li>
                    <li><strong>Data cleaning:</strong> fix nulls, convert ranges, normalize numeric fields, and remove invalid rows.</li>
                    <li><strong>Feature engineering:</strong> create meaningful variables such as BHK and price per sqft.</li>
                    <li><strong>Univariate analysis:</strong> study the distribution of price, area, and configuration.</li>
                    <li><strong>Bivariate analysis:</strong> compare price against area, bathrooms, and location.</li>
                    <li><strong>Multivariate analysis:</strong> identify relationships using correlation and grouped views.</li>
                    <li><strong>Business interpretation:</strong> translate the findings into investment and pricing recommendations.</li>
                </ol>
            </div>
            """)
        with gr.Tab("Market map"):
            gr.Markdown("### Location intelligence\nBlack bubbles show listing locations. Bubble size shows listing volume; hover for average price and price per sqft.")
            map_plot = gr.Plot()
        with gr.Tab("Market analysis"):
            gr.Markdown("### Interview-level market analysis")
            with gr.Row():
                gr.Plot(value=location_price_chart)
                gr.Plot(value=price_sqft_chart)
            with gr.Row():
                gr.Plot(value=bhk_price_chart)
                gr.Plot(value=area_price_chart)
            with gr.Row():
                gr.Plot(value=amenity_chart)
                gr.Plot(value=availability_chart)
            with gr.Row():
                gr.Plot(value=value_chart)
                gr.Plot(value=outlier_chart)
        with gr.Tab("Data quality"):
            gr.Markdown("### Data quality and real-world checks")
            gr.Markdown("The summary below answers whether the dataset contains missing values, inconsistent numeric formats, or suspicious listings.")
            gr.Dataframe(value=quality_table, interactive=False, label="Quality summary")
        with gr.Tab("Insights & recommendations"):
            gr.HTML("""
            <div class='insight-page'>
                <h2>Market insights</h2>
                <p>Use these findings to guide pricing, investment, and marketing decisions.</p>
                <h3>Example insights</h3>
                <ul>
                    <li><strong>Whitefield</strong> and <strong>Rajaji Nagar</strong> show higher average prices.</li>
                    <li>Property price generally increases with square footage and BHK.</li>
                    <li>Some properties have unrealistically high <strong>price_per_sqft</strong> values and should be reviewed as outliers.</li>
                    <li>Ready-to-move homes tend to be slightly more expensive.</li>
                    <li>Certain locations offer better value for investment through lower price per sqft.</li>
                </ul>
                <h3>Business recommendations</h3>
                <ul>
                    <li>Invest in mid-range locations with growing demand.</li>
                    <li>Avoid properties with abnormally high price per sqft until the listing is validated.</li>
                    <li>Focus marketing on the 2-3 BHK segment because it has the strongest demand signal.</li>
                    <li>Promote ready-to-move properties to premium buyers.</li>
                </ul>
            </div>
            """)

    dashboard_inputs = [location_filter, society_filter, availability_filter, bhk_filter, lower_price, upper_price]
    dashboard_outputs = [kpi_output, price_area_plot, configuration_plot, value_plot, location_plot, map_plot]
    apply_button.click(fn=update_dashboard, inputs=dashboard_inputs, outputs=dashboard_outputs)
    demo.load(fn=update_dashboard, inputs=dashboard_inputs, outputs=dashboard_outputs)

demo.launch()