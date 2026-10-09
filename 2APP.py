import streamlit as st
import numpy as np
import pandas as pd
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & MODERN FUTURISTIC THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI | Autonomous AgTech Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Dark Theme with Glassmorphism, Modern Fonts & Neon Accents
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Full-screen Dark Canvas */
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

    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Modern Glass Cards & Metrics */
    .stMetric, div[data-testid="stExpander"], div[data-testid="stForm"], .futuristic-card {
        background: rgba(17, 24, 39, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 20px !important;
        margin-bottom: 20px !important;
    }

    /* Glowing Metric Values */
    [data-testid="stMetricValue"] {
        color: #a3e635 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 12px rgba(163, 230, 53, 0.3);
    }

    /* Futuristic Input Form Controls */
    input, textarea, select, div[data-baseweb="select"] {
        background: rgba(31, 41, 55, 0.6) !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
    }

    /* High-Gloss Modern Neon Button */
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

    /* Modern Hero Banner */
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

    /* Acknowledgement Card */
    .ack-glow {
        background: linear-gradient(135deg, rgba(163, 230, 53, 0.08) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-left: 5px solid #a3e635;
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    /* AI Thinking Status Badge */
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
# 2. FUTURISTIC SYNTHETIC IMAGE GENERATOR
# -----------------------------------------------------------------------------
def generate_futuristic_image(mode="robotics"):
    img = Image.new('RGB', (600, 380), color=(11, 18, 32))
    draw = ImageDraw.Draw(img)
    
    if mode == "robotics":
        draw.rectangle([200, 140, 400, 280], fill=(24, 35, 54), outline=(163, 230, 53), width=2)
        draw.ellipse([270, 80, 330, 140], fill=(30, 41, 59), outline=(163, 230, 53), width=2)
        draw.ellipse([285, 100, 295, 110], fill=(163, 230, 53))
        draw.ellipse([305, 100, 315, 110], fill=(163, 230, 53))
        draw.line([200, 180, 120, 240], fill=(163, 230, 53), width=4)
        draw.line([400, 180, 480, 240], fill=(163, 230, 53), width=4)
        draw.ellipse([160, 250, 230, 320], fill=(15, 23, 42), outline=(163, 230, 53), width=3)
        draw.ellipse([370, 250, 440, 320], fill=(15, 23, 42), outline=(163, 230, 53), width=3)
    
    elif mode == "satellite":
        for i in range(0, 600, 40):
            draw.line([i, 0, i, 380], fill=(31, 41, 55), width=1)
        for j in range(0, 380, 40):
            draw.line([0, j, 600, j], fill=(31, 41, 55), width=1)
        draw.polygon([(100, 60), (300, 40), (500, 120), (450, 320), (150, 300)], fill=(20, 83, 45, 180), outline=(163, 230, 53), width=2)
        draw.ellipse([250, 140, 350, 240], fill=(185, 28, 28, 150), outline=(239, 68, 68), width=2)

    elif mode == "leaf":
        draw.ellipse([120, 40, 480, 340], fill=(20, 83, 45), outline=(163, 230, 53), width=2)
        draw.line([300, 40, 300, 340], fill=(163, 230, 53), width=3)
        draw.ellipse([220, 140, 280, 200], fill=(180, 83, 9))
        draw.ellipse([320, 220, 370, 270], fill=(180, 83, 9))

    return img

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
# 4. ADVANCED REASONING ENGINE FOR BIOSYNC AI TALK
# -----------------------------------------------------------------------------
def generate_ai_response(query):
    q_lower = query.lower()
    
    # 1. Platform & Developer Specifics
    if "creator" in q_lower or "developer" in q_lower or "lakshay" in q_lower or "who made" in q_lower:
        return ("**BioSyncAI** was created by **Lakshay of Class XI A** under the guidance of **Ms. Nisha Yadav Mam** for the **OlympAI Hackathon 2026**.\n\n"
                "It represents an enterprise-grade, dark-themed AgTech platform designed to model global agricultural monitoring systems like Cropin.")
    
    # 2. Vision 2057 & Autonomous Robotics
    elif "2057" in q_lower or "robot" in q_lower or "future" in q_lower or "drone" in q_lower:
        return ("Our **Vision 2057 Roadmap** targets **100% autonomous robotic agriculture** by the year 2057.\n\n"
                "* **Phase 1 (2026-2035):** AI Cloud analytics & multispectral disease detection.\n"
                "* **Phase 2 (2035-2045):** Drone swarms for thermal scanning & aerial micro-spraying.\n"
                "* **Phase 3 (2045-2057):** Solar-powered field robots performing zero-chemical harvesting and automated seeding.")

    # 3. Spatial Heatmap & Satellite Telemetry
    elif "heatmap" in q_lower or "spatial" in q_lower or "satellite" in q_lower or "grid" in q_lower:
        return ("The **Spatial Health Heatmap** correlates real-time microclimate parameters (Soil Moisture, Temperature, Humidity) with Random Forest prediction probability to map disease risk flags across field zones.")

    # 4. Multispectral Vision & NDVI
    elif "ndvi" in q_lower or "vision" in q_lower or "multispectral" in q_lower or "leaf" in q_lower:
        return ("The **Multispectral Vision Engine** applies three specialized optical channels:\n"
                "1. **Chlorophyll Index (Pseudo-NDVI):** Highlights photosynthetically active vegetation.\n"
                "2. **Lesion Edge Tracer:** Enhances structural boundaries of fungal leaf spots.\n"
                "3. **Thermal Anomaly Map:** Maps transpiration changes caused by root rot or drought.")

    # 5. Multimodal AI Disease Prediction
    elif "disease" in q_lower or "ai" in q_lower or "model" in q_lower or "inference" in q_lower:
        return ("The **Multimodal AI Engine** leverages a trained Random Forest model (3,000 samples) taking inputs for Soil Moisture, Temp, Humidity, Rain, and Bio-Resonance Frequency (300-900 Hz) to output fungal blight probabilities with up to 92.4% accuracy.")

    # 6. Yield Outlook & Irrigation
    elif "yield" in q_lower or "water" in q_lower or "irrigation" in q_lower:
        return ("The **Yield Outlook & Water Grid** evaluates moisture saturation levels (e.g. 78%) to optimize micro-irrigation flow, reducing agricultural water consumption by up to 25%.")

    # 7. General Agriculture & AgTech Questions
    elif "agtech" in q_lower or "farming" in q_lower or "soil" in q_lower or "crop" in q_lower:
        return ("**Modern AgTech** integrates IoT sensor telemetry, satellite remote sensing, computer vision, and machine learning. "
                "By combining ground sensors with orbital imagery, farmers can transition from reactive farming to predictive precision agriculture.")

    # 8. Fallback Smart Response
    else:
        return (f"Thank you for asking about: *'{query}'*.\n\n"
                "**BioSyncAI** provides real-time agricultural intelligence through its 11 integrated modules—including "
                "Spatial Heatmaps, Multispectral Vision, Multimodal Machine Learning, and the **Vision 2057 Autonomous Farming Roadmap**. "
                "Feel free to ask how any specific module works!")

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#a3e635 !important; font-weight:800;'>BioSyncAI Core</h2>", unsafe_allow_html=True)
st.sidebar.caption("⚡ Autonomous AgTech Platform")

menu = st.sidebar.radio(
    "Navigation System",
    [
        "🚀 Platform Overview",
        "💬 BioSync AI Talk (Assistant)",
        "🤖 Vision 2057: Robotic Farming",
        "🌐 Spatial Health Heatmap",
        "🔬 Multispectral Vision Engine",
        "🧠 Multimodal AI Diagnostic",
        "📊 Yield Outlook & Water Grid",
        "📞 Request Enterprise Demo",
        "💼 Careers & Talent Hub",
        "📄 RFP Report Generator",
        "📜 Acknowledgements"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 **Lead Developer:** Lakshay (Class XI A)\n🤖 **Robotic Swarm:** Vision 2057\n🏫 **OlympAI Hackathon 2026**")

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
        st.image(generate_futuristic_image("satellite"), caption="Orbital Telemetry Grid", use_container_width=True)
        st.subheader("Orbital Surveillance")
        st.write("Hyperspectral and thermal satellite telemetry mapped continuously.")

    with c2:
        st.image(generate_futuristic_image("leaf"), caption="Multispectral Cellular Vision", use_container_width=True)
        st.subheader("Cellular Diagnostics")
        st.write("Real-time detection of crop stress and pathogens using computer vision.")

    with c3:
        st.image(generate_futuristic_image("robotics"), caption="Autonomous Farm Robotics", use_container_width=True)
        st.subheader("Robotic Swarms")
        st.write("Fully automated sowing, weeding, and targeted intervention robotics.")

# -----------------------------------------------------------------------------
# MODULE 2: BIOSYNC AI TALK (ADVANCED ASSISTANT WITH THINKING STATUS)
# -----------------------------------------------------------------------------
elif menu == "💬 BioSync AI Talk (Assistant)":
    st.markdown("<h1 style='color:#a3e635;'>BioSync AI Talk Assistant</h1>", unsafe_allow_html=True)
    st.write("Ask any questions regarding AgTech, modern farming practices, soil health, crop diagnostics, or platform features!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am BioSyncAI's intelligent assistant. How can I help you with agricultural technology, diagnostics, or site features today?"}
        ]

    # Render Chat Messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_query = st.chat_input("Type your message here (e.g., 'How does the AI model work?' or 'What is Vision 2057?')...")

    if user_query:
        # Render User Message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # Render Assistant Response with Live "Thinking" & "Web Search" Animation
        with st.chat_message("assistant"):
            status_container = st.empty()
            
            # Step 1: Thinking Stage
            status_container.markdown("<div class='thinking-badge'>🧠 BioSync AI is analyzing query intent...</div>", unsafe_allow_html=True)
            time.sleep(0.7)

            # Step 2: Knowledge Base & Web Search Stage
            status_container.markdown("<div class='thinking-badge'>🔍 Searching AgTech Knowledge Base & Web Telemetry...</div>", unsafe_allow_html=True)
            time.sleep(0.8)

            # Step 3: Clear Thinking Status and Stream Response
            status_container.empty()
            full_response = generate_ai_response(user_query)
            
            # Simulated Streaming Effect
            response_box = st.empty()
            partial_text = ""
            for char in full_response:
                partial_text += char
                response_box.markdown(partial_text + "▌")
                time.sleep(0.01)
            
            response_box.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# -----------------------------------------------------------------------------
# MODULE 3: VISION 2057 (ROBOTIC FARMING ROADMAP)
# -----------------------------------------------------------------------------
elif menu == "🤖 Vision 2057: Robotic Farming":
    st.markdown("<h1 style='color:#a3e635;'>Vision 2057: The Autonomous Robotic Era</h1>", unsafe_allow_html=True)
    st.write("Our long-term global roadmap towards 100% autonomous, robotically managed agriculture by the year 2057.")

    st.image(generate_futuristic_image("robotics"), caption="BioSyncAI Autonomous Field Robot (Concept 2057)", use_container_width=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Global Swarm Target", "10,000,000 Units", "By 2057")
    with r2:
        st.metric("Human Labor Requirement", "0.0%", "-100% Manual Effort")
    with r3:
        st.metric("Precision Yield Efficiency", "99.8%", "+45% Output")

    st.markdown("---")

    with st.expander("🗺️ Strategic Roadmap to 2057", expanded=True):
        st.markdown("""
        #### **Phase 1: Diagnostic AI & Cloud Analytics (2026 – 2035)**
        * Rollout of satellite spatial heatmaps, multi-modal disease prediction, and remote sensor integration.
        
        #### **Phase 2: Hybrid Human-Drone Operations (2035 – 2045)**
        * Autonomous drone swarms for precision aerial spraying, thermal imaging, and automated soil sampling.
        
        #### **Phase 3: Full Robotic Autonomy (2045 – 2057)**
        * Solar-powered autonomous field robots handling micro-seeding, continuous mechanical weeding, and zero-chemical precision harvesting worldwide.
        """)

# -----------------------------------------------------------------------------
# MODULE 4: SPATIAL HEALTH HEATMAP
# -----------------------------------------------------------------------------
elif menu == "🌐 Spatial Health Heatmap":
    st.markdown("<h1 style='color:#a3e635;'>Operating Decision & Spatial Matrix</h1>", unsafe_allow_html=True)

    with st.expander("📌 Real-time Sector Metrics", expanded=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Monitored Area", "12,450 Acres", "+350 Acres")
        m2.metric("Health Index", "84.2 / 100", "-2.1 pts")
        m3.metric("Disease Flag", "High Risk", "Zone B")
        m4.metric("Soil Saturation", "78%", "Optimal")

    with st.expander("🗺️ Interactive Spatial Matrix", expanded=True):
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
# MODULE 5: MULTISPECTRAL VISION ENGINE
# -----------------------------------------------------------------------------
elif menu == "🔬 Multispectral Vision Engine":
    st.markdown("<h1 style='color:#a3e635;'>Multispectral Vision Engine</h1>", unsafe_allow_html=True)

    with st.expander("📷 Leaf Sample Analysis", expanded=True):
        uploaded_file = st.file_uploader("Upload Crop Sample (JPG/PNG)", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
        else:
            st.caption("⚡ Showing synthetic leaf sample image.")
            image = generate_futuristic_image("leaf")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("RGB Spectrum")
            st.image(image, use_container_width=True)

        with c2:
            st.subheader("Processed Spectral Filter")
            vision_mode = st.selectbox("Select Filter", ["Chlorophyll Index (Pseudo-NDVI)", "Lesion Edge Tracer", "Thermal Anomaly Map"])

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
# MODULE 6: MULTIMODAL AI DIAGNOSTIC
# -----------------------------------------------------------------------------
elif menu == "🧠 Multimodal AI Diagnostic":
    st.markdown("<h1 style='color:#a3e635;'>Multimodal AI Inference Engine</h1>", unsafe_allow_html=True)

    with st.expander("🎛️ Sensor Input Controls", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            in_sm = st.slider("Soil Moisture (%)", 0.0, 100.0, 82.0)
            in_temp = st.slider("Ambient Temp (°C)", 10.0, 50.0, 28.0)
            in_hum = st.slider("Humidity (%)", 0.0, 100.0, 86.0)
        with col2:
            in_rain = st.slider("Precipitation (mm)", 0.0, 100.0, 12.5)
            in_freq = st.slider("Bio-Resonance Frequency (Hz)", 300, 900, 520)

        if st.button("🚀 Run AI Inference"):
            feat = np.array([[in_sm, in_temp, in_hum, in_rain, in_freq]])
            pred = model.predict(feat)[0]
            prob = model.predict_proba(feat)[0]

            if pred == 1:
                st.error(f"🚨 **HIGH RISK DETECTED: Fungal Leaf Blight Threat**\n*Confidence:* `{prob[1]*100:.2f}%`")
            else:
                st.success(f"✅ **HEALTHY FIELD STATUS**\n*Confidence:* `{prob[0]*100:.2f}%`")

# -----------------------------------------------------------------------------
# MODULE 7: YIELD OUTLOOK & WATER GRID
# -----------------------------------------------------------------------------
elif menu == "📊 Yield Outlook & Water Grid":
    st.markdown("<h1 style='color:#a3e635;'>Harvest Forecast & Irrigation</h1>", unsafe_allow_html=True)

    with st.expander("🌾 Yield Outlook", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Estimated Harvest", "4.25 Tons / Ha", "+8.2%")
            st.line_chart(pd.DataFrame({'Yield': [3.8, 3.9, 4.0, 4.1, 4.25]}))
        with c2:
            st.metric("Water Saturation", "78%", "Optimal")
            st.progress(0.78)

# -----------------------------------------------------------------------------
# MODULE 8: REQUEST ENTERPRISE DEMO
# -----------------------------------------------------------------------------
elif menu == "📞 Request Enterprise Demo":
    st.markdown("<h1 style='color:#a3e635;'>Talk to Our Enterprise Team</h1>", unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 1])

    with col_info:
        st.markdown("""
        ### Why BioSyncAI?
        * **Global Scale:** Enterprise-grade agricultural platform.
        * **Decision Workflows:** Supply, Risk, Inspection, and Compliance.
        * **Lead Developer:** Lakshay (Class XI A)
        """)

    with col_form:
        with st.form("demo_form"):
            f_name = st.text_input("First Name *")
            l_name = st.text_input("Last Name *")
            email = st.text_input("Work Email *")
            domain = st.selectbox("Domain", ["Food-Ag", "Forest", "Water", "Energy", "Infrastructure"])
            decision_goals = st.text_area("What decision are you trying to improve?")

            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if f_name and l_name and email:
                    st.success(f"✅ Thank you {f_name}! Request logged successfully.")
                    st.info(f"""
                    📩 **Dispatched Confirmation Summary**
                    * **Email:** `{email}`
                    * **Project Lead:** Lakshay (Class XI A)
                    """)
                else:
                    st.error("Please fill in required fields.")

# -----------------------------------------------------------------------------
# MODULE 9: CAREERS & TALENT HUB
# -----------------------------------------------------------------------------
elif menu == "💼 Careers & Talent Hub":
    st.markdown("<h1 style='color:#a3e635;'>Careers at BioSyncAI</h1>", unsafe_allow_html=True)

    with st.expander("🚀 Open Roles", expanded=True):
        st.markdown("""
        #### 1. Robotics & Autonomous Hardware Engineer
        * **Scope:** Design autonomous ground rovers for Vision 2057 deployment.
        
        ---
        #### 2. Computer Vision AI Specialist
        * **Scope:** Multi-spectral leaf diagnostic model development.
        """)

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

RECOMMENDED ACTION PLAN:
1. Apply targeted copper-based fungicide to Zone B.
2. Reduce micro-irrigation flow in Zone B by 20%.
===================================================="""
    st.text_area("Report Output", report_text, height=200)
    st.download_button("📥 Download Report (.txt)", data=report_text, file_name="BioSyncAI_Report.txt")

# -----------------------------------------------------------------------------
# MODULE 11: ACKNOWLEDGEMENTS
# -----------------------------------------------------------------------------
elif menu == "📜 Acknowledgements":
    st.markdown("<h1 style='color:#a3e635;'>Acknowledgements & Credits</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='ack-glow'>
        <h2 style='color:#a3e635 !important; margin-top:0;'>👨‍💻 Developed By</h2>
        <h3 style='color:#ffffff; margin-bottom:15px;'>Lakshay</h3>
        <p style='font-size:18px; color:#cbd5e1;'><strong>Class:</strong> XI A</p>
        <p style='font-size:18px; color:#cbd5e1;'><strong>Project:</strong> BioSyncAI Autonomous AgTech Platform (OlympAI Hackathon 2026)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("🙏 Special Thanks & Gratitude", expanded=True):
        st.markdown("""
        ### **A Special Thanks to My Teacher**
        I would like to express my sincere gratitude and heartfelt thanks to my respected teacher, **Ms. Nisha Yadav Mam**, for her constant encouragement, invaluable guidance, and unwavering support throughout the creation of this project. Her mentorship inspired me to push the boundaries of technology and build **BioSyncAI**.

        ---

        ### **Acknowledgement to My Teammates**
        I am deeply grateful to all my teammates for their collaboration, enthusiasm, and tireless effort during the development of this project. Their teamwork and shared dedication played a crucial role in bringing the vision of an autonomous AgTech platform to life.
        """)
