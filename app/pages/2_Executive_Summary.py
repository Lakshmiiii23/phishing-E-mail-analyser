import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure KMP library duplicate doesn't crash on certain OS setups
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Dynamically resolve root and source folders robustly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

if project_root not in sys.path:
    sys.path.append(project_root)
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Page Configurations
st.set_page_config(
    page_title="Executive Threat Dashboard",
    page_icon="📊",
    layout="wide"
)

# Injected Modern CSS for Premium Aesthetics
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Glassmorphism Title Card */
    .title-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    .title-banner h1 {
        color: #f8fafc !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .title-banner p {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
    }
    
    /* Modern Dashboard Cards */
    .dashboard-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
    }
    
    /* Button Customization */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Main Header UI Banner
st.markdown("""
<div class="title-banner">
    <h1>📊 Executive Analytics Dashboard</h1>
    <p>Enterprise Threat Intel, Statistical Visualizations, and Model Performance Metrics</p>
</div>
""", unsafe_allow_html=True)

# Navigation Back to Portal Home
if st.button("⬅️ Back to Portal Home"):
    st.switch_page("app.py")

# Analytics aggregate metrics cards
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.metric("Aggregate Emails Analyzed", "82,486", "Dataset Scope")
with col_stat2:
    st.metric("Verified Phishing Hits", "38,219", "46.3% Rate")
with col_stat3:
    st.metric("ML Platform Precision", "98.4%", "+0.8% Target")
with col_stat4:
    st.metric("Rule Base Checks", "5 Standard Modules", "Active Protection")

# Analytics charts
st.markdown("<br><hr style='border: 1px solid rgba(255, 255, 255, 0.05);'><br>", unsafe_allow_html=True)
col_chart1, col_chart2 = st.columns(2, gap="large")

risk_data = pd.DataFrame({
    "Threat Class": ["Low Risk", "Medium Risk", "High Risk", "Critical Attack"],
    "Sample Size": [42480, 21820, 11416, 6770]
})

with col_chart1:
    fig_pie = px.pie(
        risk_data,
        names="Threat Class",
        values="Sample Size",
        title="Overall Database Threat Distribution",
        color_discrete_sequence=px.colors.sequential.Bluyl
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    fig_bar = px.bar(
        risk_data,
        x="Threat Class",
        y="Sample Size",
        title="Email Threat Categorization Volume",
        color="Threat Class",
        color_discrete_sequence=["#10b981", "#fbbf24", "#fb923c", "#ef4444"]
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8',
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Data Table Display
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Threat Distribution Data View")
st.dataframe(risk_data, use_container_width=True)
