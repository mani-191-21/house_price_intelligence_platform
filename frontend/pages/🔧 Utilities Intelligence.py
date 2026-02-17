import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

API_BASE = "http://localhost:8000/api"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Utilities Intelligence",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    <div class="modern-orange-title">🏠 Property Feature Intelligence</div>
    <div class="modern-orange-subtitle">
        Advanced Property Insights • Structural Analytics • Feature Impact Analysis
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SAFE API LOADER
# ---------------------------------------------------
def load_api(endpoint):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=8)
        r.raise_for_status()
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()
    
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

# ---------------------------------------------------
# SIDEBAR CONTROLS (INTERACTIVE)
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Dashboard Controls")

    section_select = st.multiselect(
        "Select Sections",
        ["Utility Impact", "Garage Analysis", "Summary Table"],
        default=["Utility Impact", "Garage Analysis", "Summary Table"]
    )

    min_price = st.number_input("Minimum Price Filter", value=0)

    st.markdown("---")
    st.markdown("### 📊 Dashboard Theme")
    st.write("Purple & Green Modern UI")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
central_air = load_api("/utilities/central-air")
heating_qc = load_api("/utilities/heating-quality")
electrical = load_api("/utilities/electrical")
garage_age = load_api("/utilities/garage-age")

try:
    utilities_summary = requests.get(f"{API_BASE}/utilities/summary").json()
except:
    utilities_summary = {}

# Apply Price Filter
def filter_price(df):
    if not df.empty and "House Sale Price" in df.columns:
        return df[df["House Sale Price"] >= min_price]
    return df

central_air = filter_price(central_air)
heating_qc = filter_price(heating_qc)
electrical = filter_price(electrical)
garage_age = filter_price(garage_age)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if not central_air.empty:
        st.markdown(f"""
        <div class="kpi-card">
            Avg Central Air Price<br>
            ${int(central_air["House Sale Price"].mean()):,}
        </div>
        """, unsafe_allow_html=True)

with col2:
    if not heating_qc.empty:
        st.markdown(f"""
        <div class="kpi-card">
            Avg Heating Quality Price<br>
            ${int(heating_qc["House Sale Price"].mean()):,}
        </div>
        """, unsafe_allow_html=True)

with col3:
    if not electrical.empty:
        st.markdown(f"""
        <div class="kpi-card">
            Avg Electrical System Price<br>
            ${int(electrical["House Sale Price"].mean()):,}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------
# UTILITY IMPACT SECTION
# ---------------------------------------------------
if "Utility Impact" in section_select:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🔌 Utility Impact on Pricing")

    u1, u2, u3 = st.columns(3)

    with u1:
        if not central_air.empty:
            fig = px.bar(
                central_air,
                x="Central Air Conditioning",
                y="House Sale Price",
                color="House Sale Price",
                color_continuous_scale="Greens"
            )
            fig = apply_dark_navy_layout(fig)
            fig.update_layout(height=320)
            st.plotly_chart(fig, use_container_width=True)

    with u2:
        if not heating_qc.empty:
            fig = px.bar(
                heating_qc,
                x="Heating Quality",
                y="House Sale Price",
                color="House Sale Price",
                color_continuous_scale="Purples"
            )
            fig = apply_dark_navy_layout(fig)
            fig.update_layout(height=320)
            st.plotly_chart(fig, use_container_width=True)

    with u3:
        if not electrical.empty:
            fig = px.bar(
                electrical,
                x="Electrical System",
                y="House Sale Price",
                color="House Sale Price",
                color_continuous_scale="Teal"
            )
            fig = apply_dark_navy_layout(fig)
            fig.update_layout(height=320)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# GARAGE ANALYSIS
# ---------------------------------------------------
if "Garage Analysis" in section_select:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🚗 Garage Construction vs Price")

    if not garage_age.empty:
        fig = px.scatter(
            garage_age,
            x="Garage Construction Year",
            y="House Sale Price",
            size="Garage Capacity Cars",
            color="Garage Capacity Cars",
            color_continuous_scale="Viridis"
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Garage Data Available")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# FEATURE PREMIUM ANALYSIS
# ---------------------------------------------------
st.subheader("💰 Utility Feature Price Premium")

if not central_air.empty:
    baseline = central_air["House Sale Price"].mean()

    premium = central_air.groupby("Central Air Conditioning")["House Sale Price"].mean().reset_index()
    premium["Premium vs Avg"] = premium["House Sale Price"] - baseline

    fig = px.bar(
        premium,
        x="Central Air Conditioning",
        y="Premium vs Avg",
        color="Premium vs Avg",
        color_continuous_scale="RdYlGn"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# HEATING QUALITY RANKING
# ---------------------------------------------------
st.subheader("🏆 Heating Quality Ranking")

if not heating_qc.empty:
    ranking = heating_qc.groupby("Heating Quality")["House Sale Price"].mean().sort_values().reset_index()

    fig = px.bar(
        ranking,
        x="House Sale Price",
        y="Heating Quality",
        orientation="h",
        color="House Sale Price",
        color_continuous_scale="Purples"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# ELECTRICAL QUALITY VALUE MAP
# ---------------------------------------------------
st.subheader("⚡ Electrical System Value Map")

if not electrical.empty:
    value_map = electrical.groupby("Electrical System")["House Sale Price"].agg(["mean", "count"]).reset_index()

    fig = px.scatter(
        value_map,
        x="count",
        y="mean",
        size="mean",
        color="mean",
        hover_name="Electrical System",
        color_continuous_scale="Teal"
    )

    fig.update_xaxes(title="Number of Houses")
    fig.update_yaxes(title="Average Sale Price")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------
# GARAGE MODERNITY SCORE
# ---------------------------------------------------
st.subheader("🆕 Garage Modernity Impact")

if not garage_age.empty:
    current_year = 2025
    garage_age["Garage Age"] = current_year - garage_age["Garage Construction Year"]

    bins = [0, 10, 25, 50, 200]
    labels = ["New", "Recent", "Old", "Very Old"]

    garage_age["Garage Category"] = pd.cut(
        garage_age["Garage Age"],
        bins=bins,
        labels=labels
    )

    modernity = garage_age.groupby("Garage Category")["House Sale Price"].mean().reset_index()

    fig = px.bar(
        modernity,
        x="Garage Category",
        y="House Sale Price",
        color="House Sale Price",
        color_continuous_scale="Viridis"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# ROI: CENTRAL AIR UPGRADE VALUE
# ---------------------------------------------------
st.subheader("💸 ROI Insight — Central Air Upgrade Value")

if not central_air.empty:
    air_price = central_air.groupby("Central Air Conditioning")["House Sale Price"].mean()

    if "Yes" in air_price and "No" in air_price:
        roi = air_price["Yes"] - air_price["No"]

        st.metric(
            label="Estimated Value Added by Central Air",
            value=f"${int(roi):,}"
        )

        roi_df = air_price.reset_index()

        fig = px.bar(
            roi_df,
            x="Central Air Conditioning",
            y="House Sale Price",
            color="House Sale Price",
            color_continuous_scale="Greens"
        )

        fig = apply_dark_navy_layout(fig)
        fig.update_layout(height=340)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# MARKET DEMAND: FEATURE POPULARITY IN HIGH-PRICE HOMES
# ---------------------------------------------------
st.subheader("🔥 Market Demand — High-Value Feature Presence")

if not electrical.empty:
    threshold = electrical["House Sale Price"].quantile(0.75)

    premium_homes = electrical[electrical["House Sale Price"] >= threshold]

    demand = premium_homes["Electrical System"].value_counts().reset_index()
    demand.columns = ["Electrical System", "Count"]

    fig = px.bar(
        demand,
        x="Electrical System",
        y="Count",
        color="Count",
        color_continuous_scale="Plasma"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PRICE SENSITIVITY — GARAGE CAPACITY
# ---------------------------------------------------
st.subheader("📊 Price Sensitivity — Garage Capacity Impact")

if not garage_age.empty:
    sensitivity = garage_age.groupby("Garage Capacity Cars")["House Sale Price"].mean().reset_index()

    fig = px.line(
        sensitivity,
        x="Garage Capacity Cars",
        y="House Sale Price",
        markers=True
    )

    fig.update_yaxes(title="Average Sale Price")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# OVERALL UTILITY SCORECARD
# ---------------------------------------------------
st.subheader("📊 Utility Contribution Score")

scores = {}

if not central_air.empty:
    scores["Central Air"] = central_air["House Sale Price"].mean()

if not heating_qc.empty:
    scores["Heating Quality"] = heating_qc["House Sale Price"].mean()

if not electrical.empty:
    scores["Electrical"] = electrical["House Sale Price"].mean()

if scores:
    score_df = pd.DataFrame({
        "Utility": list(scores.keys()),
        "Avg Price": list(scores.values())
    })

    fig = px.bar(
        score_df,
        x="Utility",
        y="Avg Price",
        color="Avg Price",
        color_continuous_scale="Turbo"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# SUMMARY TABLE
# ---------------------------------------------------
if "Summary Table" in section_select:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📋 Utilities Summary")

    if utilities_summary:
        util_df = pd.DataFrame(utilities_summary).fillna(0)
        st.dataframe(util_df.T, use_container_width=True)
    else:
        st.warning("No Summary Data Available")

    st.markdown('</div>', unsafe_allow_html=True)