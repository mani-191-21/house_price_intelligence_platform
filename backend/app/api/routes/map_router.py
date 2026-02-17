import os
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

# ===========================
# PATH
# ===========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, "data", "house_prices1.csv")

# ===========================
# NEIGHBORHOOD COORDS (Approx Ames)
# ===========================

NEIGH_COORDS = {
    "North Ames": [42.06, -93.62],
    "College Creek": [42.02, -93.64],
    "Old Town": [42.03, -93.61],
    "Edwards": [42.01, -93.63],
    "Somerset": [42.04, -93.66],
    "Northridge Heights": [42.05, -93.65],
    "Gilbert": [42.04, -93.60],
    "Sawyer": [42.02, -93.58],
    "Mitchell": [42.03, -93.59],
    "Crawford": [42.01, -93.61],
    "Brookside": [42.02, -93.60],
    "Iowa DOT and Rail Road": [42.00, -93.62],
    "Meadow Village": [42.01, -93.57],

    # Extra neighborhoods (approx same Ames region)
    "Northridge": [42.055, -93.655],
    "Sawyer West": [42.025, -93.585],
    "Stone Brook": [42.045, -93.665],
    "Clear Creek": [42.015, -93.645],
    "Timberland": [42.035, -93.675],
    "Veenker": [42.020, -93.655],
    "Northpark Villa": [42.010, -93.585],
    "Bloomington Heights": [42.030, -93.640],
    "Briardale": [42.018, -93.600],
    "South & West of Iowa State University": [42.000, -93.590],
    "Bluestem": [42.060, -93.580],
    "Greens": [42.048, -93.630],
    "Green Hills": [42.040, -93.690]
}

# ===========================
# LOAD DATA
# ===========================

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("CSV file not found")
    return pd.read_csv(DATA_PATH)

# ===========================
# COLOR LOGIC
# ===========================

def price_color(price):
    if price > 250000:
        return "red"
    elif price > 180000:
        return "orange"
    else:
        return "green"

# ===========================
# MAP ROUTE
# ===========================

@router.get("/map", response_class=HTMLResponse)
def generate_map():

    df = load_data()

    # IMPORTANT FIX 👇
    agg = df.groupby("Neighborhood Name").mean(numeric_only=True).reset_index()

    base_map = folium.Map(location=[42.03, -93.62], zoom_start=12)

    # =====================
    # FEATURE GROUPS
    # =====================

    marker_layer = folium.FeatureGroup(name="Neighborhood Markers")
    heat_layer = folium.FeatureGroup(name="Price Heatmap")
    area_layer = folium.FeatureGroup(name="Living Area Size")
    price_color_layer = folium.FeatureGroup(name="Price Level")
    prediction_layer = folium.FeatureGroup(name="Predicted Prices")

    cluster = MarkerCluster()

    heat_points = []

    # =====================
    # LOOP THROUGH DATA
    # =====================

    for _, r in agg.iterrows():

        name = r["Neighborhood Name"]

        if name not in NEIGH_COORDS:
            continue

        lat, lon = NEIGH_COORDS[name]

        avg_price = r["House Sale Price"]
        avg_area = r["Above Ground Living Area"]

        # -------- Basic Marker --------
        folium.Marker(
            [lat, lon],
            popup=f"{name}<br>Avg Price: ${int(avg_price)}"
        ).add_to(marker_layer)

        # -------- Cluster --------
        folium.Marker(
            [lat, lon],
            popup=name
        ).add_to(cluster)

        # -------- Heatmap data --------
        heat_points.append([lat, lon, avg_price])

        # -------- Area circles --------
        folium.CircleMarker(
            [lat, lon],
            radius=avg_area / 400,   # scaled
            popup=f"{int(avg_area)} sqft",
            fill=True,
            fill_opacity=0.6
        ).add_to(area_layer)

        # -------- Price colored circles --------
        folium.CircleMarker(
            [lat, lon],
            radius=10,
            color=price_color(avg_price),
            fill=True,
            fill_opacity=0.8,
            popup=f"{name}: ${int(avg_price)}"
        ).add_to(price_color_layer)

        # -------- Prediction (simple 5%) --------
        predicted = avg_price * 1.05

        folium.Marker(
            [lat, lon],
            popup=f"""
            <b>{name}</b><br>
            Actual: ${int(avg_price)}<br>
            Predicted: ${int(predicted)}
            """,
            icon=folium.Icon(color="blue")
        ).add_to(prediction_layer)

    # =====================
    # ADD HEATMAP
    # =====================

    HeatMap(heat_points).add_to(heat_layer)

    # =====================
    # ADD ALL LAYERS
    # =====================

    marker_layer.add_to(base_map)
    heat_layer.add_to(base_map)
    area_layer.add_to(base_map)
    price_color_layer.add_to(base_map)
    prediction_layer.add_to(base_map)
    cluster.add_to(base_map)

    folium.LayerControl(collapsed=False).add_to(base_map)

    return base_map._repr_html_()