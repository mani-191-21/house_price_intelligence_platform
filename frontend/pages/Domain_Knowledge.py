import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Real Estate Domain Knowledge",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# DARK ENTERPRISE THEME
# ---------------------------------------------------
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b1220 !important;   /* Deep Dark Navy */
}

/* Main container */
.block-container {
    background-color: #0b1220 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b1220 !important;
}

/* HERO — SAME COLOR (UNCHANGED) */
.hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 100%);
    padding: 3rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(14,165,233,0.4);
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
}

.hero-sub {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* KNOWLEDGE BLOCK — Dark Navy */
.knowledge-card {
    background: #0f172a;   /* Navy card */
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.2rem;
    border-left: 6px solid #38bdf8;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.knowledge-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
}

.knowledge-text {
    color: #cbd5e1;
    font-size: 0.95rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">🏠 Real Estate Domain Intelligence</div>
    <div class="hero-sub">
        Strategic Knowledge • Market Understanding • Investment Insights
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# KNOWLEDGE BLOCKS
# ---------------------------------------------------
# 1
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">📍 Location Premium</div>
<div>🏙️📊</div>
</div>
<div class="knowledge-text">
Location is the single most important driver of property value.
Proximity to employment hubs, schools, transit, healthcare, and
retail ecosystems creates sustained demand and long-term appreciation.
Prime micro-locations often outperform broader market trends and
maintain liquidity even during downturns.
</div>
</div>
""", unsafe_allow_html=True)

# 2
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">💰 Investment Asset Class</div>
<div>💼🏦</div>
</div>
<div class="knowledge-text">
Real estate is a stable tangible asset providing both capital
appreciation and recurring rental income. It offers inflation
hedging, portfolio diversification, and leverage opportunities,
making it a cornerstone for institutional and private wealth
management strategies.
</div>
</div>
""", unsafe_allow_html=True)

# 3
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🏢 Residential vs Commercial</div>
<div>🏢🏠</div>
</div>
<div class="knowledge-text">
Residential assets depend on population growth and housing demand,
while commercial properties are tied to economic activity, business
expansion, and employment trends. Commercial assets typically offer
higher yields but come with cyclic risks and longer vacancy periods.
</div>
</div>
""", unsafe_allow_html=True)

# 4
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">📈 Market Cycles</div>
<div>🔄📉</div>
</div>
<div class="knowledge-text">
Property markets follow cyclical patterns: expansion, peak,
correction, and recovery. Strategic investors analyze interest
rates, credit availability, construction pipelines, and macroeconomic
signals to optimize entry and exit timing.
</div>
</div>
""", unsafe_allow_html=True)

# 5
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🏗️ Supply & Demand Dynamics</div>
<div>📦📊</div>
</div>
<div class="knowledge-text">
Housing shortages combined with urbanization drive price growth.
Conversely, oversupply increases vacancy rates and reduces rental
returns. Monitoring building permits, inventory levels, and
absorption rates helps forecast price direction.
</div>
</div>
""", unsafe_allow_html=True)

# 6
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🚇 Infrastructure Impact</div>
<div>🛣️🚄</div>
</div>
<div class="knowledge-text">
Major infrastructure projects — metro systems, highways,
airports, and IT corridors — transform accessibility and
economic potential. Properties near new infrastructure often
experience accelerated appreciation before and after completion.
</div>
</div>
""", unsafe_allow_html=True)

# 7
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🏘️ Neighborhood Quality</div>
<div>🛡️🌳</div>
</div>
<div class="knowledge-text">
Safety, environmental quality, public services, schools,
and community profile define residential desirability.
High-quality neighborhoods demonstrate stronger price
resilience and attract long-term homeowners.
</div>
</div>
""", unsafe_allow_html=True)

# 8
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🧾 Rental Yield Potential</div>
<div>📄💸</div>
</div>
<div class="knowledge-text">
Rental yield measures income relative to property value.
Urban centers and student hubs often provide high yields,
while prime luxury zones prioritize capital appreciation.
Investors balance yield with vacancy risk and maintenance costs.
</div>
</div>
""", unsafe_allow_html=True)

# 9
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">⚖️ Regulatory Environment</div>
<div>📜🏛️</div>
</div>
<div class="knowledge-text">
Government regulations, zoning rules, taxation, and incentives
shape development feasibility and investor sentiment.
Transparent regulatory frameworks encourage foreign investment
and large-scale urban development.
</div>
</div>
""", unsafe_allow_html=True)

# 10
st.markdown("""
<div class="knowledge-card">
<div style="display:flex; justify-content:space-between;">
<div class="knowledge-title">🌍 Long-Term Wealth Creation</div>
<div>🌐🏆</div>
</div>
<div class="knowledge-text">
Real estate builds generational wealth through appreciation,
rental income, leverage benefits, and tax efficiencies.
It remains one of the most trusted vehicles for long-term
capital preservation across global markets.
</div>
</div>
""", unsafe_allow_html=True)