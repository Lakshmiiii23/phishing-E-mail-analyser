import os
import sys

# Ensure KMP library duplicate doesn't crash on certain OS setups
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF

# Dynamically resolve root and source folders robustly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

if project_root not in sys.path:
    sys.path.append(project_root)
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from rule_engine import calculate_rule_score
from risk_fusion import calculate_final_risk
from retrieve_context import retrieve_context
from report_generator import generate_report

# =====================================
# Page Configurations
# =====================================
st.set_page_config(
    page_title="AI Phishing Email Scanner",
    page_icon="📧",
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
    
    /* Glow Badges */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        font-weight: 600;
        font-size: 0.85rem;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-high {
        background-color: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Button Customization */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# Load Models Robustly
# =====================================
@st.cache_resource
def load_assets():
    model_path = os.path.join(project_root, "models", "phishing_model.pkl")
    vectorizer_path = os.path.join(project_root, "models", "vectorizer.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        st.error("Error: Trained model assets missing! Please run 'python run.py' from the terminal to build models first.")
        st.stop()
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

model, vectorizer = load_assets()

# =====================================
# PDF Generation Helper
# =====================================
def convert_markdown_to_pdf(markdown_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header Banner Style
    pdf.set_fill_color(30, 41, 59) # #1e293b dark slate color
    pdf.rect(0, 0, 210, 40, "F")
    
    # Centered Title inside the banner bounds using absolute set_xy
    pdf.set_text_color(248, 250, 252) # #f8fafc slate light text
    pdf.set_xy(10, 10)
    pdf.set_font("Helvetica", style="B", size=15)
    pdf.cell(190, 10, "CYBER INCIDENT ASSESSMENT REPORT", align="C")
    
    pdf.set_xy(10, 22)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(190, 10, "Automated Security Modeling & AI Threat Report", align="C")
    
    # Now set the cursor Y below the banner and reset X to left margin
    pdf.set_xy(10, 50)
    
    # Body text color (Dark charcoal)
    pdf.set_text_color(15, 23, 42) # #0f172a
    pdf.set_font("Helvetica", size=10)
    
    # Replace common unicode chars to avoid encoding errors in standard latin-1
    clean_text = markdown_text
    replacements = {
        "✓": "-",
        "🤖": "[AI]",
        "🛡️": "[SEC]",
        "🚨": "[ALERT]",
        "📊": "[METRIC]",
        "📚": "[KB]",
        "📥": "[DOWNLOAD]",
        "💡": "[TIP]",
        "🚀": "[RUN]",
        "•": "-",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'"
    }
    for orig, rep in replacements.items():
        clean_text = clean_text.replace(orig, rep)
        
    # Standard latin-1 cleanup to be 100% safe
    clean_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    
    for line in clean_text.split('\n'):
        line = line.strip()
        if not line:
            pdf.ln(3)
            continue
            
        # Explicitly ensure x is reset to left margin before drawing
        pdf.set_x(10)
            
        # Detect headings
        if line.startswith("### "):
            pdf.ln(4)
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.multi_cell(190, 6, line[4:])
            pdf.set_font("Helvetica", size=10)
        elif line.startswith("## "):
            pdf.ln(5)
            pdf.set_font("Helvetica", style="B", size=13)
            pdf.multi_cell(190, 7, line[3:])
            pdf.set_font("Helvetica", size=10)
        elif line.startswith("# "):
            pdf.ln(7)
            pdf.set_font("Helvetica", style="B", size=15)
            pdf.multi_cell(190, 8, line[2:])
            pdf.set_font("Helvetica", size=10)
        else:
            pdf.multi_cell(190, 5.5, line)
            
    return bytes(pdf.output())

# Main Header UI Banner
st.markdown("""
<div class="title-banner">
    <h1>📧 suspicious Email Scanner</h1>
    <p>Hybrid Analysis Scanner combining ML Classifier, Heuristics Rules, and GenAI incident reports.</p>
</div>
""", unsafe_allow_html=True)

# Navigation Back to Portal Home
if st.button("⬅️ Back to Portal Home"):
    st.switch_page("app.py")

# Main Content Columns
col_left, col_right = st.columns([1, 1.2], gap="large")

# Track if email has been analyzed
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
    st.session_state.results = {}

with col_left:
    st.subheader("📥 Suspicious Email Input")
    email_text = st.text_area(
        "Paste the raw content of the suspicious email below for hybrid analysis:",
        height=280,
        placeholder="Paste header/body content here..."
    )
    
    st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Analyze Threats")

    if analyze_clicked:
        if not email_text.strip():
            st.warning("Please paste some content before analyzing.")
        else:
            with st.spinner("Executing hybrid analysis threat modeling..."):
                # 1. ML Probability
                email_vector = vectorizer.transform([email_text])
                ml_prob = model.predict_proba(email_vector)[0][1]

                # 2. Heuristic Rules
                rule_score, indicators = calculate_rule_score(email_text)

                # 3. Risk Fusion Engine
                result = calculate_final_risk(ml_prob, rule_score)

                # 4. FAISS Semantic Context
                try:
                    context = retrieve_context(email_text, top_k=3)
                except Exception as e:
                    st.error(f"Semantic retrieval unavailable: {e}")
                    context = []

                # 5. Gemini assessment
                report = generate_report(
                    email_text=email_text,
                    ml_score=result["ml_score"],
                    rule_score=result["rule_score"],
                    risk_level=result["risk_level"],
                    indicators=indicators,
                    retrieved_context=context
                )

                # Store Results
                st.session_state.results = {
                    "ml_score": result["ml_score"],
                    "rule_score": result["rule_score"],
                    "final_score": result["final_score"],
                    "risk_level": result["risk_level"],
                    "indicators": indicators,
                    "context": context,
                    "report": report
                }
                st.session_state.analyzed = True

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 Standard Safeguards")
    st.info("✓ **Sender Verification**: Check headers for matching 'From' and 'Reply-To' addresses.\n\n"
            "✓ **Link Shielding**: Hover over links instead of clicking them directly.\n\n"
            "✓ **Urgency Checks**: High-pressure timelines usually imply standard phishing vectors.")

with col_right:
    if st.session_state.analyzed:
        res = st.session_state.results
        
        st.subheader("📊 Real-Time Threat Scorecard")
        
        # Threat Badge
        lvl = res["risk_level"]
        badge_class = f"badge-{lvl.lower()}"
        st.markdown(f"Risk Severity Index: <span class='badge {badge_class}'>{lvl}</span>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Risk Progress Slider
        st.progress(int(res["final_score"]))
        st.write(f"**Combined Cybersecurity Risk Score:** `{res['final_score']}%`")

        # Metric Stats
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.metric(label="ML Prediction Probability", value=f"{res['ml_score']}%")
        with sub_col2:
            st.metric(label="Rule Engine Heuristic Score", value=f"{res['rule_score']}/100")

        # Indicators Block
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🚨 Warning Flags Raised")
        if res["indicators"]:
            for item in res["indicators"]:
                st.warning(item)
        else:
            st.success("No suspicious heuristic rules triggered.")

        # RAG Context Block
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📚 Matched Security Knowledge Base Context")
        for item in res["context"]:
            st.info(item)

        # Generative Threat Analysis Report
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🤖 GenAI Incident Assessment Report")
        st.download_button(
            label="📥 Download Full Incident Report (PDF)",
            data=convert_markdown_to_pdf(res["report"]),
            file_name="cyber_incident_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    else:
        st.markdown(
            "<div style='border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 4rem; text-align: center; color: #64748b; margin-top: 2rem;'>"
            "<h3>Waiting for Phishing Assessment</h3>"
            "<p>Enter email details in the left panel and click 'Analyze Threats' to see the scorecard here.</p>"
            "</div>",
            unsafe_allow_html=True
        )
