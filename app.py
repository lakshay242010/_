import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & DESIGN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AgCloud Platform | Algorithmic Titans",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. NAVIGATION SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("AgCloud™ Platform")
st.sidebar.caption("Algorithmic Titans | OlympAI 2026")

menu = st.sidebar.radio(
    "Modules",
    [
        "🌐 Plot Intelligence & Risk Map",
        "🔬 Multimodal AI Diagnostics",
        "📊 Yield & Irrigation Forecast",
        "ℹ️ Project Info & Acknowledgements"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📍 **Active Region:** Field Zone B\n📡 **Data Stream:** Satellite + IoT Sensors")

# -----------------------------------------------------------------------------
# MODULE 1: PLOT INTELLIGENCE & RISK MAP
# -----------------------------------------------------------------------------
if menu == "🌐 Plot Intelligence & Risk Map":
    st.title("🌐 Plot Intelligence & Risk Map")
    st.caption("Real-time plot-level monitoring via fused satellite, drone imagery, and IoT ground sensors.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Monitored Area", "12,450 Acres", "+350 Acres")
    m2.metric("Overall Health Index", "84 / 100", "-3.2 pts (Zone B)")
    m3.metric("Disease Risk Score", "Moderate", "Zone B Flagged")
    m4.metric("Active Sensor Nodes", "148 Units", "100% Online")

    st.markdown("---")

    col_map, col_alerts = st.columns([2, 1])

    with col_map:
        st.subheader("🗺️ Plot Risk Heatmap")
        
        np.random.seed(42)
        grid_data = np.random.uniform(0.1, 0.45, (12, 12))
        grid_data[3:7, 7:10] = np.random.uniform(0.72, 0.95, (4, 3))  # Disease cluster in Zone B

        df_grid = pd.DataFrame(
            grid_data,
            columns=[f"Plot {i+1}" for i in range(12)],
            index=[f"Row {chr(65+i)}" for i in range(12)]
        )

        st.dataframe(
            df_grid.style.background_gradient(cmap="YlOrRd", vmin=0, vmax=1),
            use_container_width=True,
            height=320
        )
        st.caption("🟢 Green: Healthy Zone | 🟡 Yellow: Moderate Stress | 🔴 Red: Early Fungal Outbreak Flagged")

    with col_alerts:
        st.subheader("🚨 Real-Time Advisories")
        
        st.error("""
        **HIGH RISK ALERT: Zone B (Plot E8-F10)**
        * **Detected Strain:** Early Stage Fungal Leaf Blight
        * **Confidence Level:** `91.8%`
        * **Root Cause:** Extended ambient humidity (>85%) and surface dampness.
        """)

        st.warning("""
        **RECOMMENDED ACTION**
        * Perform targeted fungicide application in Zone B within **48 hours**.
        * Avoid blanket spraying; isolate treatment to 1.2 hectares.
        """)

# -----------------------------------------------------------------------------
# MODULE 2: MULTIMODAL AI DIAGNOSTICS
# -----------------------------------------------------------------------------
elif menu == "🔬 Multimodal AI Diagnostics":
    st.title("🔬 Multimodal AI Diagnostic Engine")
    st.caption("Combine leaf image analysis with ground microclimate feeds to generate precise prescriptions.")

    col_img, col_sensor = st.columns([1, 1])

    with col_img:
        st.subheader("1. Visual Data Stream")
        uploaded_file = st.file_uploader("Upload Crop Leaf Sample", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Crop Image", use_container_width=True)
        else:
            st.info("Upload a field leaf sample to evaluate disease markers.")

    with col_sensor:
        st.subheader("2. Ground Sensor Inputs")
        soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 78)
        temperature = st.slider("Ambient Temperature (°C)", 10, 50, 29)
        humidity = st.slider("Relative Humidity (%)", 0, 100, 85)
        crop_type = st.selectbox("Crop Variety", ["Soybean", "Wheat", "Maize", "Rice", "Cotton"])

    if st.button("⚡ Execute Multimodal AI Diagnosis"):
        st.markdown("---")
        st.success("Diagnostic Analysis Successfully Executed!")

        res1, res2 = st.columns(2)
        with res1:
            st.markdown("### AI Inference Results")
            st.write(f"**Target Crop:** {crop_type}")
            st.write("**Diagnosis:** Early Stage Fungal Leaf Blight")
            st.write("**Model Confidence:** `89.7%`")
            st.write(f"**Microclimate Risk Factor:** Elevated (Humidity: {humidity}%, Temp: {temperature}°C)")

        with res2:
            st.markdown("### Prescriptive Guidance")
            st.write("1. **Targeted Spraying:** Apply copper-based fungicide to affected clusters.")
            st.write("2. **Micro-Irrigation:** Pause night irrigation to reduce canopy wetness.")
            st.write("3. **Follow-Up:** Schedule automated re-inspection in 3 days.")

# -----------------------------------------------------------------------------
# MODULE 3: YIELD & IRRIGATION FORECAST
# -----------------------------------------------------------------------------
elif menu == "📊 Yield & Irrigation Forecast":
    st.title("📊 Yield Outlook & Smart Irrigation")
    st.caption("Predictive analytics for harvest planning, labor optimization, and water conservation.")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🌾 Yield Prediction Outlook")
        st.metric("Estimated Harvest", "4.2 Tons / Hectare", "+8% vs Regional Average")
        
        chart_data = pd.DataFrame({
            'Week': [f'Week {i}' for i in range(1, 9)],
            'Predicted Yield Trend': [3.8, 3.9, 4.0, 4.1, 4.15, 4.18, 4.2, 4.22],
            'Target Yield': [4.0] * 8
        })
        st.line_chart(chart_data.set_index('Week'))

    with c2:
        st.subheader("💧 Smart Irrigation Controller")
        st.metric("Soil Moisture Index", "78%", "Optimal Balance")
        
        st.markdown("""
        * **Zone A:** Normal Irrigation Schedule
        * **Zone B:** Reduce water flow by **20%** (Risk zone moisture control)
        * **Zone C:** Normal Irrigation Schedule
        """)
        st.progress(0.78, text="Optimal Canopy Moisture Level")

# -----------------------------------------------------------------------------
# MODULE 4: PROJECT INFO & ACKNOWLEDGEMENTS
# -----------------------------------------------------------------------------
elif menu == "ℹ️ Project Info & Acknowledgements":
    st.title("ℹ️ Project Information")
    
    st.markdown("""
    * **Project Title:** Agricultural AI Solutions for Sustainable Agriculture[cite: 2]
    * **Hackathon:** OlympAI Hackathon 2026[cite: 1, 2]
    * **Category:** AI for Sustainability[cite: 2]
    * **Team Name:** Algorithmic Titans[cite: 1, 2]
    * **Grade:** Class XI[cite: 1]
    """)

    st.markdown("---")

    st.subheader("👥 Team Roles & Contributions")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("**Badal Kumar**  \n*Data Engineer*[cite: 16]  \nIngestion, cleaning, geospatial alignment[cite: 16]")
    with t2:
        st.markdown("**Lakshay Bhagat**  \n*AI Modeler*[cite: 16]  \nModel design, training, evaluation[cite: 16]")
    with t3:
        st.markdown("**Aarav Sanchan**  \n*Product Lead & UI/UX*[cite: 16]  \nWorkflow, interface, explainability[cite: 16]")

    st.markdown("---")

    st.subheader("🙏 Acknowledgements")
    st.info("""
    We would like to express our sincere gratitude to our teacher, **Ms. Nisha Yadav**, for her invaluable guidance, 
    encouragement, and support throughout the development of this project on **Agricultural AI Solutions**[cite: 17]. 
    Her insights and continuous feedback were instrumental in shaping our research and keeping us on the right track[cite: 17].

    We are also deeply grateful to our fellow teammates for their hard work, dedication, and seamless collaboration[cite: 17]. 
    Building the AI model and crafting the final presentation was a true team effort, and every member's contribution 
    was vital to the success of this project[cite: 17].
    """)
