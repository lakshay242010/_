import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import io

# 1. Page Configuration
st.set_page_config(
    page_title="BhagaTube - Canva Master Studio",
    page_icon="🎨",
    layout="wide"
)

# 2. Session State Setup
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_business_modal" not in st.session_state:
    st.session_state.show_business_modal = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "BhagaTube Creator"

# 3. Aggressive Light Mode CSS (Forces white backgrounds on buttons and inputs to fix dark mode bugs)
st.markdown("""
    <style>
    /* Force main background */
    .stApp {
        background-color: #F4F5F7 !important;
        color: #0E1318 !important;
    }
    
    .block-container {
        background-color: #F4F5F7 !important;
        padding: 2rem !important;
    }

    /* Force Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }

    /* Force all text elements to dark */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #0E1318 !important;
    }

    /* FORCE ALL STREAMLIT BUTTONS TO BE CLEAN WHITE WITH DARK TEXT (Fixes black button blocks) */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #0E1318 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    .stButton > button:hover {
        background-color: #F3F4F6 !important;
        border-color: #9CA3AF !important;
    }

    /* FORCE TEXT INPUTS & SELECTBOXES TO BE WHITE */
    input, stTextInput, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0E1318 !important;
    }

    /* Hero Title */
    .hero-title {
        font-size: 44px !important;
        font-weight: 800 !important;
        text-align: center !important;
        color: #1E1B4B !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }
    .hero-sub {
        font-size: 16px !important;
        text-align: center !important;
        color: #4B5563 !important;
        margin-bottom: 25px !important;
    }

    /* Canva Feature Cards */
    .card-yellow {
        background-color: #FFD43B !important;
        padding: 25px !important;
        border-radius: 20px !important;
        color: #0E1318 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-yellow h3, .card-yellow p {
        color: #0E1318 !important;
    }

    .card-orange {
        background-color: #FF6B35 !important;
        padding: 25px !important;
        border-radius: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-orange h3, .card-orange p {
        color: #FFFFFF !important;
    }

    .card-green {
        background-color: #D1E7DD !important;
        padding: 20px !important;
        border-radius: 16px !important;
        color: #0F5132 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-green h4, .card-green p {
        color: #0F5132 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== LEFT SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown("### 🎨 **BhagaTube**")
    st.write("---")
    if st.button("🏠 Home Dashboard", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📁 Projects & Folders", use_container_width=True):
        st.session_state.page = "projects"
        st.rerun()
    if st.button("🖼️ Browse Templates", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    if st.button("👑 Brand Kit & Hub", use_container_width=True):
        st.session_state.page = "brand_kit"
        st.rerun()
    if st.button("✨ BhagaTube AI Studio", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    if st.button("🛍️ Print & Merchandise", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
        
    st.write("---")
    if not st.session_state.logged_in:
        if st.button("🔑 Log In / Sign Up", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    else:
        st.success(f"👤 {st.session_state.username}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

# ==================== BUSINESS MODAL POPUP ====================
if st.session_state.show_business_modal:
    st.info("👑 **Try BhagaTube Business for Free (30-Day Trial)**")
    st.write("Unlock Brand Kits, Background Removers, Magic Resize, and 20x AI usage.")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.radio("Choose Tier:", ["Pro - $12.99/mo", "Business - $14.99/mo"])
    with col_p2:
        st.number_input("Team Seats:", min_value=1, value=5)
    
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🚀 Start Free Trial", use_container_width=True):
            st.success("Business Trial Activated!")
            st.session_state.show_business_modal = False
            st.rerun()
    with m2:
        if st.button("✕ Close", use_container_width=True):
            st.session_state.show_business_modal = False
            st.rerun()
    st.divider()

# ==================== HOME DASHBOARD ====================
if st.session_state.page == "home":
    
    # Top Search Bar
    top_c1, top_c2, top_c3 = st.columns([3, 1.2, 1])
    with top_c1:
        st.text_input("🔍 Search 100,000+ templates, presentations, logos...", label_visibility="collapsed")
    with top_c2:
        if st.button("👑 Try Business Free"):
            st.session_state.show_business_modal = True
    with top_c3:
        if not st.session_state.logged_in:
            if st.button("Sign In / Up"):
                st.session_state.page = "auth"
                st.rerun()

    # Main Header
    st.markdown("<div class='hero-title'>What will you design today?</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>All the tools to create like a pro</div>", unsafe_allow_html=True)
    
    # Category Pills Toolbar
    cat_cols = st.columns(13)
    categories = ["Templates", "Presentation", "Social media", "Video", "Printables", "Doc", "Whiteboard", "Sheet", "Website", "Magic Layers", "Custom size", "Upload", "More"]
    for idx, cat in enumerate(categories):
        with cat_cols[idx]:
            if st.button(cat, key=f"cat_{idx}", use_container_width=True):
                st.session_state.page = "editor"
                st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Feature Row 1
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        st.markdown("""
            <div class='card-yellow'>
                <h3>Swap distracting backgrounds & transform your photos</h3>
                <p>Instantly remove or replace image backgrounds with AI.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change background"):
            st.session_state.page = "editor"
            st.rerun()
            
    with r1_c2:
        st.markdown("""
            <div class='card-orange'>
                <h3>Capture the essence of your brand in a logo</h3>
                <p>Generate professional vectors and custom branding from prompts.</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("Logo design for...", placeholder="e.g. Coffee shop...")
        if st.button("Generate a logo"):
            st.session_state.page = "brand_kit"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Feature Row 2
    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        st.markdown("""
            <div class='card-orange'>
                <h3>Reimagine your image with a short written prompt</h3>
                <p>Type what you want to change, like 'Change bag to blue' with Magic Edit.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Try Magic Edit"):
            st.session_state.page = "editor"
            st.rerun()
            
    with r2_c2:
        st.markdown("""
            <div class='card-yellow'>
                <h3>Generate natural-sounding AI voices</h3>
                <p>Convert text straight into engaging audio voiceovers and avatars.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Generate voice"):
            st.session_state.page = "editor"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Magic Media Image Generator Section
    st.subheader("🪄 Try Image Generator")
    st.write("Turn pure text to art with Magic Media™ and our range of AI art generator tools.")
    
    img_gen_1, img_gen_2 = st.columns([2, 1])
    with img_gen_1:
        st.text_input("Prompt:", value="Moon rising over the mountains")
        st.selectbox("Style Preset:", ["Dreamy", "Anime", "Watercolor", "Filmic"])
        if st.button("Generate Art"):
            st.session_state.page = "editor"
            st.rerun()
    with img_gen_2:
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", caption="AI Preview")

    st.divider()

    # Business Features
    st.subheader("Our Business Features")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("<div class='card-green'><h4>Set up a Brand Kit</h4><p>Unify your designs and logo assets.</p></div>", unsafe_allow_html=True)
        if st.button("Learn more", key="bk1"):
            st.session_state.page = "brand_kit"
            st.rerun()
    with b2:
        st.markdown("<div class='card-green'><h4>Empower your team</h4><p>Scale content across your organization.</p></div>", unsafe_allow_html=True)
        if st.button("Learn more", key="bk2"):
            st.session_state.show_business_modal = True
            st.rerun()
    with b3:
        st.markdown("<div class='card-green'><h4>Real-time collaboration</h4><p>Create designs together seamlessly.</p></div>", unsafe_allow_html=True)
        if st.button("View plans", key="bk3"):
            st.session_state.show_business_modal = True
            st.rerun()

    st.divider()

    # Templates Showcase
    st.subheader("Templates for absolutely anything")
    t1, t2 = st.columns(2)
    with t1:
        if st.button("✨ Start designing for free", use_container_width=True):
            st.session_state.page = "editor"
            st.rerun()
    with t2:
        if st.button("📁 Browse all templates", use_container_width=True):
            st.session_state.page = "editor"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)
    g1, g2, g3, g4 = st.columns(4)
    with g1: st.image("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400", caption="Invitation")
    with g2: st.image("https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400", caption="Flyer")
    with g3: st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400", caption="Greeting")
    with g4: st.image("https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400", caption="Tournament")

# ==================== PROJECTS PAGE ====================
elif st.session_state.page == "projects":
    st.header("📁 Projects & Folders")
    st.write("Access your saved designs and team work folders.")
    if st.button("Open Editor Workspace"):
        st.session_state.page = "editor"
        st.rerun()

# ==================== BRAND KIT PAGE ====================
elif st.session_state.page == "brand_kit":
    st.header("👑 BhagaTube Brand Hub")
    st.selectbox("Heading Font", ["Sans-Serif", "Serif", "Monospace"])
    st.color_picker("Brand Primary Color", "#7D2AE8")
    st.file_uploader("Upload Brand Logos", type=["png", "svg"])

# ==================== EDITOR WORKSPACE ====================
elif st.session_state.page == "editor":
    st.header("🎨 Interactive Design Workspace")
    if st.button("← Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()
        
    st.divider()
    tool_col, canvas_col = st.columns([1, 2])
    
    with tool_col:
        st.subheader("🛠️ Toolkit")
        preset = st.selectbox("Format Size", ["YouTube Thumbnail (1280x720)", "Instagram Post (1080x1080)"])
        bg_color = st.color_picker("Background Color", "#7D2AE8")
        
        base = Image.new("RGB", (1280, 720) if "Thumbnail" in preset else (1080, 1080), color=bg_color)
        
        st.markdown("---")
        heading_text = st.text_input("Heading Text", "Create Like A Pro")
        text_color = st.color_picker("Text Color", "#FFFFFF")
        pos_x = st.slider("Position X", 0, base.width - 100, 100)
        pos_y = st.slider("Position Y", 0, base.height - 100, 100)
        
        st.markdown("---")
        filter_opt = st.selectbox("Filter", ["None", "Grayscale", "Blur", "Contour"])
        brightness_val = st.slider("Brightness", 0.5, 2.0, 1.0)

    with canvas_col:
        st.subheader("🖼️ Live Preview")
        working_img = base.copy()
        
        if filter_opt == "Grayscale": working_img = working_img.convert("L").convert("RGB")
        elif filter_opt == "Blur": working_img = working_img.filter(ImageFilter.BLUR)
        elif filter_opt == "Contour": working_img = working_img.filter(ImageFilter.CONTOUR)

        working_img = ImageEnhance.Brightness(working_img).enhance(brightness_val)
        
        draw = ImageDraw.Draw(working_img)
        draw.text((pos_x, pos_y), heading_text, fill=text_color)
        
        st.image(working_img, use_container_width=True)
        
        buffer = io.BytesIO()
        working_img.save(buffer, format="PNG")
        st.download_button("📥 Download Export (.png)", data=buffer.getvalue(), file_name="export.png", mime="image/png", use_container_width=True)

# ==================== AUTHENTICATION ====================
elif st.session_state.page == "auth":
    st.header("🔑 BhagaTube Account Access")
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Sign In"):
            st.session_state.logged_in = True
            st.session_state.username = u if u else "Creator"
            st.session_state.page = "home"
            st.rerun()
