import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(
    page_title="BhagaTube",
    page_icon="🎨",
    layout="wide"
)

# Initialize Session State for Authentication & Navigation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "home"
if "users_db" not in st.session_state:
    st.session_state.users_db = {"demo_user": "password123"} # Sample user

# Custom Canva-Style Theme (Purple-Blue Gradient & Clean Layout)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1b4b, #312e81, #4c1d95, #1e3a8a);
        color: white;
    }
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .logo {
        font-family: 'Brush Script MT', cursive, sans-serif;
        font-style: italic;
        font-size: 32px;
        font-weight: bold;
        color: #FFFFFF;
        text-decoration: none;
    }
    .nav-center {
        font-size: 14px;
        color: #E2E8F0;
        word-spacing: 15px;
        font-weight: 500;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #FFFFFF;
        margin-top: 30px;
    }
    .hero-subtitle {
        font-size: 16px;
        text-align: center;
        color: #CBD5E1;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
col_logo, col_links, col_auth = st.columns([1.5, 3, 2])

with col_logo:
    if st.button("bhagatube", key="logo_btn"):
        st.session_state.page = "home"
        st.rerun()

with col_links:
    st.markdown("<div class='nav-center'>design &nbsp;&nbsp; product &nbsp;&nbsp; plans &nbsp;&nbsp; business &nbsp;&nbsp; education &nbsp;&nbsp; help</div>", unsafe_allow_html=True)

with col_auth:
    if not st.session_state.logged_in:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Sign In"):
                st.session_state.page = "signin"
                st.rerun()
        with c2:
            if st.button("Sign Up"):
                st.session_state.page = "signup"
                st.rerun()
        with c3:
            if st.button("Log In"):
                st.session_state.page = "login"
                st.rerun()
    else:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "home"
            st.rerun()

st.divider()

# ==================== PAGE ROUTING ====================

# 1. HOME LANDING PAGE
if st.session_state.page == "home":
    st.markdown("<div class='hero-title'>your ideas are now created by bhagatube</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>also for presentations, thumbnails and posters</div>", unsafe_allow_html=True)
    
    # Hero Image / Graphic Display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Placeholder or Canva-style illustration of a person creating designs
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop", 
                 caption="Create stunning visual media seamlessly with BhagaTube Studio tools.", 
                 use_container_width=True)
        
        if st.button("🚀 Start Designing Now", use_container_width=True):
            if st.session_state.logged_in:
                st.session_state.page = "editor"
                st.rerun()
            else:
                st.session_state.page = "login"
                st.warning("Please log in or sign up to access the design studio!")
                st.rerun()

# 2. SIGN UP PAGE
elif st.session_state.page == "signup":
    st.header("📝 Create Your BhagaTube Account")
    
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        username = st.text_input("Choose Username")
        email = st.text_input("Email Address")
        country = st.selectbox("Country", ["United States", "India", "United Kingdom", "Canada", "Australia", "Other"])
        password = st.text_input("Password", type="password")
        
        submit_btn = st.form_submit_button("Sign Up")
        
        if submit_btn:
            if username and password and email:
                st.session_state.users_db[username] = password
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Account created successfully!")
                st.session_state.page = "editor"
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
                
    st.write("---")
    st.write("Or sign up securely with:")
    col_g, col_a = st.columns(2)
    with col_g:
        if st.button("Google Account"):
            st.session_state.logged_in = True
            st.session_state.username = "GoogleUser"
            st.session_state.page = "editor"
            st.rerun()
    with col_a:
        if st.button("Apple ID"):
            st.session_state.logged_in = True
            st.session_state.username = "AppleUser"
            st.session_state.page = "editor"
            st.rerun()

# 3. LOG IN PAGE (Fast Login with Username & Password)
elif st.session_state.page == "login" or st.session_state.page == "signin":
    st.header("🔑 Fast Account Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        login_btn = st.form_submit_button("Log In")
        
        if login_btn:
            if username in st.session_state.users_db and st.session_state.users_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.session_state.page = "editor"
                st.rerun()
            else:
                st.error("Invalid username or password.")

# 4. BHAGATUBE DESIGN STUDIO (Canva-Style Editor)
elif st.session_state.page == "editor":
    st.header(f"🎨 BhagaTube Studio Workspace ({st.session_state.username})")
    
    tab1, tab2 = st.tabs(["🖼️ Graphic / Thumbnail Creator", "🎥 Video Editor"])
    
    with tab1:
        preset = st.selectbox("Canvas Template Size", ["YouTube Thumbnail (1280x720)", "Instagram Post (1080x1080)", "Presentation Slide (1920x1080)"])
        
        bg_col = st.color_picker("Background Color", "#4C1D95")
        
        if "Thumbnail" in preset:
            canvas = Image.new("RGB", (1280, 720), color=bg_col)
        elif "Instagram" in preset:
            canvas = Image.new("RGB", (1080, 1080), color=bg_col)
        else:
            canvas = Image.new("RGB", (1920, 1080), color=bg_col)
            
        c1, c2 = st.columns(2)
        with c1:
            custom_text = st.text_input("Add Heading Text", "BhagaTube Design")
            text_color = st.color_picker("Text Color", "#FFFFFF")
            font_size = st.slider("Text Size", 20, 120, 60)
            
        # Draw text onto canvas
        draw = ImageDraw.Draw(canvas)
        draw.text((100, 100), custom_text, fill=text_color)
        
        with c2:
            st.image(canvas, caption="Live Canva-Style Output Canvas", use_container_width=True)
            
    with tab2:
        st.subheader("Video Editing Suite")
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.slider("Trim Video Timeline (Seconds)", 0, 60, (0, 30))
        st.success("Video editing timeline active.")
