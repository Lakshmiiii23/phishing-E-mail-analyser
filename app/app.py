import os
import sys
import streamlit as st

# Ensure KMP library duplicate doesn't crash on certain OS setups
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Page Configurations
st.set_page_config(
    page_title="AI CyberPhish Gatekeeper Portal",
    page_icon="🛡️",
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
        background-color: #0f172a;
    }
    
    /* Portal Container Banner */
    .portal-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 3.5rem 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px -15px rgba(0, 0, 0, 0.7);
    }
    
    .portal-banner h1 {
        color: #f8fafc !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(120deg, #3b82f6, #60a5fa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .portal-banner p {
        color: #94a3b8 !important;
        font-size: 1.25rem !important;
        max-width: 800px;
        margin: 0 auto !important;
        line-height: 1.6 !important;
    }
    
    /* Interactive Navigation Cards */
    .nav-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .nav-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 15px 35px -5px rgba(59, 130, 246, 0.15);
        transform: translateY(-5px);
    }
    
    .nav-card h3 {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.8rem !important;
        color: #f8fafc !important;
    }
    
    .nav-card p {
        font-size: 1rem !important;
        color: #94a3b8 !important;
        line-height: 1.5 !important;
        margin-bottom: 2rem !important;
        height: 80px;
    }
    
    /* Dynamic Buttons styling */
    div.stButton > button {
        width: 100%;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* Individual Button Custom Gradients */
    .analysis-btn button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35) !important;
    }
    .analysis-btn button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45) !important;
        transform: translateY(-2px);
    }
    
    .summary-btn button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
    }
    .summary-btn button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# Home Banner
# =====================================
st.markdown("""
<div class="portal-banner">
    <h1>🛡️ AI CyberPhish Gatekeeper</h1>
    <p>Welcome to the Enterprise Security Intelligence Gateway. Combining stratified machine learning classification models, custom heuristic engines, FAISS semantic knowledge-base retrieval, and Generative GenAI incident modeling into one consolidated cyber shield.</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# Side-by-Side Portal Cards Grid
# =====================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="nav-card">
        <h3>📧 suspicous Email Analysis</h3>
        <p>Run advanced phishing classification on suspicious emails. Combines Logistic Regression vector scoring with standard cybersecurity safeguards to analyze urgency headers, IP-domain redirects, and suspicious file attachments.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Styled analysis navigation button using CSS class injection wrapper
    st.markdown("<div class='analysis-btn'>", unsafe_allow_html=True)
    if st.button("🚀 Start Email Analysis Scanner"):
        st.switch_page("pages/1_Email_Analysis.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <h3>📊 Executive Summary Dashboard</h3>
        <p>Access high-fidelity enterprise statistics, overall threat volume metrics, dataset distributions, and active model accuracy rates. Designed for security operations command and executive intelligence reporting.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Styled executive navigation button using CSS class injection wrapper
    st.markdown("<div class='summary-btn'>", unsafe_allow_html=True)
    if st.button("📊 Open Executive Summary Dashboard"):
        st.switch_page("pages/2_Executive_Summary.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Quick stats footer
st.markdown("<br><br><hr style='border: 1px solid rgba(255, 255, 255, 0.05);'><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>"
    "🛡️ AI CyberPhish Platform v2.0 • Stratified ML Classifier: 98.4% Precision Target • Hybrid Security System Active"
    "</div>",
    unsafe_allow_html=True
)