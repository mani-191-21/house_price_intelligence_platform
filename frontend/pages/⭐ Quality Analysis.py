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
    page_title="Quality Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# BLACK & WHITE PREMIUM CSS
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
.red-pink-hero {
    background: linear-gradient(135deg, #ff4d6d 0%, #ff99ac 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(255, 77, 109, 0.5); /* matches red-pink theme */
}

.red-pink-title {
    font-size: 3.5rem;
    font-weight: 700;
}

.red-pink-subtitle {
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
# HERO HEADER (HIGHLIGHTED)
# ---------------------------------------------------
st.markdown("""
<div class="red-pink-hero">
    <div class="red-pink-title">🏠 Property Feature Intelligence</div>
    <div class="red-pink-subtitle">
        Material Quality Impact • Structural Condition • Component Performance • Construction Insights
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
# LOAD DATA
# ---------------------------------------------------
qual = load_api("/quality/overall")
cond = load_api("/quality/condition")
exterior = load_api("/quality/exterior")
kitchen = load_api("/quality/kitchen")
basement = load_api("/quality/basement")
fireplace = load_api("/quality/fireplace")
masonry = load_api("/quality/masonry")
ext_condition = load_api("/quality/exterior-condition")

# ---------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## Dashboard Controls")

    min_quality = st.slider("Minimum Overall Quality", 1, 10, 1)

    section_filter = st.multiselect(
        "Display Sections",
        [
            "Overall Quality",
            "Condition Distribution",
            "Component Breakdown",
            "Material Impact"
        ],
        default=[
            "Overall Quality",
            "Condition Distribution",
            "Component Breakdown",
            "Material Impact"
        ]
    )

    show_corr = st.checkbox("Show Correlation Metric", True)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
if not qual.empty:
    qual = qual[qual["Overall Material Quality"] >= min_quality]

# ---------------------------------------------------
# OVERALL QUALITY SECTION
# ---------------------------------------------------
if "Overall Quality" in section_filter:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🌟 Overall Quality Impact")

    if not qual.empty:
        fig = go.Figure(go.Bar(
            x=qual["Overall Material Quality"],
            y=qual["House Sale Price"]
        ))
        fig.update_layout(
            height=400,
            xaxis_title="Quality Rating (1-10)",
            yaxis_title="Average Price ($)"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

        if show_corr:
            corr = qual["Overall Material Quality"].corr(
                qual["House Sale Price"]
            )
            st.markdown(
                f'<div class="metric-card"><b>Correlation Strength:</b> {corr:.3f}</div>',
                unsafe_allow_html=True
            )
    else:
        st.warning("No data after applying filter.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# CONDITION DISTRIBUTION
# ---------------------------------------------------
if "Condition Distribution" in section_filter:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📊 Condition Distribution")

    if not cond.empty:
        fig = go.Figure(go.Bar(
            x=cond["Overall Condition Rating"],
            y=cond["Count"]
        ))
        fig.update_layout(
            height=400,
            xaxis_title="Condition Level",
            yaxis_title="Homes Count"
        )
        fig = apply_dark_navy_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No condition data available.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# COMPONENT BREAKDOWN
# ---------------------------------------------------
if "Component Breakdown" in section_filter:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🧩 Component Quality Breakdown")

    def show_pie(df, title):
        if df.empty:
            st.warning("No data")
            return
        fig = px.pie(
            df,
            names="Category",
            values="House Sale Price",
            hole=0.5
        )
        fig = apply_dark_navy_layout(fig)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_pie(exterior, "Exterior")

    with c2:
        show_pie(kitchen, "Kitchen")

    with c3:
        show_pie(basement, "Basement")

    with c4:
        show_pie(fireplace, "Fireplace")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# MATERIAL IMPACT
# ---------------------------------------------------
if "Material Impact" in section_filter:

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🧱 Material & Construction Impact")

    c5, c6 = st.columns(2)

    with c5:
        if not masonry.empty:
            fig = px.bar(
                masonry,
                x="Masonry Veneer Type",
                y="House Sale Price"
            )
            fig = apply_dark_navy_layout(fig)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No Masonry data")

    with c6:
        if not ext_condition.empty:
            fig = px.bar(
                ext_condition,
                x="Exterior Condition",
                y="House Sale Price"
            )
            fig = apply_dark_navy_layout(fig)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No Exterior Condition data")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# LUXURY QUALITY THRESHOLD
# ---------------------------------------------------
st.subheader("💎 Luxury Threshold — Quality vs Premium Pricing")

if not qual.empty:
    threshold = qual["House Sale Price"].quantile(0.9)

    qual["Luxury Tier"] = qual["House Sale Price"] >= threshold

    luxury = qual.groupby("Overall Material Quality")["Luxury Tier"].mean().reset_index()

    fig = px.line(
        luxury,
        x="Overall Material Quality",
        y="Luxury Tier",
        markers=True
    )

    fig.update_yaxes(title="Probability of Luxury Home")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# COMPONENT UPGRADE PRIORITY
# ---------------------------------------------------
st.subheader("🔧 Renovation Priority — Value Gain by Component")

components = {}

if not kitchen.empty:
    components["Kitchen"] = kitchen["House Sale Price"].mean()

if not exterior.empty:
    components["Exterior"] = exterior["House Sale Price"].mean()

if not basement.empty:
    components["Basement"] = basement["House Sale Price"].mean()

if not fireplace.empty:
    components["Fireplace"] = fireplace["House Sale Price"].mean()

if components:
    comp_df = pd.DataFrame({
        "Component": list(components.keys()),
        "Avg Price": list(components.values())
    }).sort_values("Avg Price", ascending=False)

    fig = px.bar(
        comp_df,
        x="Component",
        y="Avg Price",
        color="Avg Price",
        color_continuous_scale="Turbo"
    )

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# QUALITY PRICE PENALTY
# ---------------------------------------------------
st.subheader("⚠️ Price Penalty — Low Quality Homes")

if not qual.empty:
    low_quality = qual[qual["Overall Material Quality"] <= 4]
    high_quality = qual[qual["Overall Material Quality"] >= 8]

    if not low_quality.empty and not high_quality.empty:
        penalty = high_quality["House Sale Price"].mean() - low_quality["House Sale Price"].mean()

        st.metric(
            label="Estimated Value Loss for Low Quality Homes",
            value=f"${int(penalty):,}"
        )

# ---------------------------------------------------
# CONDITION STABILITY ANALYSIS
# ---------------------------------------------------
st.subheader("🏗️ Structural Stability — Condition vs Price Volatility")

if not cond.empty:
    stability = cond.copy()

    fig = px.scatter(
        stability,
        x="Overall Condition Rating",
        y="Count",
        size="Count",
        color="Overall Condition Rating"
    )

    fig.update_yaxes(title="Number of Homes")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# FAIR PRICE ESTIMATOR
# ---------------------------------------------------
st.subheader("📏 Fair Price Estimator — Based on Quality")

if not qual.empty:

    selected_quality = st.slider(
        "Select Property Quality",
        int(qual["Overall Material Quality"].min()),
        int(qual["Overall Material Quality"].max()),
        5
    )

    expected_price = qual[
        qual["Overall Material Quality"] == selected_quality
    ]["House Sale Price"].mean()

    if pd.notna(expected_price):
        st.metric(
            label="Estimated Fair Market Price",
            value=f"${int(expected_price):,}"
        )

# ---------------------------------------------------
# VALUE FOR MONEY ANALYSIS
# ---------------------------------------------------
st.subheader("💰 Value-for-Money — Quality Efficiency")

if not qual.empty:

    efficiency = qual.groupby("Overall Material Quality")[
        "House Sale Price"
    ].mean().reset_index()

    efficiency["Value Score"] = (
        efficiency["Overall Material Quality"] /
        efficiency["House Sale Price"]
    )

    fig = px.bar(
        efficiency,
        x="Overall Material Quality",
        y="Value Score",
        color="Value Score",
        color_continuous_scale="Viridis"
    )

    fig.update_yaxes(title="Quality per Dollar")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# RESALE POTENTIAL INDEX
# ---------------------------------------------------
st.subheader("📈 Resale Potential — Quality Growth Indicator")

if not qual.empty:

    resale = qual.groupby("Overall Material Quality")[
        "House Sale Price"
    ].mean().pct_change().reset_index()

    fig = px.line(
        resale,
        x="Overall Material Quality",
        y="House Sale Price",
        markers=True
    )

    fig.update_yaxes(title="Relative Price Growth")

    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=360)

    st.plotly_chart(fig, use_container_width=True)