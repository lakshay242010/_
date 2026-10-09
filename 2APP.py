import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & MODERN FUTURISTIC DARK THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI | Autonomous AgTech Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #030712 !important;
        color: #f3f4f6 !important;
    }

    [data-testid="stMainBlockContainer"], .main, .block-container {
        background: #030712 !important;
        padding-top: 2rem !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .stMetric, div[data-testid="stExpander"], div[data-testid="stForm"], .futuristic-card {
        background: rgba(17, 24, 39, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    [data-testid="stMetricValue"] {
        color: #a3e635 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 12px rgba(163, 230, 53, 0.3);
    }

    input, textarea, select, div[data-baseweb="select"] {
        background: rgba(31, 41, 55, 0.6) !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #a3e635 0%, #65a30d 100%) !important;
        color: #052e16 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        width: 100% !important;
        height: 52px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 20px rgba(163, 230, 53, 0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(163, 230, 53, 0.55) !important;
    }

    .hero-banner-modern {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(3, 7, 18, 0.9) 100%), 
                    radial-gradient(circle at top right, rgba(163, 230, 53, 0.15), transparent 50%);
        border: 1px solid rgba(163, 230, 53, 0.2);
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #a3e635 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }

    .ack-glow {
        background: linear-gradient(135deg, rgba(163, 230, 53, 0.08) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-left: 5px solid #a3e635;
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .thinking-badge {
        color: #a3e635;
        font-size: 13px;
        font-weight: 600;
        background: rgba(163, 230, 53, 0.1);
        padding: 6px 12px;
        border-radius: 20px;
        border: 1px solid rgba(163, 230, 53, 0.3);
        display: inline-block;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. REAL HIGH-RESOLUTION PHOTOGRAPHY ASSET REPOSITORY
# -----------------------------------------------------------------------------
REAL_IMAGES = {
    "drone": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=1200&auto=format&fit=crop",
    "satellite": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
    "harvest": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?q=80&w=1200&auto=format&fit=crop",
    "leaf_health": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?q=80&w=1200&auto=format&fit=crop",
    "business_executive": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200&auto=format&fit=crop",
    "logistics": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=1200&auto=format&fit=crop"
}

# -----------------------------------------------------------------------------
# 3. MACHINE LEARNING MODEL
# -----------------------------------------------------------------------------
@st.cache_resource
def train_biosync_model():
    np.random.seed(42)
    n_samples = 3000

    soil_moisture = np.random.uniform(20, 95, n_samples)
    temperature = np.random.uniform(15, 42, n_samples)
    humidity = np.random.uniform(30, 98, n_samples)
    rainfall = np.random.uniform(0, 50, n_samples)
    bio_freq = np.random.uniform(300, 900, n_samples)

    labels = []
    for sm, t, h, r, freq in zip(soil_moisture, temperature, humidity, rainfall, bio_freq):
        if (h > 78 and 22 <= t <= 33 and sm > 65) or (freq < 480):
            labels.append(1)
        else:
            labels.append(0)

    X = np.column_stack((soil_moisture, temperature, humidity, rainfall, bio_freq))
    y = np.array(labels)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X, y)
    return clf

model = train_biosync_model()

# -----------------------------------------------------------------------------
# 4. KNOWLEDGE BASE RESPONSES
# -----------------------------------------------------------------------------
def generate_ai_response(query):
    q_lower = query.lower()
    
    if "introduced" in q_lower or "history" in q_lower or "origin" in q_lower or "neolithic" in q_lower:
        return ("### 🌾 The History & Introduction of Agriculture\n\n"
                "Agriculture began approximately **12,000 years ago** during the **Neolithic Revolution**.\n\n"
                "1. **Fertile Crescent:** Domestication of wheat, barley, and rye in the Middle East.\n"
                "2. **East Asia & Mesoamerica:** Independent development of rice, corn, and potatoes.\n"
                "3. **Socioeconomic Transition:** Settled farming allowed human populations to build permanent cities, trade networks, and modern industries.")

    elif "business" in q_lower or "revenue" in q_lower or "profit" in q_lower or "economic" in q_lower or "market" in q_lower:
        return ("### 📈 Enterprise Agribusiness & Market Valuation\n\n"
                "* **Operating Margin Optimization:** AI diagnostics lower chemical spending by up to **32%**.\n"
                "* **Supply Chain Compliance:** Meets EUDR zero-deforestation guidelines across 103 enterprise jurisdictions.\n"
                "* **Capital Allocation:** Real-time yield trajectory reduces harvest insurance premiums by **18%**.")

    elif "creator" in q_lower or "developer" in q_lower or "lakshay" in q_lower:
        return ("**BioSyncAI** was created by **Lakshay of Class XI A** along with team members for the **OlympAI Hackathon 2026**.")

    elif "2057" in q_lower or "robot" in q_lower or "future" in q_lower or "drone" in q_lower:
        return ("Our **Vision 2057 Roadmap** targets **100% autonomous robotic agriculture** through solar-powered ground rovers and aerial drone swarms.")

    else:
        return (f"### 🧬 AgTech Analysis: '{query}'\n\n"
                "BioSyncAI connects orbital remote sensing, soil moisture microclimates, and machine learning classifiers to streamline farm yields and business operations.")

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#a3e635 !important; font-weight:800;'>BioSyncAI Core</h2>", unsafe_allow_html=True)
st.sidebar.caption("⚡ Enterprise AgTech & Robotic Mesh")

menu = st.sidebar.radio(
    "Navigation System",
    [
        "🚀 Platform Overview",
        "💼 Enterprise Business & ROI Matrix",
        "💬 BioSync AI Talk Studio",
        "🤖 Vision 2057: Autonomous Swarms",
        "🌐 Live Motion Spatial Matrix",
        "🔬 Multispectral Leaf Diagnostics",
        "🧠 Multimodal AI Diagnostic",
        "📊 Yield Outlook & Water Grid",
        "📞 Request Enterprise Demo",
        "📄 RFP Report Generator",
        "ℹ️ Created By & Team"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 **Created By:** Lakshay (Class XI A)\n🤖 **Robotic Swarm:** Vision 2057\n🏫 **OlympAI Hackathon 2026**")

# -----------------------------------------------------------------------------
# MODULE 1: PLATFORM OVERVIEW
# -----------------------------------------------------------------------------
if menu == "🚀 Platform Overview":
    st.markdown("""
    <div class='hero-banner-modern'>
        <div class='hero-title'>BioSyncAI Enterprise Platform</div>
        <p style='font-size: 18px; color: #cbd5e1; line-height: 1.6;'>
            Next-generation agricultural intelligence powering autonomous operations, orbital field analytics, and predictive AI decision frameworks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(REAL_IMAGES["satellite"], caption="Orbital Satellite Telemetry Grid", use_container_width=True)
        st.subheader("Orbital Surveillance")
        st.write("Hyperspectral and thermal satellite telemetry mapped continuously.")

    with c2:
        st.image(REAL_IMAGES["leaf_health"], caption="Multispectral Cellular Vision", use_container_width=True)
        st.subheader("Cellular Diagnostics")
        st.write("Real-time detection of crop stress and pathogens using computer vision.")

    with c3:
        st.image(REAL_IMAGES["drone"], caption="Autonomous Farm Robotics & Drones", use_container_width=True)
        st.subheader("Robotic Swarms")
        st.write("Fully automated sowing, weeding, and targeted intervention robotics.")

# -----------------------------------------------------------------------------
# MODULE 2: ENTERPRISE BUSINESS & ROI MATRIX
# -----------------------------------------------------------------------------
elif menu == "💼 Enterprise Business & ROI Matrix":
    st.markdown("<h1 style='color:#a3e635;'>Enterprise Business Intelligence & ROI</h1>", unsafe_allow_html=True)

    st.image(REAL_IMAGES["business_executive"], caption="BioSyncAI Enterprise Operations Dashboard", use_container_width=True)

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Monitored Portfolio", "$1.4B", "+12.4%")
    b2.metric("Operating Cost Savings", "28.5%", "-$420k/Yr")
    b3.metric("Global Coverage", "103 Countries", "+14 Regions")
    b4.metric("EUDR Compliance", "100%", "Verified")

    st.markdown("---")
    st.subheader("📊 Live Enterprise Revenue & Yield Trajectory")
    
    # Interactive Revenue / Yield Simulator Chart
    acres = st.slider("Select Farm Size (Acres)", 1000, 50000, 12500, step=1000)
    baseline_yield = acres * 3.8 * 240
    optimized_yield = acres * 4.6 * 240

    df_business = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
        "Traditional Revenue ($)": np.linspace(baseline_yield * 0.1, baseline_yield, 8),
        "BioSyncAI AI Optimized ($)": np.linspace(optimized_yield * 0.12, optimized_yield, 8)
    }).set_index("Month")

    st.line_chart(df_business)

# -----------------------------------------------------------------------------
# MODULE 3: BIOSYNC AI TALK STUDIO
# -----------------------------------------------------------------------------
elif menu == "💬 BioSync AI Talk Studio":
    st.markdown("<h1 style='color:#a3e635;'>BioSync AI Talk Assistant & Studio</h1>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am BioSyncAI's enterprise assistant. Ask me anything about AgTech, business operations, crop history, or economics."}
        ]

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_query = st.chat_input("Type your query here...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            status_container = st.empty()
            status_container.markdown("<div class='thinking-badge'>🧠 BioSync AI is analyzing query intent...</div>", unsafe_allow_html=True)
            time.sleep(0.5)

            status_container.markdown("<div class='thinking-badge'>🔍 Searching AgTech Knowledge Base & Live Telemetry...</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            status_container.empty()

            full_response = generate_ai_response(user_query)
            st.write(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# -----------------------------------------------------------------------------
# MODULE 4: VISION 2057: AUTONOMOUS SWARMS
# -----------------------------------------------------------------------------
elif menu == "🤖 Vision 2057: Autonomous Swarms":
    st.markdown("<h1 style='color:#a3e635;'>Vision 2057: Autonomous Agriculture</h1>", unsafe_allow_html=True)

    st.image(REAL_IMAGES["drone"], caption="BioSyncAI Heavy-Duty Agricultural Sprayer Drone", use_container_width=True)

    r1, r2, r3 = st.columns(3)
    r1.metric("Global Drone Swarm Target", "10,000,000", "By 2057")
    r2.metric("Manual Human Effort", "0.0%", "-100%")
    r3.metric("Harvesting Accuracy", "99.8%", "+45% Efficiency")

# -----------------------------------------------------------------------------
# MODULE 5: LIVE MOTION SPATIAL MATRIX
# -----------------------------------------------------------------------------
elif menu == "🌐 Live Motion Spatial Matrix":
    st.markdown("<h1 style='color:#a3e635;'>Operating Decision & Real-Time Motion Matrix</h1>", unsafe_allow_html=True)

    run_sim = st.toggle("⚡ Enable Real-Time Motion Data Stream", value=True)
    chart_placeholder = st.empty()

    if run_sim:
        # Live Motion Working Graph Simulation
        for i in range(5):
            live_data = pd.DataFrame(
                np.random.randn(20, 3) + [25, 65, 80],
                columns=["Soil Temperature (°C)", "Moisture Saturation (%)", "Humidity (%)"]
            )
            chart_placeholder.line_chart(live_data)
            time.sleep(0.3)
    else:
        static_data = pd.DataFrame(
            np.random.randn(20, 3) + [25, 65, 80],
            columns=["Soil Temperature (°C)", "Moisture Saturation (%)", "Humidity (%)"]
        )
        chart_placeholder.line_chart(static_data)

# -----------------------------------------------------------------------------
# MODULE 6: MULTISPECTRAL LEAF DIAGNOSTICS
# -----------------------------------------------------------------------------
elif menu == "🔬 Multispectral Leaf Diagnostics":
    st.markdown("<h1 style='color:#a3e635;'>Multispectral Crop Health Engine</h1>", unsafe_allow_html=True)

    st.image(REAL_IMAGES["leaf_health"], caption="High-Resolution Real Crop Sample Analysis", use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 7: MULTIMODAL AI DIAGNOSTIC
# -----------------------------------------------------------------------------
elif menu == "🧠 Multimodal AI Diagnostic":
    st.markdown("<h1 style='color:#a3e635;'>Multimodal AI Inference Engine</h1>", unsafe_allow_html=True)

    with st.expander("🎛️ Live Field Telemetry Controls", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            in_sm = st.slider("Soil Moisture (%)", 0.0, 100.0, 82.0)
            in_temp = st.slider("Ambient Temp (°C)", 10.0, 50.0, 28.0)
            in_hum = st.slider("Humidity (%)", 0.0, 100.0, 86.0)
        with col2:
            in_rain = st.slider("Precipitation (mm)", 0.0, 100.0, 12.5)
            in_freq = st.slider("Bio-Resonance Frequency (Hz)", 300, 900, 520)

        if st.button("🚀 Run Live AI Model Inference"):
            feat = np.array([[in_sm, in_temp, in_hum, in_rain, in_freq]])
            pred = model.predict(feat)[0]
            prob = model.predict_proba(feat)[0]

            if pred == 1:
                st.error(f"🚨 **HIGH RISK DETECTED: Fungal Leaf Blight Threat**\n*Confidence:* `{prob[1]*100:.2f}%`")
            else:
                st.success(f"✅ **HEALTHY FIELD STATUS**\n*Confidence:* `{prob[0]*100:.2f}%`")

# -----------------------------------------------------------------------------
# MODULE 8: YIELD OUTLOOK & WATER GRID
# -----------------------------------------------------------------------------
elif menu == "📊 Yield Outlook & Water Grid":
    st.markdown("<h1 style='color:#a3e635;'>Harvest Forecast & Irrigation</h1>", unsafe_allow_html=True)

    st.image(REAL_IMAGES["harvest"], caption="Automated Industrial Crop Harvesting", use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Estimated Harvest", "4.25 Tons / Ha", "+8.2%")
        st.line_chart(pd.DataFrame({'Yield Trajectory': [3.8, 3.9, 4.0, 4.1, 4.25]}))
    with c2:
        st.metric("Water Saturation Index", "78%", "Optimal Flow")
        st.progress(0.78)

# -----------------------------------------------------------------------------
# MODULE 9: REQUEST ENTERPRISE DEMO
# -----------------------------------------------------------------------------
elif menu == "📞 Request Enterprise Demo":
    st.markdown("<h1 style='color:#a3e635;'>Talk to Our Enterprise Team</h1>", unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 1])

    with col_info:
        st.markdown("""
        ### Why BioSyncAI?
        * **Global Scale:** Enterprise-grade agricultural intelligence.
        * **Decision Workflows:** Supply, Risk, Inspection, and Compliance.
        * **Lead Developer:** Lakshay (Class XI A)
        """)

    with col_form:
        with st.form("demo_form"):
            f_name = st.text_input("First Name *")
            l_name = st.text_input("Last Name *")
            email = st.text_input("Work Email *")
            domain = st.selectbox("Domain", ["Food-Ag", "Forest", "Water", "Energy", "Infrastructure"])
            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if f_name and l_name and email:
                    st.success(f"✅ Request recorded for `{email}`.")

# -----------------------------------------------------------------------------
# MODULE 10: RFP REPORT GENERATOR
# -----------------------------------------------------------------------------
elif menu == "📄 RFP Report Generator":
    st.markdown("<h1 style='color:#a3e635;'>Enterprise RFP & Agronomic Export</h1>", unsafe_allow_html=True)

    report_text = """====================================================
BIOSYNCAI ENTERPRISE AGRONOMIC REPORT
Developer: Lakshay (Class XI A)
Project: OlympAI Hackathon 2026
====================================================

Overall Health Status: Moderate Risk (Zone B Flagged)
Estimated Harvest Yield: 4.25 Tons / Hectare
Active Sensor Nodes: 148 Units
===================================================="""
    st.text_area("Report Output", report_text, height=200)
    st.download_button("📥 Download Report (.txt)", data=report_text, file_name="BioSyncAI_Report.txt")

# -----------------------------------------------------------------------------
# MODULE 11: CREATED BY & TEAM
# -----------------------------------------------------------------------------
elif menu == "ℹ️ Created By & Team":
    st.markdown("<h1 style='color:#a3e635;'>Project Credits</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='ack-glow'>
        <h2 style='color:#a3e635 !important; margin-top:0;'>👨‍💻 Created By</h2>
        <h3 style='color:#ffffff; margin-bottom:15px;'>Lakshay</h3>
        <p style='font-size:18px; color:#cbd5e1;'><strong>Class:</strong> XI A</p>
        <p style='font-size:18px; color:#cbd5e1;'><strong>Project:</strong> BioSyncAI Autonomous AgTech Platform (OlympAI Hackathon 2026)</p>
    </div>
    """, unsafe_allow_html=True)
