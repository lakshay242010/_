import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import io

# Page Configuration
st.set_page_config(
    page_title="BhagaTube - Design Anything",
    page_icon="🎨",
    layout="wide"
)

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "All"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_business_modal" not in st.session_state:
    st.session_state.show_business_modal = False

# Canva-Style Custom CSS Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F5F7;
        color: #0e1318;
    }
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #0e1318;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .category-pill {
        display: inline-block;
        padding: 8px 20px;
        margin: 5px;
        border-radius: 20px;
        background: #FFFFFF;
        color: #333;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
    }
    .feature-card-yellow {
        background: #FFD43B;
        padding: 25px;
        border-radius: 16px;
        color: #0e1318;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .feature-card-orange {
        background: #FF6B35;
        padding: 25px;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🎨 **BhagaTube**")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📁 Projects", use_container_width=True):
        st.session_state.page = "projects"
        st.rerun()
    if st.button("🖼️ Templates", use_container_width=True):
        st.session_state.page = "templates"
        st.rerun()
    if st.button("👑 Brand & Business", use_container_width=True):
        st.session_state.show_business_modal = True
    if st.button("✨ BhagaTube AI Studio", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    st.divider()
    if not st.session_state.logged_in:
        if st.button("🔑 Log In / Sign Up", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    else:
        st.success(f"User: {st.session_state.username}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# --- BUSINESS MODAL POPUP ---
if st.session_state.show_business_modal:
    st.info("👑 **Try BhagaTube Business for Free (30-Day Trial)**")
    st.write("Unlock Brand Kits, Background Removers, 20x AI Usage, and Team Collaboration.")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("Start Free Trial"):
            st.success("Business Plan activated for 30 days!")
            st.session_state.show_business_modal = False
            st.rerun()
    with col_m2:
        if st.button("Close"):
            st.session_state.show_business_modal = False
            st.rerun()
    st.divider()

# ==================== PAGE 1: HOME DASHBOARD ====================
if st.session_state.page == "home":
    
    col_tb1, col_tb2, col_tb3 = st.columns([3, 1, 1])
    with col_tb1:
        search_query = st.text_input("🔍 Search anything (e.g., YouTube thumbnail, logo, presentation)", label_visibility="collapsed")
    with col_tb2:
        if st.button("👑 Try Business Free"):
            st.session_state.show_business_modal = True
    with col_tb3:
        if not st.session_state.logged_in:
            if st.button("Sign In / Up"):
                st.session_state.page = "auth"
                st.rerun()

    # Main Hero Header (Fixed syntax error here)
    st.markdown("<div class='hero-title'>All the tools to create like a pro</div>", unsafe_allow_html=True)
    
    # Category Pills Filter Bar
    cols = st.columns(7)
    categories = ["AI", "Social Media", "Video", "Presentation", "Print", "Try it now", "Education"]
    for i, cat in enumerate(categories):
        with cols[i]:
            if st.button(cat, use_container_width=True):
                st.session_state.selected_tool = cat

    st.write("<br>", unsafe_allow_html=True)

    # Interactive Tool Cards Grid
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
            <div class='feature-card-yellow'>
                <h3>Swap distracting backgrounds & transform your photos</h3>
                <p>Instantly remove or replace image backgrounds with AI.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change background"):
            st.session_state.page = "editor"
            st.rerun()
            
    with c2:
        st.markdown("""
            <div class='feature-card-orange'>
                <h3>Capture the essence of your brand in a logo</h3>
                <p>Generate professional logos from a simple text prompt.</p>
            </div>
        """, unsafe_allow_html=True)
        logo_prompt = st.text_input("Logo design for...", placeholder="e.g. Coffee shop, Gaming clan...")
        if st.button("✨ Create Logo"):
            st.session_state.page = "editor"
            st.rerun()

    st.write("---")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
            <div class='feature-card-orange'>
                <h3>Reimagine your image with a short written prompt</h3>
                <p>Type what you want to change, like 'Change bag to blue'.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Try Magic Edit"):
            st.session_state.page = "editor"
            st.rerun()
            
    with c4:
        st.markdown("""
            <div class='feature-card-yellow'>
                <h3>Generate natural-sounding AI voices & art</h3>
                <p>Convert text to voiceovers or gorgeous digital artwork instantly.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Generate voice or art"):
            st.session_state.page = "editor"
            st.rerun()

    st.write("---")
    st.markdown("### Templates for absolutely anything")
    
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400", caption="Presentation Template")
        if st.button("Use Template 1"):
            st.session_state.page = "editor"
            st.rerun()
    with t2:
        st.image("https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400", caption="Social Media Post")
        if st.button("Use Template 2"):
            st.session_state.page = "editor"
            st.rerun()
    with t3:
        st.image("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400", caption="Poster Design")
        if st.button("Use Template 3"):
            st.session_state.page = "editor"
            st.rerun()
    with t4:
        st.image("https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400", caption="YouTube Thumbnail")
        if st.button("Use Template 4"):
            st.session_state.page = "editor"
            st.rerun()

# ==================== PAGE 2: AUTHENTICATION ====================
elif st.session_state.page == "auth":
    st.header("🔑 Welcome to BhagaTube")
    tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
    
    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Log In"):
                st.session_state.logged_in = True
                st.session_state.username = user if user else "Creator"
                st.success("Logged in successfully!")
                st.session_state.page = "home"
                st.rerun()
                
    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            new_user = st.text_input("Choose Username")
            new_pwd = st.text_input("Create Password", type="password")
            if st.form_submit_button("Create Account"):
                st.session_state.logged_in = True
                st.session_state.username = new_user if new_user else name
                st.success("Account created!")
                st.session_state.page = "editor"
                st.rerun()

# ==================== PAGE 3: FULL WORKING DESIGN EDITOR ====================
elif st.session_state.page == "editor":
    st.header(f"🎨 BhagaTube Studio Workspace")
    
    col_tools, col_canvas = st.columns([1, 2])
    
    with col_tools:
        st.subheader("Design Toolkit")
        template_type = st.selectbox("Format", ["YouTube Thumbnail (1280x720)", "Instagram Post (1080x1080)", "Presentation (1920x1080)"])
        bg_color = st.color_picker("Background Fill", "#FF6B35")
        
        if "Thumbnail" in template_type:
            canvas_img = Image.new("RGB", (1280, 720), color=bg_color)
        elif "Instagram" in template_type:
            canvas_img = Image.new("RGB", (1080, 1080), color=bg_color)
        else:
            canvas_img = Image.new("RGB", (1920, 1080), color=bg_color)
            
        st.divider()
        st.write("🔤 **Text Layers**")
        user_text = st.text_input("Heading Text", "Create Like A Pro")
        text_color = st.color_picker("Text Color", "#FFFFFF")
        pos_x = st.slider("Position X", 0, canvas_img.width - 100, 100)
        pos_y = st.slider("Position Y", 0, canvas_img.height - 100, 100)
        
        st.divider()
        st.write("✨ **AI Enhancements**")
        filter_choice = st.selectbox("Apply Filter Effect", ["None", "Grayscale", "Blur", "Contour"])
        brightness = st.slider("Brightness Boost", 0.5, 2.0, 1.0)

    with col_canvas:
        st.subheader("Live Interactive Canvas Preview")
        
        processed = canvas_img.copy()
        if filter_choice == "Grayscale":
            processed = processed.convert("L").convert("RGB")
        elif filter_choice == "Blur":
            processed = processed.filter(ImageFilter.BLUR)
        elif filter_choice == "Contour":
            processed = processed.filter(ImageFilter.CONTOUR)
            
        processed = ImageEnhance.Brightness(processed).enhance(brightness)
        
        draw = ImageDraw.Draw(processed)
        draw.text((pos_x, pos_y), user_text, fill=text_color)
        
        st.image(processed, use_container_width=True)
        
        buf = io.BytesIO()
        processed.save(buf, format="PNG")
        st.download_button(
            label="📥 Download Final Design (.png)",
            data=buf.getvalue(),
            file_name="bhagatube_design.png",
            mime="image/png",
            use_container_width=True
        )
