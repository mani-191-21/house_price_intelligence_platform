import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np

st.set_page_config(page_title="Geographic Maps", page_icon="🗺️", layout="wide")

# =========================================================
# DARK NAVY PLOTLY TEMPLATE
# =========================================================
pio.templates["dark_navy"] = pio.templates["plotly_dark"]

pio.templates["dark_navy"].layout.paper_bgcolor = "#0f172a"
pio.templates["dark_navy"].layout.plot_bgcolor = "#1e293b"
pio.templates["dark_navy"].layout.font.color = "#e2e8f0"
pio.templates["dark_navy"].layout.legend.bgcolor = "#1e293b"
pio.templates["dark_navy"].layout.xaxis.gridcolor = "#334155"
pio.templates["dark_navy"].layout.yaxis.gridcolor = "#334155"

pio.templates.default = "dark_navy"

# =========================================================
# GLOBAL DARK NAVY + PURPLE HEADER
# =========================================================
st.markdown("""
<style>

/* Main Background */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
}

.block-container {
    background-color: #0f172a !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Purple Header */
.maps-header {
    background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
    padding: 2.5rem;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(124, 58, 237, 0.5);
}

/* Text */
h1, h2, h3, h4 {
    color: #f1f5f9 !important;
}

p, span, div {
    color: #cbd5e1;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #1e293b !important;
    border-radius: 12px;
    padding: 15px;
}

/* Remove white from components */
.stTabs [data-baseweb="tab-panel"] {
    background-color: #0f172a !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="maps-header">
    <h1>🗺️ Geographic Distribution & Maps</h1>
    <p style="font-size: 1.2rem;">
        Visualize property distributions and geographic patterns
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# API SETUP
# =========================================================
if 'api_base' not in st.session_state:
    st.session_state.api_base = "http://localhost:8000/api"

API_URL = "http://localhost:8000/api/map"

API_BASE = st.session_state.api_base

@st.cache_data(ttl=600)
def load_map_data():
    try:
        response = requests.get(f"{API_BASE}/maps/geographic", timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

with st.spinner("Loading geographic data..."):
    data = load_map_data()

# =========================================================
# SAMPLE DATA FALLBACK
# =========================================================
if not data:
    sample_neighborhoods = [
        "NAmes", "CollgCr", "OldTown", "Edwards", "Somerst",
        "Gilbert", "NridgHt", "Sawyer", "NWAmes", "SawyerW"
    ]

    np.random.seed(42)
    data = {
        "neighborhood_distribution": [
            {
                "Neighborhood": hood,
                "AvgPrice": np.random.randint(150000, 400000),
                "Count": np.random.randint(20, 100),
                "Lat": 42.0308 + np.random.uniform(-0.02, 0.02),
                "Lon": -93.6319 + np.random.uniform(-0.02, 0.02)
            }
            for hood in sample_neighborhoods
        ]
    }

# ------------------------------
# Function to apply Dark Navy layout
# ------------------------------
def apply_dark_navy_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(15, 23, 42, 1)",  # dark navy overall background
        plot_bgcolor="rgba(15, 23, 42, 1)",   # dark navy for chart area
        font=dict(color="white"),              # white text for contrast
        legend=dict(font=dict(color="white")),# ensure legend text is readable
        margin=dict(l=40, r=40, t=40, b=40)   # optional: add padding
    )
    return fig

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["🗺️ Neighborhood Map", "📊 Distribution Analysis", "🌍 Folium Map"])

# =========================================================
# TAB 1 — Executive Neighborhood Intelligence
# =========================================================
with tab1:

    geo_data = pd.DataFrame(data["neighborhood_distribution"])

    st.markdown("## 🏘️ Neighborhood Market Intelligence")

    # ---------------------------------------------------
    # 🔹 Top KPI Metrics
    # ---------------------------------------------------
    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total Neighborhoods", len(geo_data))
    k2.metric("Total Listings", geo_data["Count"].sum())
    k3.metric("Average Price", f"${geo_data['AvgPrice'].mean():,.0f}")
    k4.metric("Highest Price", f"${geo_data['AvgPrice'].max():,.0f}")
    k5.metric("Lowest Price", f"${geo_data['AvgPrice'].min():,.0f}")

    st.markdown("---")

    # ---------------------------------------------------
    # 🔹 Main Analytics Row
    # ---------------------------------------------------
    col1, col2, col3 = st.columns(3)

    # 1️⃣ Top Expensive Neighborhoods
    with col1:
        top_price = geo_data.sort_values("AvgPrice", ascending=False).head(10)

        fig = px.bar(
            top_price,
            x="Neighborhood",
            y="AvgPrice",
            color="AvgPrice",
            title="💰 Most Expensive Areas",
            color_continuous_scale="Reds"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # 2️⃣ Highest Supply Areas
    with col2:
        top_supply = geo_data.sort_values("Count", ascending=False).head(10)

        fig = px.bar(
            top_supply,
            x="Neighborhood",
            y="Count",
            color="Count",
            title="📦 Highest Property Supply",
            color_continuous_scale="Blues"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # 3️⃣ Price vs Demand Matrix
    with col3:
        fig = px.scatter(
            geo_data,
            x="Count",
            y="AvgPrice",
            size="Count",
            color="AvgPrice",
            hover_name="Neighborhood",
            title="📊 Demand vs Price Matrix"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # 🔹 Premium Market Insights
    # ---------------------------------------------------
    col4, col5 = st.columns(2)

    # 4️⃣ Premium vs Standard Segmentation
    with col4:
        threshold = geo_data["AvgPrice"].median()

        seg = geo_data.copy()
        seg["Segment"] = seg["AvgPrice"].apply(
            lambda x: "Premium" if x > threshold else "Standard"
        )

        fig = px.bar(
            seg,
            x="Neighborhood",
            y="AvgPrice",
            color="Segment",
            title="🏆 Premium vs Standard Areas"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # 5️⃣ Market Activity Score
    with col5:
        geo_data["ActivityScore"] = geo_data["Count"] * geo_data["AvgPrice"]

        fig = px.bar(
            geo_data.sort_values("ActivityScore", ascending=False),
            x="Neighborhood",
            y="ActivityScore",
            color="ActivityScore",
            title="🔥 Market Activity Score"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        

# =========================================================
# TAB 2 — Distribution (Enterprise Analytics)
# =========================================================
with tab2:

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    # ---------------------------------------------------
    # 1️⃣ Property Supply by Neighborhood
    # ---------------------------------------------------
    st.subheader("Property Supply by Neighborhood")
    fig = px.bar(
        geo_data.sort_values("Count", ascending=False),
        x="Neighborhood",
        y="Count",
        color="Count",
        title="Supply by Neighborhood",
        color_continuous_scale="Blues"
    )
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # 2️⃣ Average Price by Neighborhood
    # ---------------------------------------------------
    st.subheader("Average Price by Neighborhood")
    fig = px.bar(
        geo_data.sort_values("AvgPrice", ascending=False),
        x="Neighborhood",
        y="AvgPrice",
        color="AvgPrice",
        title="Average Price Distribution",
        color_continuous_scale="Purples"
    )
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=400, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # 3️⃣ Price vs Supply Matrix
    # ---------------------------------------------------
    st.subheader("Price vs Supply Matrix")
    fig = px.scatter(
        geo_data,
        x="Count",
        y="AvgPrice",
        size="Count",
        color="AvgPrice",
        hover_name="Neighborhood",
        title="Price vs Supply Matrix"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # 4️⃣ High-Demand Premium Zones
    # ---------------------------------------------------
    st.subheader("High-Demand Premium Zones")
    high_demand = geo_data[
        geo_data["Count"] > geo_data["Count"].median()
    ]

    fig = px.scatter(
        high_demand,
        x="Count",
        y="AvgPrice",
        size="AvgPrice",
        color="AvgPrice",
        hover_name="Neighborhood",
        title="High-Demand Premium Zones"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # 5️⃣ Price Inequality Analysis
    # ---------------------------------------------------
    st.subheader("Price Inequality Analysis")
    price_sorted = geo_data.sort_values("AvgPrice")

    fig = px.line(
        price_sorted,
        x="Neighborhood",
        y="AvgPrice",
        markers=True,
        title="Price Inequality Across Neighborhoods"
    )
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------
    # 6️⃣ Premium vs Standard Segmentation
    # ---------------------------------------------------
    st.subheader("Premium vs Standard Segmentation")
    threshold = geo_data["AvgPrice"].median()

    premium = geo_data.copy()
    premium["Segment"] = premium["AvgPrice"].apply(
        lambda x: "Premium" if x > threshold else "Standard"
    )

    fig = px.bar(
        premium,
        x="Neighborhood",
        y="AvgPrice",
        color="Segment",
        title="Premium vs Standard Areas"
    )
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Geographic Summary")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Neighborhoods", len(geo_data))
    c2.metric("Total Properties", geo_data["Count"].sum())
    c3.metric("Avg Price", f"${geo_data['AvgPrice'].mean():,.0f}")
    c4.metric("Price Range", f"${geo_data['AvgPrice'].max() - geo_data['AvgPrice'].min():,.0f}")

# =========================================================
# TAB 3 - Folium Map (HTML from FastAPI)
# =========================================================
with tab3:
    st.markdown("### 🌍 Interactive Folium Map")

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            map_html = response.text

            st.components.v1.html(
                map_html,
                height=700,
                scrolling=True
            )
        else:
            st.error("Failed to load map from FastAPI")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🗺️ Map Controls")

    show_labels = st.checkbox("Show Labels", value=True)
    map_style = st.selectbox("Map Style", ["Default", "Satellite", "Terrain"])

    st.markdown("---")
    st.info("""
    Data represents properties in
    Ames, Iowa area with geographic
    coordinates for visualization.
    """)

    if st.button("🔄 Refresh Map", use_container_width=True):
        st.cache_data.clear()
        st.rerun()