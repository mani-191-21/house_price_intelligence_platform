import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="House Price Intelligence Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# GLOBAL DARK ENTERPRISE STYLE
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Background */
html, body, [data-testid="stAppViewContainer"], .block-container {
    background-color: #0f172a !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* ---------------- HERO ---------------- */
.green-hero {
    background: linear-gradient(135deg, #14532d 0%, #16a34a 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(22,163,74,0.4);
}

.green-title { font-size: 3.5rem; font-weight: 700; color: white; }
.green-subtitle { font-size: 1.2rem; opacity: 0.9; color: white; }

/* ---------------- METRIC CARDS ---------------- */
.stat {
    background: #1e293b;
    padding: 1.4rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
}

.stat-delta {
    font-size: 0.9rem;
    font-weight: 600;
}

.positive { color: #22c55e; }
.negative { color: #ef4444; }

/* ---------------- NAV CARDS ---------------- */
.card {
    background: #1e293b;
    padding: 1.4rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f1f5f9;
}

.card-icon { font-size: 1.6rem; }

/* ---------------- POPUP PANEL ---------------- */
.enterprise-popup {
    background: linear-gradient(135deg, #0b1220 0%, #1e293b 100%);
    border-radius: 22px;
    padding: 2.5rem 2rem;
    margin: 2rem 0;
    color: #e2e8f0;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    border: 1px solid rgba(148,163,184,0.15);
}

.popup-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 1.5rem;
}

.popup-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.4rem;
}

.popup-item {
    background: rgba(30,41,59,0.7);
    padding: 1.2rem;
    border-radius: 14px;
    border-left: 4px solid #16a34a;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #14532d 0%, #16a34a 100%);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
}

[data-testid="metric-container"] {
    background-color: #1e293b !important;
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown("""
<div class="green-hero">
    <div class="green-title">🏡 House Price Intelligence</div>
    <div class="green-subtitle">
        Smart Market Analytics • Real Estate Insights • Predictive Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# MARKET SNAPSHOT
# ------------------------------------------------------------
st.subheader("Market Snapshot")

cols = st.columns(4)

metrics = [
    ("Avg Property Price", "$251.5M", "+4.3%"),
    ("Active Listings", "3,420", "+120"),
    ("Days on Market", "42 days", "-5 days"),
    ("Avg Rental Yield", "3.8%", "+0.4%")
]

for col, (label, value, delta) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="stat">
            <div class="stat-number">{value}</div>
            <div style="color:#94a3b8">{label}</div>
            <div class="stat-delta positive">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------
st.subheader("Explore Modules")

nav_items = [
    ("🔮 Price Prediction", "Prediction"),
    ("📈 Price Trends", "Price Trends"),
    ("🗺️ Neighborhood", "Neighborhood"),
    ("🏠 Key Features", "Features"),
    ("⭐ Quality Rating", "Quality"),
    ("💧 Utilities", "Utilities"),
    ("🗺️ Geographic Maps", "Maps")
]

nav_cols = st.columns(4)

for i, (title, page) in enumerate(nav_items):
    with nav_cols[i % 4]:
        st.markdown(f"""
        <div class="card">
            <div class="card-icon">{title.split()[0]}</div>
            <div class="card-title">{title.split(' ',1)[1]}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open →", key=page):
            st.switch_page(f"pages/{page}.py")

st.markdown("---")


# ------------------------------------------------------------
# EXECUTIVE POPUP
# ------------------------------------------------------------
st.markdown("""
<div class="enterprise-popup">
<div class="popup-title">🧠 Executive Market Intelligence</div>

<div class="popup-grid">

<div class="popup-item">
📈 <b>Demand Acceleration:</b><br>
Premium neighborhoods are experiencing <b>18–25% faster absorption rates</b>
than the city average, driven by limited supply and affluent buyer activity.<br>
<span style="color:#94a3b8">Implication: Sellers hold strong pricing power in top-tier zones.</span>
</div>

<div class="popup-item">
💰 <b>Capital Growth Hotspots:</b><br>
Properties within <b>3–5 km of major employment hubs</b> are appreciating up to
<b>1.6× faster</b> than peripheral locations.<br>
<span style="color:#94a3b8">Implication: Long-term investors should prioritize transit-connected corridors.</span>
</div>

<div class="popup-item">
🏗️ <b>Development Opportunity:</b><br>
Undersupplied suburban zones show a <b>housing deficit of ~12–15%</b>,
creating favorable conditions for new residential projects.<br>
<span style="color:#94a3b8">Implication: Early-stage land acquisition can yield superior ROI.</span>
</div>

<div class="popup-item">
🏆 <b>Luxury Segment Stability:</b><br>
High-end properties demonstrate <b>lower price volatility</b> and
retain value during downturns due to cash-driven purchases.<br>
<span style="color:#94a3b8">Implication: Serves as a defensive asset class for wealthy portfolios.</span>
</div>

<div class="popup-item">
🏙️ <b>Urban Migration Trend:</b><br>
Population inflow toward mixed-use urban centers is increasing rental demand
by <b>8–12% annually</b>.<br>
<span style="color:#94a3b8">Implication: Rental-focused investments outperform speculative holdings.</span>
</div>

<div class="popup-item">
🚆 <b>Infrastructure Impact:</b><br>
Upcoming transit projects historically boost nearby property values by
<b>20–35% within 5 years</b> of completion.<br>
<span style="color:#94a3b8">Implication: Strategic pre-infrastructure investment offers outsized gains.</span>
</div>

</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# EXECUTIVE BRIEFINGS
# ------------------------------------------------------------
st.subheader("🧠 Executive Intelligence Briefings")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("🚀 Market Momentum"):
        st.write("Limited supply + high demand → continued price growth.")

with col2:
    with st.expander("💰 Investment Signal"):
        st.write("Mid-tier zones outperform luxury in rental ROI.")

with col3:
    with st.expander("⚠️ Risk Advisory"):
        st.write("Rising interest rates may slow leveraged markets.")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## Control Panel")

    st.selectbox("User Role",
        ["Investor", "Portfolio Manager", "Developer", "Analyst"])

    st.selectbox("Time Horizon",
        ["Last Quarter", "6 Months", "12 Months", "3 Years"])

    st.metric("Portfolio Value", "₹14.2 Cr", "+6.2%")
    st.metric("Occupancy", "92%", "+3%")
    st.metric("Net Yield", "4.1%", "+0.5%")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")

st.markdown(f"""
<div style='text-align:center;color:#64748b;padding:2rem'>
<strong>House Price Intelligence Platform</strong><br>
Strategic real estate decisions • © {datetime.now().year}
</div>
""", unsafe_allow_html=True)