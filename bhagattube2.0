import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import io

# Page Setup
st.set_page_config(
    page_title="CreatorStudio Pro - Ultimate Media Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light Theme CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F5F7;
        color: #0E1318;
    }
    .main-header {
        font-size: 38px;
        font-weight: 800;
        color: #1E1B4B;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-text {
        font-size: 16px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("⚡ CreatorStudio Pro")
    st.caption("The Ultimate Content Suite")
    st.write("---")
    
    app_mode = st.radio(
        "Select Studio Tool:",
        ["🖼️ Thumbnail Studio", "✍️ AI Script Generator", "📈 SEO Optimizer", "📅 Content Planner"]
    )
    
    st.write("---")
    st.info("💡 **Tip**: Create high-contrast text overlays to boost your click-through rates!")

# ==================== TOOL 1: THUMBNAIL STUDIO ====================
if app_mode == "🖼️ Thumbnail Studio":
    st.markdown("<div class='main-header'>YouTube & Social Media Thumbnail Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Design, edit, and optimize click-worthy thumbnails instantly.</div>", unsafe_allow_html=True)
    
    col_ctrl, col_prev = st.columns([1, 1.5], gap="large")
    
    with col_ctrl:
        st.subheader("🛠️ Design Controls")
        
        bg_choice = st.selectbox("Background Type", ["Solid Color", "Preset Gradient", "Upload Image"], key="bg_type_select")
        
        if bg_choice == "Solid Color":
            bg_color = st.color_picker("Pick Background Color", "#FF6B35", key="solid_bg_picker")
            canvas = Image.new("RGB", (1280, 720), color=bg_color)
        elif bg_choice == "Preset Gradient":
            theme_grad = st.selectbox("Theme Preset", ["Cyberpunk Neon", "Sunset Orange", "Deep Ocean"], key="preset_select")
            base_col = "#7D2AE8" if theme_grad == "Cyberpunk Neon" else ("#FF4500" if theme_grad == "Sunset Orange" else "#00C4CC")
            canvas = Image.new("RGB", (1280, 720), color=base_col)
        else:
            uploaded_file = st.file_uploader("Upload background image", type=["jpg", "png", "jpeg"], key="thumb_uploader")
            if uploaded_file:
                canvas = Image.open(uploaded_file).convert("RGB").resize((1280, 720))
            else:
                canvas = Image.new("RGB", (1280, 720), color="#1E1B4B")
                
        st.write("---")
        caption_text = st.text_input("Main Heading Text", "HOW TO BUILD A STARTUP", key="thumb_text")
        text_color = st.color_picker("Text Color", "#FFFFFF", key="text_color_picker")
        pos_x = st.slider("Horizontal Position (X)", 50, 1000, 100, key="pos_x_slider")
        pos_y = st.slider("Vertical Position (Y)", 50, 600, 250, key="pos_y_slider")
        
        st.write("---")
        filter_type = st.selectbox("Filter Effect", ["None", "Grayscale", "Blur", "High Contrast"], key="filter_select")
        brightness = st.slider("Brightness Adjustment", 0.5, 2.0, 1.0, key="bright_slider")

    with col_prev:
        st.subheader("🖼️ Live Preview (1280x720)")
        
        working_image = canvas.copy()
        
        if filter_type == "Grayscale":
            working_image = working_image.convert("L").convert("RGB")
        elif filter_type == "Blur":
            working_image = working_image.filter(ImageFilter.BLUR)
        elif filter_type == "High Contrast":
            working_image = ImageEnhance.Contrast(working_image).enhance(1.8)
            
        working_image = ImageEnhance.Brightness(working_image).enhance(brightness)
        
        draw = ImageDraw.Draw(working_image)
        draw.text((pos_x, pos_y), caption_text, fill=text_color)
        
        st.image(working_image, use_container_width=True)
        
        buffer = io.BytesIO()
        working_image.save(buffer, format="PNG")
        st.download_button(
            label="📥 Download High-Res Thumbnail (.png)",
            data=buffer.getvalue(),
            file_name="creator_thumbnail.png",
            mime="image/png",
            use_container_width=True
        )

# ==================== TOOL 2: AI SCRIPT GENERATOR ====================
elif app_mode == "✍️ AI Script Generator":
    st.markdown("<div class='main-header'>AI Video Script Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Generate professional hooks, outlines, and video scripts in seconds.</div>", unsafe_allow_html=True)
    
    with st.form("script_form"):
        topic = st.text_input("Video Topic / Title", placeholder="e.g., 5 Coding Tips for Beginners")
        tone = st.selectbox("Tone of Voice", ["High Energy & Engaging", "Professional & Educational", "Casual & Humorous", "Dramatic"])
        duration = st.selectbox("Target Length", ["Shorts / Reels (60 seconds)", "Standard Video (8-10 minutes)", "Deep Dive (20+ minutes)"])
        
        submitted = st.form_submit_button("🚀 Generate Full Script Structure")
        
        if submitted and topic:
            st.success("Script generated successfully!")
            st.subheader("🎬 Generated Video Blueprint")
            
            st.markdown(f"**📌 Topic:** {topic}")
            st.markdown(f"**🎨 Tone:** {tone} | **⏱️ Length:** {duration}")
            st.write("---")
            
            st.markdown("### 1. The Hook (0 - 15 seconds)")
            st.write(f"> *'Stop scrolling if you want to master {topic} without wasting months of your time.'*")
            
            st.markdown("### 2. Introduction & Overview")
            st.write(f"> *'Welcome back to the channel. Today we are breaking down {topic} step-by-step.'*")
            
            st.markdown("### 3. Core Content Body")
            st.write("> - **Point 1:** Foundation and setup mistakes to avoid.")
            st.write("> - **Point 2:** The secret shortcut nobody talks about.")
            
            st.markdown("### 4. Call to Action (Outro)")
            st.write("> *'If this helped you, hit subscribe and drop a comment below!'*")

# ==================== TOOL 3: SEO OPTIMIZER ====================
elif app_mode == "📈 SEO Optimizer":
    st.markdown("<div class='main-header'>YouTube SEO & Tag Optimizer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Generate viral tags, search-optimized descriptions, and catchy titles.</div>", unsafe_allow_html=True)
    
    keyword = st.text_input("Enter Main Keyword / Niche", value="Python programming tutorials")
    
    if st.button("🔍 Analyze & Generate Tags"):
        st.success("SEO analysis complete!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='metric-card'><h3>92 / 100</h3><p>SEO Score</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-card'><h3>High</h3><p>Search Volume</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='metric-card'><h3>Low</h3><p>Competition</p></div>", unsafe_allow_html=True)
            
        st.write("---")
        st.subheader("🏷️ Recommended Viral Tags")
        tags = [f"{keyword}", f"learn {keyword}", f"best {keyword}", f"{keyword} for beginners", "creator tips", "masterclass"]
        st.code(", ".join(tags), language="text")

# ==================== TOOL 4: CONTENT PLANNER ====================
elif app_mode == "📅 Content Planner":
    st.markdown("<div class='main-header'>Content Scheduling & Planner</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Organize your publishing calendar and track content status.</div>", unsafe_allow_html=True)
    
    with st.form("planner_form"):
        p_title = st.text_input("Content Title")
        p_platform = st.selectbox("Platform", ["YouTube", "Instagram Reels", "TikTok", "Newsletter"])
        p_date = st.date_input("Scheduled Publish Date")
        p_status = st.selectbox("Status", ["Idea 💡", "In Production 🎬", "Ready to Publish 🚀"])
        
        if st.form_submit_button("Add to Schedule"):
            st.success(f"Added '{p_title}' for {p_platform} on {p_date} ({p_status})!")
            
    st.write("---")
    st.subheader("📋 Publishing Queue")
    st.write("• **10 Python Scripts** — YouTube (In Production 🎬)")
    st.write("• **AI Design Tools** — Instagram (Idea 💡)")
