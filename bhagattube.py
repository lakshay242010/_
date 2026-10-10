import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import io

# Page Configuration
st.set_page_config(
    page_title="BhagaTube - Canva Master Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "saved_users" not in st.session_state:
    st.session_state.saved_users = {"admin": "password123"}
if "presentation_slides" not in st.session_state:
    st.session_state.presentation_slides = [
        {"title": "Slide 1: Welcome", "bg": "#7D2AE8", "text": "Welcome to BhagaTube Presentation"},
        {"title": "Slide 2: Features", "bg": "#00C4CC", "text": "AI Powered Design Tools"}
    ]
if "current_slide_idx" not in st.session_state:
    st.session_state.current_slide_idx = 0

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🎨 **BhagaTube**")
    st.write("---")
    if st.button("🏠 Home Dashboard", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📊 Presentation Maker", use_container_width=True):
        st.session_state.page = "presentation_maker"
        st.rerun()
    if st.button("🖼️ Design Workspace", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    if st.button("👑 Brand Kit", use_container_width=True):
        st.session_state.page = "brand_kit"
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
            st.session_state.username = ""
            st.rerun()

# ==================== HOME DASHBOARD ====================
if st.session_state.page == "home":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("🔍 Search 100,000+ templates, presentations, logos...", label_visibility="collapsed")
    with col2:
        if not st.session_state.logged_in:
            if st.button("Sign In / Up", use_container_width=True):
                st.session_state.page = "auth"
                st.rerun()

    st.markdown("<h1 style='text-align: center;'>What will you design today?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>All the tools to create like a pro</p>", unsafe_allow_html=True)
    
    # Category Toolbar
    cats = ["Templates", "Presentation", "Social media", "Video", "Printables", "Doc", "Website"]
    cols = st.columns(len(cats))
    for i, cat in enumerate(cats):
        with cols[i]:
            if st.button(cat, use_container_width=True):
                if cat == "Presentation":
                    st.session_state.page = "presentation_maker"
                else:
                    st.session_state.page = "editor"
                st.rerun()

    st.write("---")
    
    # Feature Cards
    c1, c2 = st.columns(2)
    with c1:
        st.info("🖼️ **Swap Backgrounds**\nInstantly remove or replace image backgrounds with AI.")
        if st.button("Open Background Tool"):
            st.session_state.page = "editor"
            st.rerun()
    with c2:
        st.warning("🎨 **Brand Logos**\nCapture the essence of your brand in a custom logo.")
        if st.button("Open Logo Generator"):
            st.session_state.page = "brand_kit"
            st.rerun()

# ==================== PRESENTATION MAKER ====================
elif st.session_state.page == "presentation_maker":
    st.header("📊 Presentation Maker")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        
    st.write("Create and edit your presentation slides.")
    
    tabs = st.columns(len(st.session_state.presentation_slides) + 1)
    for idx, s in enumerate(st.session_state.presentation_slides):
        with tabs[idx]:
            if st.button(f"Slide {idx+1}", key=f"slide_tab_{idx}"):
                st.session_state.current_slide_idx = idx
                st.rerun()
    with tabs[-1]:
        if st.button("➕ Add Slide"):
            st.session_state.presentation_slides.append({
                "title": f"Slide {len(st.session_state.presentation_slides)+1}",
                "bg": "#FF6B35",
                "text": "New slide content..."
            })
            st.session_state.current_slide_idx = len(st.session_state.presentation_slides) - 1
            st.rerun()

    curr = st.session_state.current_slide_idx
    slide = st.session_state.presentation_slides[curr]
    
    col_t, col_c = st.columns(2)
    with col_t:
        slide["title"] = st.text_input("Slide Title", slide["title"])
        slide["text"] = st.text_area("Slide Content", slide["text"])
        slide["bg"] = st.color_picker("Background Color", slide["bg"])
    with col_c:
        img = Image.new("RGB", (1920, 1080), color=slide["bg"])
        draw = ImageDraw.Draw(img)
        draw.text((150, 200), slide["title"], fill="#FFFFFF")
        draw.text((150, 400), slide["text"], fill="#FFFFFF")
        st.image(img, use_container_width=True)

# ==================== DESIGN WORKSPACE ====================
elif st.session_state.page == "editor":
    st.header("🎨 Design Workspace")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        
    col_t, col_c = st.columns(1)
    with col_t:
        text = st.text_input("Heading Text", "Create Like A Pro")
        color = st.color_picker("Text Color", "#FFFFFF")
        bg = st.color_picker("Canvas Background", "#7D2AE8")
        
        canvas = Image.new("RGB", (1280, 720), color=bg)
        draw = ImageDraw.Draw(canvas)
        draw.text((100, 100), text, fill=color)
        st.image(canvas, use_container_width=True)

# ==================== BRAND KIT ====================
elif st.session_state.page == "brand_kit":
    st.header("👑 Brand Kit")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.color_picker("Primary Brand Color", "#7D2AE8")
    st.color_picker("Secondary Brand Color", "#00C4CC")
    st.file_uploader("Upload Brand Logo", type=["png", "svg"])

# ==================== AUTHENTICATION ====================
elif st.session_state.page == "auth":
    st.header("🔑 Account Access")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        
    tab1, tab2 = st.tabs(["Sign In", "Register"])
    with tab1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                if u in st.session_state.saved_users and st.session_state.saved_users[u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success("Signed in successfully!")
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Invalid credentials (try admin / password123)")
    with tab2:
        with st.form("signup"):
            un = st.text_input("Choose Username")
            pw = st.text_input("Create Password", type="password")
            if st.form_submit_button("Register"):
                if un and pw:
                    st.session_state.saved_users[un] = pw
                    st.session_state.logged_in = True
                    st.session_state.username = un
                    st.success("Account created!")
                    st.session_state.page = "home"
                    st.rerun()
