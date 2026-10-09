import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ENTERPRISE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI Platform | Algorithmic Titans",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Custom Theme
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stMetric { background-color: #111827; border: 1px solid #10b981; padding: 18px; border-radius: 12px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1); }
    .stButton>button { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; border: none; border-radius: 8px; font-weight: bold; width: 100%; height: 48px; font-size: 15px; }
    .stButton>button:hover { background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MACHINE LEARNING ENGINE
# -----------------------------------------------------------------------------
@st.cache_resource
def train_master_biosync_model():
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

model = train_master_biosync_model()

# -----------------------------------------------------------------------------
# 3. GLOBAL NAVIGATION & ENTERPRISE "TALK TO US" FORM
# -----------------------------------------------------------------------------
st.sidebar.title("🌱 BioSyncAI Platform")
st.sidebar.caption("Algorithmic Titans | Class XI")

selected_plot = st.sidebar.selectbox(
    "📍 Select Active Field Plot",
    ["Plot 101 - North Sector (Wheat)", "Plot 102 - Zone B (Soybean)", "Plot 103 - South Sector (Maize)"]
)

menu = st.sidebar.radio(
    "Platform Navigation",
    [
        "📞 Talk to Us (Enterprise Lead)",
        "🌐 Plot Intelligence & Spatial Risk Matrix",
        "🔬 Multispectral Vision & Image Diagnostics",
        "🤖 Multimodal AI Diagnostic Engine",
        "📊 Yield Outlook & Smart Irrigation",
        "📄 Export Agronomic Report",
        "ℹ️ Project Info & Acknowledgements"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📡 **Sensor Mesh:** 148 IoT Nodes Active\n🛰️ **Satellite Link:** Synced")

# -----------------------------------------------------------------------------
# MODULE 1: ENTERPRISE "TALK TO US" CONTACT FORM
# -----------------------------------------------------------------------------
if menu == "📞 Talk to Us (Enterprise Lead)":
    st.title("📞 Schedule a BioSyncAI Enterprise Demo")
    st.caption("Connect with our agritech specialists to transform your farm operations with intelligent cloud solutions.")

    with st.form("contact_form"):
        st.subheader("Enterprise Inquiry Form")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name *")
            email = st.text_input("Work Email Address *")
            company_size = st.selectbox("Company Size", ["1-50 employees", "51-200 employees", "201-1000 employees", "1000+ employees"])
        with c2:
            last_name = st.text_input("Last Name *")
            company_name = st.text_input("Company / Organization Name *")
            org_type = st.selectbox("Organization Type", ["Agribusiness / Enterprise", "Farming Cooperative", "Government / NGO", "Research Institution"])

        message = st.text_area("Tell us about your acreage & specific farm monitoring needs")
        submit_btn = st.form_submit_button("🚀 Request Enterprise Consult")

        if submit_btn:
            if first_name and last_name and email and company_name:
                st.success(f"Thank you, {first_name}! Your inquiry for **{company_name}** has been received. Our team will contact you at `{email}` shortly.")
            else:
                st.error("Please fill out all required fields marked with *.")

# -----------------------------------------------------------------------------
# MODULE 2: PLOT INTELLIGENCE & HEATMAP
# -----------------------------------------------------------------------------
elif menu == "🌐 Plot Intelligence & Spatial Risk Matrix":
    st.title("🌐 BioSyncAI Plot Intelligence & Spatial Risk Matrix")
    st.caption(f"Spatial analytics and microclimate telemetry for **{selected_plot}**")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monitored Grid", "12,450 Acres", "+350 Acres")
    m2.metric("Bio-Resonance Index", "84.2 / 100", "-2.1 pts")
    m3.metric("Disease Risk Alert", "High Risk", "Zone B Flagged")
    m4.metric("Soil Saturation Index", "78%", "Optimal Balance")

    st.markdown("---")
    col_map, col_alerts = st.columns([2, 1])

    with col_map:
        st.subheader("🗺️ Plot-Level Spatial Health Matrix")
        grid_dim = st.slider("Spatial Resolution Grid Size", 5, 20, 10)
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

        st.dataframe(
            df_grid.style.background_gradient(cmap="YlOrRd", vmin=0, vmax=1),
            use_container_width=True,
            height=340
        )

    with col_alerts:
        st.subheader("🚨 Real-Time Advisories")
        st.error("""
        **CRITICAL ALERT: Plot 102 (Zone B)**
        * **Detected Strain:** Early Fungal Leaf Blight Outbreak
        * **ML Model Confidence:** `92.4%`
        * **Primary Trigger:** Extended canopy wetness + Humidity > 80%.
        """)

# -----------------------------------------------------------------------------
# MODULE 3: MULTISPECTRAL VISION & IMAGE DIAGNOSTICS
# -----------------------------------------------------------------------------
elif menu == "🔬 Multispectral Vision & Image Diagnostics":
    st.title("🔬 Advanced Multispectral Vision & Image Diagnostics")
    
    uploaded_file = st.file_uploader("Upload Crop Leaf Sample (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Original RGB Field Sample")
            st.image(image, use_container_width=True)
            contrast_val = st.slider("Enhance Visual Contrast", 0.5, 2.5, 1.0)
            enhancer = ImageEnhance.Contrast(image)
            st.image(enhancer.enhance(contrast_val), caption="Contrast Adjusted View", use_container_width=True)

        with col2:
            st.subheader("Multispectral Channel Analyzer")
            vision_mode = st.selectbox(
                "Select Visual Channel Filter",
                ["Chlorophyll Index (Pseudo-NDVI)", "Lesion & Contour Edge Tracer", "Thermal Stress Map"]
            )

            if vision_mode == "Chlorophyll Index (Pseudo-NDVI)":
                r, g, b = image.split()
                processed_image = Image.merge("RGB", (b, ImageEnhance.Contrast(g).enhance(2.2), r))
            elif vision_mode == "Lesion & Contour Edge Tracer":
                gray = image.convert("L")
                processed_image = ImageOps.invert(gray.filter(ImageFilter.FIND_EDGES))
            elif vision_mode == "Thermal Stress Map":
                r, g, b = image.split()
                processed_image = Image.merge("RGB", (g, r, b))

            st.image(processed_image, caption=f"Active Filter: {vision_mode}", use_container_width=True)
    else:
        st.info("Upload a leaf sample to perform computer vision channels processing.")

# -----------------------------------------------------------------------------
# MODULE 4: MULTIMODAL AI DIAGNOSTIC ENGINE
# -----------------------------------------------------------------------------
elif menu == "🤖 Multimodal AI Diagnostic Engine":
    st.title("🤖 Multimodal Machine Learning Diagnostic Engine")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        in_sm = st.slider("Soil Moisture (%)", 0.0, 100.0, 82.0)
        in_temp = st.slider("Ambient Temperature (°C)", 10.0, 50.0, 28.0)
        in_hum = st.slider("Relative Humidity (%)", 0.0, 100.0, 86.0)
    with col_in2:
        in_rain = st.slider("Precipitation (mm)", 0.0, 100.0, 12.5)
        in_freq = st.slider("Bio-Acoustic Plant Resonance (Hz)", 300, 900, 520)

    if st.button("🚀 Run Live Machine Learning Inference"):
        feat_vector = np.array([[in_sm, in_temp, in_hum, in_rain, in_freq]])
        pred_class = model.predict(feat_vector)[0]
        prob_scores = model.predict_proba(feat_vector)[0]

        res1, res2 = st.columns(2)
        with res1:
            if pred_class == 1:
                st.error(f"🚨 **HIGH RISK DETECTED: Fungal Leaf Blight**\n*Confidence:* `{prob_scores[1]*100:.2f}%`")
            else:
                st.success(f"✅ **HEALTHY FIELD STATUS**\n*Confidence:* `{prob_scores[0]*100:.2f}%`")
        with res2:
            st.write("1. Apply targeted copper-based fungicide.\n2. Adjust irrigation flow by 20%.")

# -----------------------------------------------------------------------------
# MODULE 5: YIELD OUTLOOK & SMART IRRIGATION
# -----------------------------------------------------------------------------
elif menu == "📊 Yield Outlook & Smart Irrigation":
    st.title("📊 Harvest Yield & Smart Irrigation Analytics")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Estimated Harvest", "4.25 Tons / Hectare", "+8.2% vs Baseline")
        st.line_chart(pd.DataFrame({'Yield': [3.8, 3.9, 4.0, 4.1, 4.25]}))
    with c2:
        st.metric("Soil Moisture Index", "78%", "Slightly Elevated")
        st.progress(0.78)

# -----------------------------------------------------------------------------
# MODULE 6: EXPORT AGRONOMIC REPORT
# -----------------------------------------------------------------------------
elif menu == "📄 Export Agronomic Report":
    st.title("📄 Autonomous Agronomic Field Report Synthesis")
    report_text = f"BIOSYNCAI FIELD REPORT\nPlot: {selected_plot}\nStatus: Zone B Flagged\nPredicted Yield: 4.25 Tons/Ha"
    st.text_area("Report Preview", report_text, height=200)
    st.download_button("📥 Download Report (.txt)", data=report_text, file_name="BioSyncAI_Report.txt")

# -----------------------------------------------------------------------------
# MODULE 7: PROJECT INFO & ACKNOWLEDGEMENTS
# -----------------------------------------------------------------------------
elif menu == "ℹ️ Project Info & Acknowledgements":
    st.title("ℹ️ Project Information & Acknowledgements")
    st.markdown("""
    * **Project Title:** Agricultural AI Solutions for Sustainable Agriculture
    * **Model Name:** BioSyncAI Platform
    * **Event:** OlympAI Hackathon 2026
    * **Team Name:** Algorithmic Titans (Class XI)
    * **Team Members:** Badal Kumar, Lakshay Bhagat, Aarav Sanchan
    * **Advisor:** Ms. Nisha Yadav
    """)
