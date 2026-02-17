import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

API_BASE = "http://localhost:8000/api"

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="House Price Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Custom CSS Styling
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #eef2f7 0%, #d9e4f5 100%);
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

.hero {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}

.kpi-card {
    background: violet;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    text-align: center;
}

.insight-box {
    background: #ffffff;
    padding: 1rem;
    border-left: 5px solid #2ecc71;
    border-radius: 10px;
    margin-top: 1rem;
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
# Hero Section
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🏠 House Price Trends Intelligence</h1>
    <p>Yearly Trends • Seasonal Analysis • Market Segments</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar UI/UX Controls
# ---------------------------------------------------
with st.sidebar:
    st.title("⚙️ Dashboard Controls")
    st.markdown("---")

    selected_year_range = st.slider(
        "Select Construction Year Range",
        1990, 2025, (2000, 2020)
    )

    segment_filter = st.multiselect(
        "Select Market Segment",
        ["Budget", "Mid", "Premium", "Luxury"],
        default=["Budget", "Mid", "Premium", "Luxury"]
    )

    st.markdown("---")
    st.markdown("### 📌 About")
    st.info("""
    This dashboard connects to a live API backend.
    It visualizes:
    • Yearly price trends  
    • Monthly seasonality  
    • Distribution spread  
    • Market segmentation  
    """)

# ---------------------------------------------------
# API Loader
# ---------------------------------------------------
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
    except Exception as e:
        st.error(f"API error on {endpoint}: {str(e)}")
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

# Load datasets
fdf1 = load_api_data("/price-trends/yearly")
fdf2 = load_api_data("/price-trends/seasonal")
fdf3 = load_api_data("/price-trends/distribution")
fdf4 = load_api_data("/price-trends/segments")

# ---------------------------------------------------
# Main Dashboard
# ---------------------------------------------------
if fdf1.empty:
    st.warning("No data available from API.")
else:

    # Filter by Year
    fdf1 = fdf1[
        (fdf1['Construction Year'] >= selected_year_range[0]) &
        (fdf1['Construction Year'] <= selected_year_range[1])
    ]

    # ---------------------------------------------------
    # KPI Section
    # ---------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_price = int(fdf1['House Sale Price'].mean())
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Average Price</h3>
            <h2>${avg_price:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_sales = len(fdf1)
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Total Sales</h3>
            <h2>{total_sales}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        median_price = int(fdf1['House Sale Price'].median())
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Median Price</h3>
            <h2>${median_price:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------------------------------------------
    # Yearly Trends
    # ---------------------------------------------------
    st.subheader("📈 Yearly Price Trends")

    yearly = fdf1.groupby('Construction Year')['House Sale Price'] \
                 .agg(['mean', 'median']).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly['Construction Year'],
        y=yearly['mean'],
        mode='lines+markers',
        name='Mean Price'
    ))
    fig.add_trace(go.Scatter(
        x=yearly['Construction Year'],
        y=yearly['median'],
        mode='lines+markers',
        name='Median Price'
    ))
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Trend Insight
    if len(yearly) > 1:
        change = ((yearly.iloc[-1]['mean'] - yearly.iloc[0]['mean']) /
                  yearly.iloc[0]['mean'] * 100)
        st.markdown(
            f"<div class='insight-box'><b>Trend Insight:</b> "
            f"{'📈 Upward' if change > 0 else '📉 Downward'} movement of "
            f"<b>{abs(change):.2f}%</b> over selected period.</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------------------------------------------------
    # Seasonal Analysis
    # ---------------------------------------------------
    st.subheader("📆 Seasonal Patterns")

    monthly = fdf2.groupby('Month Sold')['House Sale Price'].mean().reset_index()

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly['Month'] = monthly['Month Sold'].apply(lambda x: months[int(x)-1])

    fig = px.bar(
        monthly,
        x='Month',
        y='House Sale Price',
        color='House Sale Price',
        color_continuous_scale='Teal'
    )
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # Distribution
    # ---------------------------------------------------
    st.subheader("📉 Price Distribution")

    fig = go.Figure(go.Histogram(
        x=fdf1['House Sale Price'],
        nbinsx=40
    ))
    fig.update_layout(
        height=350,
        xaxis_title='Price ($)',
        yaxis_title='Count'
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # Market Segments
    # ---------------------------------------------------
    st.subheader("🏘 Market Segments")

    segs = pd.cut(
        fdf4['House Sale Price'],
        bins=[0,150000,250000,400000,1e6],
        labels=['Budget','Mid','Premium','Luxury']
    )

    seg_df = segs.value_counts().reset_index()
    seg_df.columns = ['Segment','Count']

    seg_df = seg_df[seg_df['Segment'].isin(segment_filter)]

    fig = go.Figure(go.Pie(
        labels=seg_df['Segment'],
        values=seg_df['Count'],
        hole=0.5
    ))
    fig = apply_dark_navy_layout(fig)
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------------------------------------------
    # AFFORDABILITY ESTIMATOR
    # ---------------------------------------------------
    st.subheader("🏦 Affordability Calculator")

    income = st.number_input("Monthly Household Income ($)", 1000, 50000, 6000)
    rate = st.slider("Interest Rate (%)", 1.0, 12.0, 7.5)
    years = st.slider("Loan Term (Years)", 5, 30, 20)

    monthly_budget = income * 0.30  # 30% rule

    r = rate / 100 / 12
    n = years * 12

    if r > 0:
        loan = monthly_budget * ((1 + r) ** n - 1) / (r * (1 + r) ** n)
    else:
        loan = monthly_budget * n

    st.metric("Estimated Affordable Property Price", f"${int(loan):,}")

    # ---------------------------------------------------
    # BEST VALUE YEAR
    # ---------------------------------------------------
    st.subheader("🕰 Property Value by Construction Year")

    fig = px.line(
        yearly,
        x='Construction Year',
        y='mean',
        markers=True,
        title="Average Price by Construction Year"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    
    # ---------------------------------------------------
    # BEST MONTH TO SELL
    # ---------------------------------------------------
    st.subheader("📅 Seasonal Selling Prices")

    fig = px.bar(
        monthly,
        x='Month',
        y='House Sale Price',
        title="Average Price by Month"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    
    # ---------------------------------------------------
    # BEST MONTH TO BUY
    # ---------------------------------------------------
    st.subheader("🛒 Buyer Advantage Period")

    fig = px.line(
        monthly,
        x='Month',
        y='House Sale Price',
        markers=True,
        title="Seasonal Buying Opportunities"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


    # Market Momentum Indicator (Price Change Over Time)
    st.subheader("📈 Market Momentum Trend")

    yearly_growth = yearly.copy()
    yearly_growth['Growth %'] = yearly_growth['mean'].pct_change() * 100

    fig = px.line(
        yearly_growth,
        x='Construction Year',
        y='Growth %',
        markers=True,
        title="Year-over-Year Price Growth"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


    # Price Segmentation Distribution (Market Structure)
    st.subheader("🧠 Market Price Segmentation")

    fig = px.box(
        fdf1,
        y='House Sale Price',
        points='all',
        title="Price Distribution & Outliers"
    )
    fig = apply_dark_navy_layout(fig)
    st.plotly_chart(fig, use_container_width=True)