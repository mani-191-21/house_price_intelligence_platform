import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(page_title="Neighborhood Analysis", page_icon="🗺️", layout="wide")

if 'api_base' not in st.session_state:
    st.session_state.api_base = "http://localhost:8000/api"

API_BASE = st.session_state.api_base

# Custom CSS
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
# ---------------------------------------------------
# MODERN PURPLE / GREEN THEME
# ---------------------------------------------------
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
.modern-orange-hero {
    background: linear-gradient(135deg, #ff7f50 0%, #ffa500 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(255, 165, 0, 0.5); /* modern orange shadow */
}

.modern-orange-title {
    font-size: 3.5rem;
    font-weight: 700;
}

.modern-orange-subtitle {
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

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------
st.markdown("""
<div class="modern-orange-hero">
    <div class="modern-orange-title">🏠 Neighborhood and Loacation Analysis</div>
    <div class="modern-orange-subtitle">
        Advanced Property Insights • Structural Analytics • Feature Impact Analysis
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data(ttl=600)
def load_location_data():
    try:
        response = requests.get(f"{API_BASE}/location/neighborhood", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

with st.spinner("Loading neighborhood data..."):
    data = load_location_data()

if not data:
    st.warning("⚠️ Unable to load neighborhood data. Please ensure the backend API is running.")
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

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏘️ Neighborhood Comparison",
    "📍 Zoning Impact",
    "📏 Lot Characteristics",
    "🚗 Access & Infrastructure",
    "🧠 Intelligence Infrastructure"
])

# TAB 1: Neighborhood Comparison
with tab1:
    if "neighborhood_comparison" in data:
        neighborhoods = pd.DataFrame(data["neighborhood_comparison"])
        
        st.markdown("## 🏘️ Neighborhood Comparison — Enterprise Insights")

        # =====================================================
        # 1️⃣ Top Neighborhood Price Comparison (Existing)
        # =====================================================
        fig = px.bar(
            neighborhoods.head(15),
            x="Neighborhood Name",
            y="AvgPrice",
            color="MedianPrice",
            title="Top 15 Neighborhoods by Average Price",
            labels={"AvgPrice": "Average Price ($)", "MedianPrice": "Median Price ($)"},
            color_continuous_scale="Viridis"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # 2️⃣ Price Stability Index
        # =====================================================
        neighborhoods["Stability"] = neighborhoods["MedianPrice"] / neighborhoods["AvgPrice"]

        fig = px.bar(
            neighborhoods.sort_values("Stability", ascending=False).head(12),
            x="Neighborhood Name",
            y="Stability",
            color="Stability",
            title="Price Stability Index (Safer Investments)"
        )

        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # 3️⃣ Median vs Average Price Relationship
        # =====================================================
        fig = px.scatter(
            neighborhoods,
            x="MedianPrice",
            y="AvgPrice",
            size="TotalSales",
            hover_name="Neighborhood Name",
            title="Median vs Average Price — Luxury Skew Detection"
        )

        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # 4️⃣ High-Demand Premium Zones
        # =====================================================
        premium = neighborhoods[
            neighborhoods["AvgPrice"] > neighborhoods["AvgPrice"].mean()
        ]

        fig = px.bar(
            premium.sort_values("TotalSales", ascending=False).head(10),
            x="Neighborhood Name",
            y="TotalSales",
            color="AvgPrice",
            title="High-Demand Premium Neighborhoods"
        )

        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # 5️⃣ Undervalued Opportunity Map
        # =====================================================
        fig = px.scatter(
            neighborhoods,
            x="AvgPrice",
            y="TotalSales",
            color="MedianPrice",
            size="TotalSales",
            hover_name="Neighborhood Name",
            title="Undervalued Investment Opportunity Map"
        )

        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # 6️⃣ Sales Concentration Curve
        # =====================================================
        df_sorted = neighborhoods.sort_values("TotalSales", ascending=False)
        df_sorted["Cumulative"] = df_sorted["TotalSales"].cumsum()

        fig = px.line(
            df_sorted,
            x="Neighborhood Name",
            y="Cumulative",
            markers=True,
            title="Sales Concentration Curve (Market Dominance)"
        )

        fig = apply_dark_navy_layout(fig)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


        # =====================================================
        # Detailed Table (Optional — keep or remove)
        # =====================================================
        st.markdown("### 📊 Detailed Neighborhood Statistics")

        st.dataframe(
            neighborhoods.style.format({
                "AvgPrice": "${:,.0f}",
                "MedianPrice": "${:,.0f}",
                "TotalSales": "{:,}"
            }),
            use_container_width=True
        )

# TAB 2: Zoning Impact
with tab2:
    if "zoning_impact" in data:
        zoning = pd.DataFrame(data["zoning_impact"])

        st.markdown("## 📍 Zoning Impact — Enterprise Insights")

        # 1️⃣ Distribution by Zoning Type
        fig = px.pie(
            zoning,
            names="Zoning Classification",
            values="TotalSales",
            title="Market Share by Zoning",
            hole=0.4
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 2️⃣ Average Price by Zoning
        fig = px.bar(
            zoning,
            x="Zoning Classification",
            y="AvgPrice",
            color="AvgPrice",
            title="Average Property Price by Zoning",
            color_continuous_scale="RdYlGn"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 3️⃣ Demand vs Price Map
        fig = px.scatter(
            zoning,
            x="TotalSales",
            y="AvgPrice",
            size="TotalSales",
            color="MedianPrice",
            hover_name="Zoning Classification",
            title="Demand vs Price by Zoning"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 4️⃣ Premium Zoning Types
        premium = zoning.sort_values("AvgPrice", ascending=False).head(8)

        fig = px.bar(
            premium,
            x="Zoning Classification",
            y="AvgPrice",
            color="MedianPrice",
            title="Premium Zoning Segments"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 5️⃣ Price Stability by Zoning
        zoning["Stability"] = zoning["MedianPrice"] / zoning["AvgPrice"]

        fig = px.bar(
            zoning.sort_values("Stability", ascending=False),
            x="Zoning Classification",
            y="Stability",
            color="Stability",
            title="Price Stability by Zoning"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# TAB 3: Lot Characteristics
with tab3:
    st.markdown("## 📏 Lot Characteristics — Enterprise Insights")

    # 1️⃣ Lot Frontage vs Price
    if "lot_frontage_vs_price" in data:
        lot_frontage = pd.DataFrame(data["lot_frontage_vs_price"])

        fig = px.scatter(
            lot_frontage,
            x="Lot Frontage Length",
            y="House Sale Price",
            opacity=0.5,
            title="Frontage Impact on Property Price"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # 2️⃣ Lot Area Impact
    if "lot_area_impact" in data:
        lot_area = pd.DataFrame(data["lot_area_impact"])

        fig = px.bar(
            lot_area,
            x="Lot Area Range",
            y="AvgPrice",
            color="Count",
            title="Average Price by Lot Size",
            color_continuous_scale="Blues"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 3️⃣ Demand vs Lot Size
        fig = px.scatter(
            lot_area,
            x="Lot Area Range",
            y="Count",
            size="Count",
            color="AvgPrice",
            title="Demand by Lot Size"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 4️⃣ Premium Lot Segments
        premium = lot_area.sort_values("AvgPrice", ascending=False).head(8)

        fig = px.bar(
            premium,
            x="Lot Area Range",
            y="AvgPrice",
            color="AvgPrice",
            title="Premium Lot Size Segments"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 5️⃣ Lot Size Efficiency (Price per Sale)
        lot_area["Efficiency"] = lot_area["AvgPrice"] / lot_area["Count"]

        fig = px.bar(
            lot_area.sort_values("Efficiency", ascending=False),
            x="Lot Area Range",
            y="Efficiency",
            color="Efficiency",
            title="Lot Size Investment Efficiency"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# TAB 4: Access & Infrastructure
with tab4:
    st.markdown("## 🚗 Access & Infrastructure — Enterprise Insights")

    # 1️⃣ Alley Access Impact
    if "alley_access_analysis" in data:
        alley = pd.DataFrame(data["alley_access_analysis"])

        fig = px.bar(
            alley,
            x="Alley Access",
            y="AvgPrice",
            color="Count",
            title="Price by Alley Access Type",
            color_continuous_scale="Greens"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 2️⃣ Demand by Alley Access
        fig = px.pie(
            alley,
            names="Alley Access",
            values="Count",
            hole=0.4,
            title="Demand Distribution by Alley Access"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # 3️⃣ Paved Driveway Premium
    if "paved_drive_premium" in data:
        paved = pd.DataFrame(data["paved_drive_premium"])

        fig = px.bar(
            paved,
            x="Driveway Paving",
            y="AvgPrice",
            color="MedianPrice",
            title="Average Price by Driveway Type",
            color_continuous_scale="Oranges"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 4️⃣ Price Stability by Driveway Type
        paved["Stability"] = paved["MedianPrice"] / paved["AvgPrice"]

        fig = px.bar(
            paved,
            x="Driveway Paving",
            y="Stability",
            color="Stability",
            title="Price Stability by Driveway Type"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 5️⃣ Demand vs Price by Infrastructure
        fig = px.scatter(
            paved,
            x="AvgPrice",
            y="MedianPrice",
            size="AvgPrice",
            color="AvgPrice",
            hover_name="Driveway Paving",
            title="Infrastructure Premium Map"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# =========================================================
# TAB 5: Intelligence Infrastructure
# =========================================================
with tab5:
    st.markdown("## 🧠 Intelligence Infrastructure — AI Market Insights")

    # Assume neighborhood data exists
    if "neighborhood_comparison" in data:
        intel = pd.DataFrame(data["neighborhood_comparison"])

        # -------------------------------------------------
        # 1️⃣ Investment Opportunity Matrix
        # Low price + high sales = best investment zones
        # -------------------------------------------------
        fig1 = px.scatter(
            intel,
            x="AvgPrice",
            y="TotalSales",
            size="TotalSales",
            color="AvgPrice",
            hover_name="Neighborhood Name",
            title="Investment Opportunity Matrix"
        )
        fig1 = apply_dark_navy_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        # -------------------------------------------------
        # 2️⃣ Market Concentration (Pareto Analysis)
        # Shows which neighborhoods dominate sales
        # -------------------------------------------------
        pareto = intel.sort_values(
            "TotalSales", ascending=False
        ).copy()

        pareto["CumulativeShare"] = (
            pareto["TotalSales"].cumsum() /
            pareto["TotalSales"].sum() * 100
        )

        fig2 = px.line(
            pareto,
            x="Neighborhood Name",
            y="CumulativeShare",
            markers=True,
            title="Market Concentration Curve (Pareto)"
        )
        fig2 = apply_dark_navy_layout(fig2)
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

        # -------------------------------------------------
        # 3️⃣ Price Stability Index
        # Median vs Average price gap
        # -------------------------------------------------
        intel["StabilityIndex"] = (
            intel["MedianPrice"] / intel["AvgPrice"]
        )

        fig3 = px.bar(
            intel.sort_values("StabilityIndex"),
            x="Neighborhood Name",
            y="StabilityIndex",
            color="StabilityIndex",
            title="Price Stability by Neighborhood"
        )
        fig3 = apply_dark_navy_layout(fig3)
        fig3.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

        # -------------------------------------------------
        # 4️⃣ Premium vs Affordable Segmentation
        # Detect luxury clusters
        # -------------------------------------------------
        threshold = intel["AvgPrice"].median()

        premium = intel.copy()
        premium["Segment"] = premium["AvgPrice"].apply(
            lambda x: "Premium" if x > threshold else "Affordable"
        )

        fig4 = px.pie(
            premium,
            names="Segment",
            values="TotalSales",
            hole=0.4,
            title="Premium vs Affordable Market Share"
        )
        fig4 = apply_dark_navy_layout(fig4)
        st.plotly_chart(fig4, use_container_width=True)

        # -------------------------------------------------
        # 5️⃣ High-Demand Premium Zones
        # Expensive AND high sales → top targets
        # -------------------------------------------------
        fig5 = px.scatter(
            intel,
            x="AvgPrice",
            y="TotalSales",
            color="MedianPrice",
            size="AvgPrice",
            hover_name="Neighborhood Name",
            title="High-Demand Premium Neighborhoods"
        )
        fig5 = apply_dark_navy_layout(fig5)
        st.plotly_chart(fig5, use_container_width=True)


# Summary insights
st.markdown("---")
st.markdown("## 💡 Key Location Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🏘️ Neighborhood Matters**
    - Location is a primary price driver
    - Premium neighborhoods command 2-3x average
    - School districts impact significantly
    """)

with col2:
    st.success("""
    **📍 Zoning Considerations**
    - Residential zoning most common
    - Commercial zones vary widely
    - Mixed-use areas growing
    """)

with col3:
    st.warning("""
    **📏 Lot Characteristics**
    - Larger lots = higher prices
    - Frontage impacts curb appeal
    - Corner lots command premium
    """)

# Sidebar without metrics
# Sidebar with filter categories
with st.sidebar:
    st.markdown("## 🗺️ Location Filters")
    st.info("Select categories to explore neighborhood data")
    
    st.markdown("---")
    
    # Neighborhood filter
    if "neighborhood_comparison" in data:
        neighborhoods = [row["Neighborhood Name"] for row in data["neighborhood_comparison"]]
        selected_neighborhoods = st.multiselect(
            "🏘️ Select Neighborhood(s)",
            options=neighborhoods,
            default=neighborhoods[:5]  # default first 5
        )

    # Zoning filter
    if "zoning_impact" in data:
        zoning_types = [row["Zoning Classification"] for row in data["zoning_impact"]]
        selected_zoning = st.multiselect(
            "📍 Select Zoning Type(s)",
            options=zoning_types,
            default=zoning_types[:3]
        )

    # Lot area filter
    if "lot_area_impact" in data:
        lot_ranges = [row["Lot Area Range"] for row in data["lot_area_impact"]]
        selected_lot_range = st.selectbox(
            "📐 Lot Area Range",
            options=lot_ranges
        )

    # Alley access filter
    if "alley_access_analysis" in data:
        alley_types = [row["Alley Access"] for row in data["alley_access_analysis"]]
        selected_alley = st.selectbox(
            "🛣️ Alley Access Type",
            options=alley_types
        )

    # Driveway paving filter
    if "paved_drive_premium" in data:
        driveway_types = [row["Driveway Paving"] for row in data["paved_drive_premium"]]
        selected_driveway = st.selectbox(
            "🚗 Driveway Paving",
            options=driveway_types
        )

    # Refresh button
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()