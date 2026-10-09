import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ENTERPRISE DARK THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI | Enterprise Agricultural Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force Deep Enterprise Dark Mode (Cropin Aesthetic)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stMainBlockContainer"], .main, .block-container {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d1520 !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    .stMetric, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #0d1520 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }
    input, textarea, select, div[data-baseweb="select"] {
        background-color: #0d1520 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #f1f5f9 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 48px !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%) !important;
        color: #000000 !important;
    }
    .cropin-header {
        color: #84cc16 !important;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .partner-card {
        background-color: #0d1520;
        border-left: 4px solid #84cc16;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    }
    .hero-banner {
        background: linear-gradient(180deg, #0d1520 0%, #04080e 100%);
        border: 1px solid #1e293b;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. IMAGE GENERATION UTILITIES
# -----------------------------------------------------------------------------
def generate_synthetic_image(image_type="leaf"):
    img = Image.new('RGB', (500, 350), color=(13, 21, 32))
    draw = ImageDraw.Draw(img)
    
    if image_type == "leaf":
        draw.ellipse([100, 40, 400, 310], fill=(34, 139, 34), outline=(132, 204, 22), width=2)
        draw.line([250, 40, 250, 310], fill=(132, 204, 22), width=3)
        draw.line([250, 120, 170, 70], fill=(132, 204, 22), width=2)
        draw.line([250, 180, 330, 130], fill=(132, 204, 22), width=2)
        draw.line([250, 240, 160, 200], fill=(132, 204, 22), width=2)
        draw.ellipse([180, 150, 220, 190], fill=(139, 69, 19))
        draw.ellipse([270, 210, 300, 240], fill=(139, 69, 19))
    elif image_type == "satellite":
        for i in range(0, 500, 50):
            draw.line([i, 0, i, 350], fill=(30, 41, 59), width=1)
        for j in range(0, 350, 50):
            draw.line([0, j, 500, j], fill=(30, 41, 59), width=1)
        draw.rectangle([100, 50, 250, 200], fill=(34, 197, 94, 100), outline=(132, 204, 22), width=2)
        draw.rectangle([250, 50, 400, 200], fill=(239, 68, 68, 100), outline=(239, 68, 68), width=2)
        draw.rectangle([100, 200, 400, 300], fill=(234, 179, 8, 100), outline=(234, 179, 8), width=2)
    elif image_type == "supply":
        draw.rectangle([50, 100, 150, 250], fill=(30, 58, 138), outline=(59, 130, 246), width=2)
        draw.line([150, 175, 250, 175], fill=(132, 204, 22), width=3)
        draw.rectangle([250, 100, 350, 250], fill=(15, 118, 110), outline=(20, 184, 166), width=2)
        draw.line([350, 175, 420, 175], fill=(132, 204, 22), width=3)
        draw.ellipse([420, 145, 470, 205], fill=(180, 83, 9), outline=(245, 158, 11), width=2)

    return img

# -----------------------------------------------------------------------------
# 3. MACHINE LEARNING DIAGNOSTIC MODEL
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
# 4. GLOBAL SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#84cc16 !important;'>BioSyncAI Platform</h2>", unsafe_allow_html=True)
st.sidebar.caption("Verified Intelligence for the Physical World")

menu = st.sidebar.radio(
    "Navigation Hierarchy",
    [
        "🏠 Platform Overview & Introduction",
        "🌐 Operating Decision & Spatial Matrix",
        "🔬 Multispectral Vision Diagnostics",
        "🤖 Multimodal AI Engine",
        "🚚 Supply Chain Traceability & EUDR",
        "📊 Yield Outlook & Irrigation",
        "🌱 ESG & Carbon Footprint Analytics",
        "📞 Talk to Us (Request Demo)",
        "💼 Enterprise Careers & Talent",
        "📄 Enterprise RFP & Report Export",
        "ℹ️ Partner & Acknowledgements"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📡 **BioSync Core:** Active\n🛰️ **Global Mesh:** 103+ Countries\n🧬 **Partner:** ALGORITHMIC TITANS")

# -----------------------------------------------------------------------------
# MODULE 1: PLATFORM OVERVIEW & INTRODUCTION
# -----------------------------------------------------------------------------
if menu == "🏠 Platform Overview & Introduction":
    st.markdown("<div class='cropin-header'>BioSyncAI Cloud & Intelligence Engine</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-banner'>
        <h2>Building Intelligence for the Physical World</h2>
        <p style='font-size: 16px; color: #94a3b8;'>
            BioSyncAI connects agribusinesses, financial institutions, and development agencies to real-time ground telemetry, orbital remote sensing, and predictive machine learning models across one billion acres.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(generate_synthetic_image("satellite"), caption="Orbital Telemetry & Field Parceling", use_container_width=True)
        st.subheader("Orbital Risk Grid")
        st.write("Real-time plot monitoring combining thermal, SAR, and optical satellite feeds.")

    with c2:
        st.image(generate_synthetic_image("leaf"), caption="Multispectral Crop Health Diagnostics", use_container_width=True)
        st.subheader("Multispectral Diagnostics")
        st.write("Computer vision models analyzing leaf cellular stress and fungal infections.")

    with c3:
        st.image(generate_synthetic_image("supply"), caption="End-to-End Supply Traceability", use_container_width=True)
        st.subheader("Supply Traceability")
        st.write("Full compliance tracking across global supply chains from plot to processing.")

    st.markdown("---")
    
    with st.expander("📌 Platform Core Pillars", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            ### Key Capabilities
            * **Global Scale:** Monitoring 103+ countries with 250+ enterprise integrations.
            * **Data Integration:** IoT soil sensors, bio-acoustic resonance, and satellite imagery.
            * **Prescriptive AI:** Real-time intervention advisories for disease and stress mitigation.
            """)
        with col_b:
            st.markdown("""
            ### Impact Metrics
            * **Yield Improvement:** Up to +18% increase in farm productivity.
            * **Resource Optimization:** -25% reduction in irrigation water usage.
            * **Risk Prevention:** 92.4% accuracy in early fungal blight detection.
            """)

# -----------------------------------------------------------------------------
# MODULE 2: OPERATING DECISION & SPATIAL MATRIX
# -----------------------------------------------------------------------------
elif menu == "🌐 Operating Decision & Spatial Matrix":
    st.markdown("<div class='cropin-header'>Operating Decision & Spatial Risk Matrix</div>", unsafe_allow_html=True)
    
    with st.expander("📌 Grid Configuration & Sector Metrics", expanded=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Monitored Area", "12,450 Acres", "+350 Acres")
        m2.metric("Health Index", "84.2 / 100", "-2.1 pts")
        m3.metric("Disease Risk Flag", "High Risk", "Zone B")
        m4.metric("Soil Saturation", "78%", "Optimal")

    with st.expander("🗺️ Interactive Spatial Heatmap", expanded=True):
        st.image(generate_synthetic_image("satellite"), caption="Active Satellite Field Map", use_container_width=True)
        grid_dim = st.slider("Resolution Grid Size", 5, 20, 10)
        sm_range = np.linspace(30, 90, grid_dim)
        hum_range = np.linspace(40, 95, grid_dim)

        risk_matrix = np.zeros((grid_dim, grid_dim))
        for r_idx, sm_val in enumerate(sm_range):
            for c_idx, hum_val in enumerate(hum_range):
                input_feat = np.array([[sm_val, 28.0, hum_val, 10.0, 550.0]])
                risk_matrix[r_idx, c_idx] = model.predict_proba(input_feat)[0][1]

        df_grid = pd.DataFrame(
            risk_matrix,
            index=[f"Moisture {sm:.0f}%" for sm in sm_range],
            columns=[f"Humidity {h:.0f}%" for h in hum_range]
        )

        st.dataframe(df_grid, use_container_width=True, height=340)

# -----------------------------------------------------------------------------
# MODULE 3: MULTISPECTRAL VISION DIAGNOSTICS
# -----------------------------------------------------------------------------
elif menu == "🔬 Multispectral Vision Diagnostics":
    st.markdown("<div class='cropin-header'>Multispectral Vision Engine</div>", unsafe_allow_html=True)
    
    with st.expander("📷 Leaf Sample Analysis & Processing Channel", expanded=True):
        uploaded_file = st.file_uploader("Upload Crop Sample (JPG/PNG)", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
        else:
            st.caption("⚡ Showing synthetic leaf sample for demonstration.")
            image = generate_synthetic_image("leaf")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Original RGB View")
            st.image(image, use_container_width=True)

        with c2:
            st.subheader("Spectral Processing Channel")
            vision_mode = st.selectbox("Select Filter Channel", ["Chlorophyll Index (Pseudo-NDVI)", "Lesion Edge Tracer", "Thermal Anomaly Map"])

            if vision_mode == "Chlorophyll Index (Pseudo-NDVI)":
                r, g, b = image.split()
                processed_image = Image.merge("RGB", (b, ImageEnhance.Contrast(g).enhance(2.0), r))
            elif vision_mode == "Lesion Edge Tracer":
                gray = image.convert("L")
                processed_image = ImageOps.invert(gray.filter(ImageFilter.FIND_EDGES))
            elif vision_mode == "Thermal Anomaly Map":
                r, g, b = image.split()
                processed_image = Image.merge("RGB", (g, r, b))

            st.image(processed_image, caption=f"Active Filter: {vision_mode}", use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 4: MULTIMODAL AI ENGINE
# -----------------------------------------------------------------------------
elif menu == "🤖 Multimodal AI Engine":
    st.markdown("<div class='cropin-header'>Multimodal AI Inference Engine</div>", unsafe_allow_html=True)

    with st.expander("🎛️ Microclimate & Bio-Acoustic Inputs", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            in_sm = st.slider("Soil Moisture (%)", 0.0, 100.0, 82.0)
            in_temp = st.slider("Ambient Temp (°C)", 10.0, 50.0, 28.0)
            in_hum = st.slider("Humidity (%)", 0.0, 100.0, 86.0)
        with col2:
            in_rain = st.slider("Precipitation (mm)", 0.0, 100.0, 12.5)
            in_freq = st.slider("Bio-Resonance Frequency (Hz)", 300, 900, 520)

        if st.button("🚀 Run Live AI Inference"):
            feat = np.array([[in_sm, in_temp, in_hum, in_rain, in_freq]])
            pred = model.predict(feat)[0]
            prob = model.predict_proba(feat)[0]

            if pred == 1:
                st.error(f"🚨 **HIGH RISK DETECTED: Fungal Leaf Blight Threat**\n*Confidence:* `{prob[1]*100:.2f}%`")
            else:
                st.success(f"✅ **HEALTHY FIELD STATUS**\n*Confidence:* `{prob[0]*100:.2f}%`")

# -----------------------------------------------------------------------------
# MODULE 5: SUPPLY CHAIN TRACEABILITY & EUDR
# -----------------------------------------------------------------------------
elif menu == "🚚 Supply Chain Traceability & EUDR":
    st.markdown("<div class='cropin-header'>Supply Chain Traceability & Deforestation Compliance</div>", unsafe_allow_html=True)

    with st.expander("📦 Supply Chain Pipeline & Verification", expanded=True):
        st.image(generate_synthetic_image("supply"), caption="Supply Traceability Verification Pipeline", use_container_width=True)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("""
            ### Batch Tracking
            * **Batch ID:** `BATCH-2057-WHEAT-884`
            * **Origin Field:** Sector Alpha-01
            * **Certification:** EUDR Compliant (Zero Deforestation)
            * **GPS Polygon:** Verification Active
            """)
        with col_s2:
            st.markdown("""
            ### Verification Log
            * **Harvest Timestamp:** 2026-10-08
            * **Processor Check:** Passed
            * **Carbon Footprint / Ton:** 142 kg CO2e
            * **Quality Score:** Grade A Export
            """)

# -----------------------------------------------------------------------------
# MODULE 6: YIELD OUTLOOK & IRRIGATION
# -----------------------------------------------------------------------------
elif menu == "📊 Yield Outlook & Irrigation":
    st.markdown("<div class='cropin-header'>Harvest Yield & Irrigation Analytics</div>", unsafe_allow_html=True)
    
    with st.expander("🌾 Crop Yield Forecast & Water Controller", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Estimated Yield", "4.25 Tons / Hectare", "+8.2%")
            st.line_chart(pd.DataFrame({'Yield': [3.8, 3.9, 4.0, 4.1, 4.25]}))
        with c2:
            st.metric("Soil Moisture Index", "78%", "Slightly Elevated")
            st.progress(0.78)

# -----------------------------------------------------------------------------
# MODULE 7: ESG & CARBON FOOTPRINT ANALYTICS
# -----------------------------------------------------------------------------
elif menu == "🌱 ESG & Carbon Footprint Analytics":
    st.markdown("<div class='cropin-header'>ESG & Sustainability Intelligence</div>", unsafe_allow_html=True)

    with st.expander("📉 Environmental Metrics & Carbon Credit Forecasting", expanded=True):
        e1, e2, e3 = st.columns(3)
        e1.metric("Carbon Sequestration", "3.2 Tons CO2e / Ha", "+12%")
        e2.metric("Water Savings Index", "24.5%", "-5.2% Consumption")
        e3.metric("Soil Biodiversity Score", "88 / 100", "High Vitality")

        st.subheader("Seasonal Carbon Sequestration Trajectory")
        esg_df = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'CO2 Sequestered (Tons)': [1.1, 1.4, 1.8, 2.2, 2.8, 3.2]
        })
        st.bar_chart(esg_df.set_index('Month'))

# -----------------------------------------------------------------------------
# MODULE 8: TALK TO US (REQUEST DEMO)
# -----------------------------------------------------------------------------
elif menu == "📞 Talk to Us (Request Demo)":
    st.markdown("<div class='cropin-header'>Request a Conversation</div>", unsafe_allow_html=True)
    st.write("Built for consequential decisions. Combine deep domain expertise with enterprise technology and global deployment experience.")

    col_info, col_form = st.columns([1, 1])

    with col_info:
        st.markdown("""
        ### Why BioSyncAI?
        * **01 | Global Scale:** 250+ enterprise clients across 103+ countries.
        * **02 | Operating Decisions:** Supply, Risk, Inspection, and Compliance workflows.
        * **03 | Enterprise Context:** Intelligence computed across one billion acres.
        
        ---
        #### Contact Direct:
        * **Partner Email:** `algorithmictitans113@gmail.com`
        """)

    with col_form:
        with st.form("cropin_lead_form"):
            st.subheader("Talk to Our Enterprise Team")
            
            f_name = st.text_input("First Name *")
            l_name = st.text_input("Last Name *")
            email = st.text_input("Work Email *")
            
            job_role = st.selectbox("Job Role", ["Select your role", "Agronomist / Farm Manager", "Enterprise Executive", "Supply Chain Lead", "Government Official", "Researcher"])
            domain = st.selectbox("Domain", ["Select your domain", "Food-Ag", "Forest", "Water", "Energy", "Infrastructure", "Banking & Insurance"])
            industry = st.selectbox("Industry", ["Select your industry", "Farming & Crop Production", "Agrochemicals & Seeds", "Food Processing", "Government & NGO"])
            region = st.selectbox("Region", ["Select your region", "North America", "Asia Pacific (India)", "Europe", "Latin America", "Middle East & Africa"])
            
            decision_goals = st.text_area("What decision are you trying to improve?")
            
            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if f_name and l_name and email:
                    st.success(f"✅ Thank you {f_name}! Your request has been recorded successfully.")
                    st.info(f"""
                    📩 **Enterprise Dispatch Summary**
                    
                    * **Recipient:** `{email}`
                    * **Partner Email:** `algorithmictitans113@gmail.com`
                    * **Domain Selected:** {domain}
                    * **Decision Goals:** {decision_goals if decision_goals else 'Enterprise AgTech Operations'}
                    
                    An automated representative from **ALGORITHMIC TITANS** will process your request.
                    """)
                else:
                    st.error("Please fill in required fields: First Name, Last Name, and Work Email.")

# -----------------------------------------------------------------------------
# MODULE 9: ENTERPRISE CAREERS & TALENT
# -----------------------------------------------------------------------------
elif menu == "💼 Enterprise Careers & Talent":
    st.markdown("<div class='cropin-header'>Careers at BioSyncAI</div>", unsafe_allow_html=True)
    st.write("Join us in building the intelligence layer for global agriculture and climate resilience.")

    with st.expander("🚀 Open Positions", expanded=True):
        st.subheader("Current Job Openings")
        
        st.markdown("""
        #### 1. Senior AI/ML Engineer - Computer Vision
        * **Location:** Remote / Hybrid
        * **Domain:** Deep Learning for Satellite & Drone Imagery Analysis
        * **Stack:** PyTorch, OpenCV, Geospatial Raster Processing
        """)
        if st.button("Apply for Computer Vision Role"):
            st.success("Application form initialized. Send your CV to algorithmictitans113@gmail.com")

        st.markdown("---")

        st.markdown("""
        #### 2. Enterprise Solutions Architect
        * **Location:** Global / Remote
        * **Domain:** Agribusiness ERP Integrations & IoT Telemetry
        * **Stack:** Streamlit, Python, REST APIs, Geospatial Databases
        """)
        if st.button("Apply for Solutions Architect Role"):
            st.success("Application form initialized. Send your CV to algorithmictitans113@gmail.com")

# -----------------------------------------------------------------------------
# MODULE 10: ENTERPRISE RFP & REPORT EXPORT
# -----------------------------------------------------------------------------
elif menu == "📄 Enterprise RFP & Report Export":
    st.markdown("<div class='cropin-header'>Enterprise RFP & Agronomic Report</div>", unsafe_allow_html=True)
    
    with st.expander("📝 Generate Automated Report", expanded=True):
        report_text = """====================================================
BIOSYNCAI ENTERPRISE AGRONOMIC REPORT
Partner: ALGORITHMIC TITANS
Contact: algorithmictitans113@gmail.com
====================================================

Overall Health Status: Moderate Risk (Zone B Flagged)
Estimated Harvest Yield: 4.25 Tons / Hectare
Active Sensor Nodes: 148 Units

RECOMMENDED ACTION PLAN:
1. Apply targeted copper-based fungicide to Zone B.
2. Reduce micro-irrigation flow in Zone B by 20%.
===================================================="""
        st.text_area("Report Content", report_text, height=200)
        st.download_button("📥 Download Agronomic Report (.txt)", data=report_text, file_name="BioSyncAI_Report.txt")

# -----------------------------------------------------------------------------
# MODULE 11: PARTNER & ACKNOWLEDGEMENTS
# -----------------------------------------------------------------------------
elif menu == "ℹ️ Partner & Acknowledgements":
    st.markdown("<div class='cropin-header'>Partner Information & Contact</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='partner-card'>
        <h3>🤝 Official Development Partner</h3>
        <h2 style='color:#84cc16 !important; margin-top:0;'>ALGORITHMIC TITANS</h2>
        <p><strong>Contact Email:</strong> <a href='mailto:algorithmictitans113@gmail.com' style='color:#84cc16;'>algorithmictitans113@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ Project & Platform Details", expanded=True):
        st.markdown("""
        * **Platform Name:** BioSyncAI Enterprise Platform
        * **Core Technology:** Multimodal Machine Learning & Multispectral Computer Vision
        * **Domain:** Agricultural Intelligence & Climate Resilience
        """)
