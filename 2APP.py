import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & COMPLETE FULL-SCREEN DARK THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI | Enterprise Intelligence Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Dark Theme Injection across all parent containers, viewports, and text elements
st.markdown("""
    <style>
    /* Force overall application background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }

    /* Force Main Viewport & Block Containers */
    [data-testid="stMainBlockContainer"], .main, .block-container {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }

    /* Force Header & Toolbar Transparency */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #04080e !important;
        color: #f1f5f9 !important;
    }

    /* Sidebar Background & Borders */
    section[data-testid="stSidebar"] {
        background-color: #0d1520 !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Cards, Metrics, Dataframes, and Expanders */
    .stMetric, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #0d1520 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* Input Controls, Selectboxes, and Text Areas */
    input, textarea, select, div[data-baseweb="select"] {
        background-color: #0d1520 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }

    /* Text & Headers Override */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #f1f5f9 !important;
    }

    /* Primary Accent Buttons (Cropin Lime Green) */
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

    /* Custom Header & Partner Card Styling */
    .cropin-header {
        color: #84cc16 !important;
        font-size: 28px;
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
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MACHINE LEARNING DIAGNOSTIC MODEL
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
# 3. GLOBAL SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#84cc16 !important;'>BioSyncAI Platform</h2>", unsafe_allow_html=True)
st.sidebar.caption("Verified Intelligence for the Physical World")

menu = st.sidebar.radio(
    "Navigation Hierarchy",
    [
        "📞 Talk to Us (Request Demo)",
        "🌐 Operating Decision & Spatial Matrix",
        "🔬 Multispectral Vision Diagnostics",
        "🤖 Multimodal AI Engine",
        "📊 Yield Outlook & Irrigation",
        "📄 Enterprise RFP & Report Export",
        "ℹ️ Partner & Acknowledgements"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📡 **BioSync Core:** Active\n🛰️ **Global Mesh:** 103+ Countries\n🧬 **Partner:** ALGORITHMIC TITANS")

# -----------------------------------------------------------------------------
# MODULE 1: TALK TO US (CROPIN COPYCAT SALES FUNNEL)
# -----------------------------------------------------------------------------
if menu == "📞 Talk to Us (Request Demo)":
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
        * **Global Support:** +1 202 555 0101
        """)

    with col_form:
        with st.form("cropin_lead_form"):
            st.subheader("Talk to Our Enterprise Team")
            
            f_name = st.text_input("First Name *")
            l_name = st.text_input("Last Name *")
            email = st.text_input("Work Email *")
            phone = st.text_input("Phone Number (+1 202 555 0101)")
            
            job_role = st.selectbox("Job Role", ["Select your role", "Agronomist / Farm Manager", "Enterprise Executive", "Supply Chain Lead", "Government Official", "Researcher"])
            domain = st.selectbox("Domain", ["Select your domain", "Food-Ag", "Forest", "Water", "Energy", "Infrastructure", "Banking & Insurance"])
            industry = st.selectbox("Industry", ["Select your industry", "Farming & Crop Production", "Agrochemicals & Seeds", "Food Processing", "Government & NGO"])
            region = st.selectbox("Region", ["Select your region", "North America", "Asia Pacific (India)", "Europe", "Latin America", "Middle East & Africa"])
            
            decision_goals = st.text_area("What decision are you trying to improve?")
            
            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if f_name and l_name and email:
                    st.success(f"✅ Thank you {f_name}! Your request has been recorded.")
                    
                    st.info(f"""
                    📩 **Automated Message Dispatch Sent To:** `{email}`
                    
                    ---
                    **From:** BioSyncAI Enterprise Team <algorithmictitans113@gmail.com>  
                    **Subject:** Confirmation - BioSyncAI Enterprise Consultation Request  
                    
                    Dear {f_name} {l_name},
                    
                    Thank you for reaching out to BioSyncAI. We have received your inquiry for the **{domain}** domain ({industry}). 
                    Our enterprise lead representative will review your requirements regarding:
                    *"{decision_goals if decision_goals else 'Enterprise Operations'}"*
                    
                    We will get in touch with you shortly at {email} or {phone}.
                    
                    Best regards,  
                    **BioSyncAI Enterprise Team**  
                    Partner: ALGORITHMIC TITANS
                    """)
                else:
                    st.error("Please enter required fields: First Name, Last Name, and Work Email.")

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
# MODULE 5: YIELD OUTLOOK & IRRIGATION
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
# MODULE 6: ENTERPRISE RFP & REPORT EXPORT
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
# MODULE 7: PARTNER & ACKNOWLEDGEMENTS
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
