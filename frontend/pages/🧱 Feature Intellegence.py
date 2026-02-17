import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

st.set_page_config(page_title="Property Features", page_icon="🏗️", layout="wide")

# =========================================================
# DARK NAVY PLOTLY TEMPLATE (FORCE ALL CHARTS)
# =========================================================
pio.templates["dark_navy"] = pio.templates["plotly_dark"]

pio.templates["dark_navy"].layout.paper_bgcolor = "#0f172a"   # app background navy
pio.templates["dark_navy"].layout.plot_bgcolor = "#1e293b"    # chart area navy
pio.templates["dark_navy"].layout.font.color = "#e2e8f0"
pio.templates["dark_navy"].layout.legend.bgcolor = "#1e293b"
pio.templates["dark_navy"].layout.xaxis.gridcolor = "#334155"
pio.templates["dark_navy"].layout.yaxis.gridcolor = "#334155"

pio.templates.default = "dark_navy"

# =========================================================
# Initialize API base
# =========================================================
if 'api_base' not in st.session_state:
    st.session_state.api_base = "http://localhost:8000/api"

API_BASE = st.session_state.api_base

# =========================================================
# CUSTOM CSS (NO WHITE ANYWHERE)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Remove default white */
html, body {
    background-color: #0f172a !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
}

.block-container {
    background-color: #0f172a !important;
    padding-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* HERO */
.jewel-hero {
    background: linear-gradient(135deg, #2A1A5E 0%, #5C2A72 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    color: #F0EAFB;  /* light jewel-tone text for luxury feel */
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(92, 42, 114, 0.5); /* subtle jewel glow */
}

.jewel-title {
    font-size: 3.5rem;
    font-weight: 700;
}

.jewel-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Dark metric cards */
[data-testid="metric-container"] {
    background-color: #1e293b !important;
    border-radius: 12px;
    padding: 15px;
}

/* Text */
h1, h2, h3, h4, h5, h6 {
    color: #f1f5f9 !important;
}

p, span, div {
    color: #cbd5e1;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #14532d 0%, #16a34a 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-weight: 600;
}

.stButton>button:hover {
    box-shadow: 0 6px 20px rgba(22, 163, 74, 0.4);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO HEADER
# =========================================================
st.markdown("""
<div class="jewel-hero">
    <div class="jewel-title">🏠 Property Feature Intelligence</div>
    <div class="jewel-subtitle">
        Advanced Property Insights • Structural Analytics • Feature Impact Analysis
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LOAD API DATA
# =========================================================
@st.cache_data(ttl=600)
def load_api_data(endpoint):
    try:
        res = requests.get(f"{API_BASE}{endpoint}", timeout=8)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

with st.spinner("Loading feature data..."):
    bldg = load_api_data("/features/building-types")
    style = load_api_data("/features/house-styles")
    found = load_api_data("/features/foundations")
    live = load_api_data("/features/living-area-impact")
    floor = load_api_data("/features/floor-impact")
    bed = load_api_data("/features/bedrooms")
    bath = load_api_data("/features/bathrooms")
    gar = load_api_data("/features/garage")
    out = load_api_data("/features/outdoor")
    pool = load_api_data("/features/pool")

if bldg.empty:
    st.warning("⚠️ No feature data available.")
    st.stop()

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏘️ Building & Design",
    "📐 Space & Area",
    "🛏️ Room Configuration",
    "🚗 Garage & Parking",
    "🌳 Outdoor Features"
])

# ------------------------------
# Tab 1: Building Types, Style, Foundation
# ------------------------------
# ------------------------------
# Tab 1: Building Types, Style, Foundation
# ------------------------------
with tab1:
    st.markdown("## 🏗️ Structural Composition — Enterprise Insights")

    # EXISTING VISUALS
    if not bldg.empty:
        fig = px.pie(bldg, names="Type", values="Count", hole=0.4,
                     title="Building Type Distribution")
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    if not style.empty:
        fig = px.bar(style, x="Style", y="Count", color="Count",
                     title="Architectural Style Distribution")
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    if not found.empty:
        fig = px.pie(found, names="Foundation", values="Count",
                     title="Foundation Type Distribution")
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏆 ENTERPRISE INSIGHT 1: Market Concentration Analysis
    # =========================================================
    if not bldg.empty:
        top_types = bldg.sort_values("Count", ascending=False).head(5)

        fig = px.bar(
            top_types,
            x="Type",
            y="Count",
            color="Count",
            title="Top Building Types by Market Concentration"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 💼 ENTERPRISE INSIGHT 2: Premium Style Dominance
    # =========================================================
    if not style.empty:
        top_styles = style.sort_values("Count", ascending=False).head(5)

        fig = px.pie(
            top_styles,
            names="Style",
            values="Count",
            hole=0.5,
            title="Dominant Architectural Styles (Top 5)"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏠 ENTERPRISE INSIGHT 3: Foundation Reliability Distribution
    # =========================================================
    if not found.empty:
        fig = px.bar(
            found.sort_values("Count", ascending=False),
            x="Foundation",
            y="Count",
            color="Count",
            title="Foundation Reliability Indicator (Usage Frequency)"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 📊 ENTERPRISE INSIGHT 4: Structural Diversity Index
    # =========================================================
    if not bldg.empty and not style.empty and not found.empty:
        diversity_data = pd.DataFrame({
            "Category": ["Building Types", "Architectural Styles", "Foundation Types"],
            "UniqueCount": [
                bldg["Type"].nunique(),
                style["Style"].nunique(),
                found["Foundation"].nunique()
            ]
        })

        fig = px.bar(
            diversity_data,
            x="Category",
            y="UniqueCount",
            color="UniqueCount",
            title="Structural Diversity Across Market"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Tab 2: Living Area & Floors
# ------------------------------
with tab2:
    st.markdown("## 🏢 Space Utilization — Enterprise Insights")

    # EXISTING VISUALS
    if not live.empty:
        fig = px.scatter(
            live,
            x="Above Ground Living Area",
            y="House Sale Price",
            color="Overall Material Quality",
            size="Total Basement Area",
            opacity=0.6,
            title="Living Area vs Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    if not floor.empty:
        fig = px.scatter(
            floor,
            x="Total Floors",
            y="House Sale Price",
            opacity=0.5,
            title="Floors vs Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 💰 ENTERPRISE INSIGHT 1: Price per Sq Ft Efficiency
    # =========================================================
    if not live.empty:
        live["PricePerSqFt"] = (
            live["House Sale Price"] /
            live["Above Ground Living Area"]
        )

        fig = px.scatter(
            live,
            x="Above Ground Living Area",
            y="PricePerSqFt",
            color="PricePerSqFt",
            opacity=0.6,
            title="Space Efficiency — Price per Sq Ft"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏆 ENTERPRISE INSIGHT 2: Luxury Segment Detection
    # =========================================================
    if not live.empty:
        luxury = live[
            live["House Sale Price"] >
            live["House Sale Price"].quantile(0.85)
        ]

        fig = px.scatter(
            luxury,
            x="Above Ground Living Area",
            y="House Sale Price",
            size="Total Basement Area",
            color="House Sale Price",
            title="Luxury Property Cluster"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏗️ ENTERPRISE INSIGHT 3: Basement ROI Impact
    # =========================================================
    if not live.empty:
        fig = px.scatter(
            live,
            x="Total Basement Area",
            y="House Sale Price",
            color="Total Basement Area",
            opacity=0.6,
            title="Basement Size Impact on Property Value"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 📈 ENTERPRISE INSIGHT 4: Floor Premium Analysis
    # =========================================================
    if not floor.empty:
        floor_avg = (
            floor.groupby("Total Floors")["House Sale Price"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            floor_avg,
            x="Total Floors",
            y="House Sale Price",
            color="House Sale Price",
            title="Average Price by Number of Floors"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 📊 ENTERPRISE INSIGHT 5: Size vs Quality vs Price Map
    # =========================================================
    if not live.empty:
        fig = px.scatter(
            live,
            x="Above Ground Living Area",
            y="House Sale Price",
            size="Total Basement Area",
            color="Overall Material Quality",
            hover_data=["Total Basement Area"],
            title="Integrated Value Map: Size + Quality + Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Tab 3: Bedrooms & Bathrooms
# ------------------------------
# ------------------------------
# Tab 3: Bedrooms & Bathrooms
# ------------------------------
with tab3:
    st.markdown("## 🏡 Family Space Analytics — Enterprise Insights")

    # EXISTING VISUALS
    if not bed.empty:
        fig = px.bar(
            bed,
            x="Bedrooms Above Ground",
            y="House Sale Price",
            title="Price by Number of Bedrooms"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    if not bath.empty:
        fig = px.bar(
            bath,
            x="Full Bathrooms",
            y="House Sale Price",
            title="Price by Number of Bathrooms"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 💰 ENTERPRISE INSIGHT 1: Price Premium per Extra Bedroom
    # =========================================================
    if not bed.empty:
        bed_sorted = bed.sort_values("Bedrooms Above Ground")
        bed_sorted["BedroomPremium"] = bed_sorted["House Sale Price"].diff()

        fig = px.bar(
            bed_sorted,
            x="Bedrooms Above Ground",
            y="BedroomPremium",
            color="BedroomPremium",
            title="Marginal Value of Additional Bedrooms"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🛁 ENTERPRISE INSIGHT 2: Bathroom Value Growth
    # =========================================================
    if not bath.empty:
        bath_sorted = bath.sort_values("Full Bathrooms")
        bath_sorted["BathPremium"] = bath_sorted["House Sale Price"].diff()

        fig = px.bar(
            bath_sorted,
            x="Full Bathrooms",
            y="BathPremium",
            color="BathPremium",
            title="Marginal Value of Additional Bathrooms"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏆 ENTERPRISE INSIGHT 3: Optimal Bedroom Count (Peak Value)
    # =========================================================
    if not bed.empty:
        fig = px.line(
            bed.sort_values("Bedrooms Above Ground"),
            x="Bedrooms Above Ground",
            y="House Sale Price",
            markers=True,
            title="Optimal Bedroom Count vs Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 📈 ENTERPRISE INSIGHT 4: Optimal Bathroom Count
    # =========================================================
    if not bath.empty:
        fig = px.line(
            bath.sort_values("Full Bathrooms"),
            x="Full Bathrooms",
            y="House Sale Price",
            markers=True,
            title="Optimal Bathroom Count vs Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏠 ENTERPRISE INSIGHT 5: Family Home Demand Map
    # =========================================================
    if not bed.empty:
        fig = px.scatter(
            bed,
            x="Bedrooms Above Ground",
            y="House Sale Price",
            size="House Sale Price",
            color="House Sale Price",
            title="Demand Map by Bedroom Count"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# ------------------------------
# Tab 4: Garage
# ------------------------------
# ------------------------------
# Tab 4: Garage
# ------------------------------
with tab4:
    st.markdown("## 🚗 Garage Value Analytics — Enterprise Insights")

    # EXISTING VISUAL
    if not gar.empty:
        fig = px.bar(
            gar,
            x="Garage Capacity Cars",
            y="House Sale Price",
            title="Price by Garage Capacity"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 💰 ENTERPRISE INSIGHT 1: Price Premium per Extra Car Space
    # =========================================================
    if not gar.empty:
        gar_sorted = gar.sort_values("Garage Capacity Cars")
        gar_sorted["GaragePremium"] = (
            gar_sorted["House Sale Price"].diff()
        )

        fig = px.bar(
            gar_sorted,
            x="Garage Capacity Cars",
            y="GaragePremium",
            color="GaragePremium",
            title="Marginal Value of Additional Garage Space"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏆 ENTERPRISE INSIGHT 2: Optimal Garage Size (Peak Value)
    # =========================================================
    if not gar.empty:
        fig = px.line(
            gar.sort_values("Garage Capacity Cars"),
            x="Garage Capacity Cars",
            y="House Sale Price",
            markers=True,
            title="Optimal Garage Capacity vs Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 📈 ENTERPRISE INSIGHT 3: Demand Map by Garage Size
    # =========================================================
    if not gar.empty:
        fig = px.scatter(
            gar,
            x="Garage Capacity Cars",
            y="House Sale Price",
            size="House Sale Price",
            color="House Sale Price",
            title="Buyer Demand Map by Garage Capacity"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # 🏡 ENTERPRISE INSIGHT 4: High-End Property Indicator
    # =========================================================
    if not gar.empty:
        luxury_gar = gar[
            gar["House Sale Price"] >
            gar["House Sale Price"].quantile(0.85)
        ]

        fig = px.scatter(
            luxury_gar,
            x="Garage Capacity Cars",
            y="House Sale Price",
            color="House Sale Price",
            size="House Sale Price",
            title="Luxury Homes by Garage Capacity"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Tab 5: Outdoor Features
# ------------------------------
with tab5:
    if not out.empty:
        fig1 = px.scatter(
            out,
            x="Wood Deck Area",
            y="House Sale Price",
            opacity=0.5
        )
        fig1 = apply_dark_navy_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.scatter(
            out,
            x="Open Porch Area",
            y="House Sale Price",
            opacity=0.5
        )
        fig2 = apply_dark_navy_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        # =========================================================
        # 🌟 ENTERPRISE INSIGHT 1: Outdoor Space ROI Curve
        # =========================================================
        outdoor = out.copy()
        outdoor["Total Outdoor Area"] = (
            outdoor["Wood Deck Area"] +
            outdoor["Open Porch Area"]
        )

        fig3 = px.scatter(
            outdoor,
            x="Total Outdoor Area",
            y="House Sale Price",
            color="Total Outdoor Area",
            size="Total Outdoor Area",
            title="Total Outdoor Living Space vs Price"
        )
        fig3 = apply_dark_navy_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    if not pool.empty:
        fig = px.bar(
            pool,
            x="Pool Quality",
            y="House Sale Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # =========================================================
        # 🏆 ENTERPRISE INSIGHT 2: Pool Luxury Premium Map
        # =========================================================
        luxury_pool = pool[
            pool["House Sale Price"] >
            pool["House Sale Price"].quantile(0.85)
        ]

        fig4 = px.scatter(
            luxury_pool,
            x="Pool Quality",
            y="House Sale Price",
            color="House Sale Price",
            size="House Sale Price",
            title="Luxury Homes by Pool Quality"
        )
        fig4 = apply_dark_navy_layout(fig4)
        st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🏗️ Feature Categories")
    st.markdown("""
    - Building & Design  
    - Space & Area  
    - Room Configuration  
    - Garage & Parking  
    - Outdoor Features  
    """)
    st.markdown("---")
    st.success(f"Connected to: {API_BASE}")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()