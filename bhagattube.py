import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import io

# 1. Page Configuration
st.set_page_config(
    page_title="BhagaTube - Visual Suite & AI Design Platform",
    page_icon="🎨",
    layout="wide"
)

# 2. Global State Initialization
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_business_modal" not in st.session_state:
    st.session_state.show_business_modal = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "BhagaTube Creator"
if "recent_designs" not in st.session_state:
    st.session_state.recent_designs = [
        {"title": "YouTube Tech Review Thumbnail", "type": "Thumbnail (1280x720)", "date": "1 day ago"},
        {"title": "Product Launch Slide Deck", "type": "Presentation (1920x1080)", "date": "3 days ago"},
        {"title": "Instagram Summer Event Promo", "type": "Social Post (1080x1080)", "date": "5 days ago"}
    ]

# 3. Custom Canva-Style Aesthetic CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #0E1318;
    }
    .hero-title {
        font-size: 46px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #7D2AE8, #00C4CC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .sub-hero {
        font-size: 16px;
        text-align: center;
        color: #5E6267;
        margin-bottom: 25px;
    }
    .card-yellow {
        background: #FFD43B;
        padding: 25px;
        border-radius: 18px;
        color: #0E1318;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-orange {
        background: #FF6B35;
        padding: 25px;
        border-radius: 18px;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-purple {
        background: #7D2AE8;
        padding: 25px;
        border-radius: 18px;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    .card-green {
        background: #00C4CC;
        padding: 20px;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== LEFT VERTICAL SIDEBAR MENU ====================
with st.sidebar:
    st.title("🎨 BhagaTube")
    st.caption("Canva-Style Visual Suite")
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

# ==================== CANVA PRO & BUSINESS POPUP MODAL ====================
if st.session_state.show_business_modal:
    st.info("👑 **Try BhagaTube Business for Free (30-Day Trial)**")
    st.write("Unlock Brand Kits, Background Removers, Magic Resize, and 20x AI usage across your entire team.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.radio("Choose Tier:", ["Pro (Individual) - $12.99/mo", "Business (Teams) - $14.99/user/mo", "Enterprise Suite - Custom"])
    with col_p2:
        st.number_input("Team Seat Count:", min_value=1, max_value=200, value=5)
        
    m_c1, m_c2 = st.columns(2)
    with m_c1:
        if st.button("🚀 Start 30-Day Free Trial", use_container_width=True):
            st.success("Business Trial Activated Successfully!")
            st.session_state.show_business_modal = False
            st.rerun()
    with m_c2:
        if st.button("✕ Close Window", use_container_width=True):
            st.session_state.show_business_modal = False
            st.rerun()
    st.divider()

# ==================== PAGE 1: HOME DASHBOARD ====================
if st.session_state.page == "home":
    
    # Top Search Header Bar
    top_c1, top_c2, top_c3 = st.columns([3, 1.2, 1])
    with top_c1:
        st.text_input("🔍 Search 100,000+ templates, docs, videos, or AI magic tools...", label_visibility="collapsed")
    with top_c2:
        if st.button("👑 Try Business Free"):
            st.session_state.show_business_modal = True
    with top_c3:
        if not st.session_state.logged_in:
            if st.button("Sign In / Up"):
                st.session_state.page = "auth"
                st.rerun()
        else:
            st.caption("🔔 Notifications (3)")

    # Hero Main Header
    st.markdown("<div class='hero-title'>What will you design today?</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-hero'>Create, edit, and collaborate with AI tools for presentations, social media, and video.</div>", unsafe_allow_html=True)
    
    # 13 Category Pills Toolbar
    cat_cols = st.columns(13)
    categories = ["Templates", "Presentation", "Social media", "Video", "Printables", "Doc", "Whiteboard", "Sheet", "Website", "Magic Layers", "Custom size", "Upload", "More"]
    for idx, cat in enumerate(categories):
        with cat_cols[idx]:
            if st.button(cat, key=f"cat_{idx}", use_container_width=True):
                st.session_state.page = "editor"
                st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Section 1: AI Feature Tools (Matching Screenshots)
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.markdown("""
            <div class='card-yellow'>
                <h3>Swap distracting backgrounds & transform your photos</h3>
                <p>Instantly remove or replace image backgrounds with precision AI.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change background"):
            st.session_state.page = "editor"
            st.rerun()
            
    with r1_col2:
        st.markdown("""
            <div class='card-orange'>
                <h3>Capture the essence of your brand in a logo</h3>
                <p>Generate professional vectors and brand kits from simple prompts.</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("Logo design for...", placeholder="e.g. Organic Coffee Shop")
        if st.button("Generate a logo"):
            st.session_state.page = "brand_kit"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.markdown("""
            <div class='card-purple'>
                <h3>Reimagine your image with a short written prompt</h3>
                <p>Type what you want to change, like 'Change bag to blue' with Magic Edit.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Try Magic Edit"):
            st.session_state.page = "editor"
            st.rerun()
            
    with r2_col2:
        st.markdown("""
            <div class='card-green'>
                <h3>Generate natural-sounding AI voices</h3>
                <p>Convert text straight into engaging audio voiceovers and avatars.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Generate voice"):
            st.session_state.page = "editor"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Section 2: Magic Media Image Generator
    st.subheader("🪄 Try Image Generator")
    st.caption("Turn pure text to art with Magic Media™ and our range of AI art generator tools. Simply enter a prompt, pick a style, and watch your words transform into beautiful art.")
    
    img_gen_1, img_gen_2 = st.columns([2, 1])
    with img_gen_1:
        st.text_input("Prompt:", value="Moon rising over the mountains")
        st.selectbox("Style Preset:", ["Dreamy", "Anime", "Watercolor", "Filmic", "3D Render"])
        if st.button("Generate Art"):
            st.session_state.page = "editor"
            st.rerun()
    with img_gen_2:
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", caption="AI Generation Preview")

    st.divider()

    # Section 3: Business Features & Brand Management
    st.subheader("Our Business Features")
    st.caption("Enhance the design capabilities of your team or business with BhagaTube business plans!")
    
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown("<div class='card-green'><h4>Set up a Brand Kit to unify your designs</h4><p>Ensure logos, colors, and typography stay consistent across all exports.</p></div>", unsafe_allow_html=True)
        if st.button("Learn More & Configure", key="b1"):
            st.session_state.page = "brand_kit"
            st.rerun()
    with b_col2:
        st.markdown("<div class='card-green'><h4>Empower your team to scale content</h4><p>Manage permissions, lock templates, and collaborate seamlessly.</p></div>", unsafe_allow_html=True)
        if st.button("View Team Plans", key="b2"):
            st.session_state.show_business_modal = True
            st.rerun()
    with b_col3:
        st.markdown("<div class='card-green'><h4>Collaborate & create in real time</h4><p>Multi-user editing, comments, and project workflows.</p></div>", unsafe_allow_html=True)
        if st.button("Explore Collaboration", key="b3"):
            st.session_state.show_business_modal = True
            st.rerun()

    st.divider()

    # Section 4: Templates Showcase
    st.subheader("Templates for absolutely anything")
    t_btn1, t_btn2 = st.columns(2)
    with t_btn1:
        if st.button("✨ Start designing for free", use_container_width=True):
            st.session_state.page = "editor"
            st.rerun()
    with t_btn2:
        if st.button("📁 Browse all templates", use_container_width=True):
            st.session_state.page = "editor"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)
    t_grid1, t_grid2, t_grid3, t_grid4 = st.columns(4)
    with t_grid1:
        st.image("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400", caption="Party Invitation")
    with t_grid2:
        st.image("https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400", caption="House Party Flyer")
    with t_grid3:
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400", caption="Festival Greeting")
    with t_grid4:
        st.image("https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400", caption="Sports Tournament")

# ==================== PAGE 2: PROJECTS & FOLDERS ====================
elif st.session_state.page == "projects":
    st.header("📁 Projects & Folders")
    st.write("Access your saved designs, team folders, and uploaded assets.")
    
    for item in st.session_state.recent_designs:
        col_a, col_b, col_c = st.columns([3, 2, 1])
        with col_a:
            st.markdown(f"**{item['title']}**")
        with col_b:
            st.caption(f"{item['type']} • Edited {item['date']}")
        with col_c:
            if st.button("Open", key=item['title']):
                st.session_state.page = "editor"
                st.rerun()
        st.divider()

# ==================== PAGE 3: BRAND KIT MANAGER ====================
elif st.session_state.page == "brand_kit":
    st.header("👑 BhagaTube Brand Hub")
    st.write("Manage color palettes, typography, and logos for consistent design output.")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Color Palettes", "🔤 Typography", "🖼️ Logos & Assets"])
    
    with tab1:
        st.subheader("Brand Colors")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.color_picker("Primary Color", "#7D2AE8")
        with c2: st.color_picker("Secondary Color", "#00C4CC")
        with c3: st.color_picker("Accent Color", "#FF6B35")
        with c4: st.color_picker("Background Fill", "#F8F9FA")
        if st.button("Save Palette"):
            st.success("Palette Saved to Brand Kit!")
            
    with tab2:
        st.subheader("Fonts")
        st.selectbox("Heading Font Family", ["Sans-Serif Bold", "Serif Elegant", "Monospace Tech", "Script Display"])
        st.selectbox("Body Font Family", ["Inter", "Roboto", "Open Sans", "Lato"])
        
    with tab3:
        st.subheader("Logo Assets")
        st.file_uploader("Upload PNG or SVG logo files", type=["png", "svg"])

# ==================== PAGE 4: FULL WORKING CANVA EDITOR ====================
elif st.session_state.page == "editor":
    st.header("🎨 Interactive Design Workspace")
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()
        
    st.divider()
    
    tool_col, canvas_col = st.columns([1, 2])
    
    with tool_col:
        st.subheader("🛠️ Design Controls")
        
        # Template selection
        preset = st.selectbox("Format Size Preset", [
            "YouTube Thumbnail (1280x720)", 
            "Instagram Post (1080x1080)", 
            "Presentation Slide (1920x1080)",
            "Custom Upload Image"
        ])
        
        uploaded_image = None
        if preset == "Custom Upload Image":
            file_up = st.file_uploader("Upload canvas background", type=["jpg", "png", "jpeg"])
            if file_up:
                uploaded_image = Image.open(file_up)
                
        bg_color = st.color_picker("Background Color", "#7D2AE8")
        
        if uploaded_image:
            base = uploaded_image.convert("RGB")
        else:
            if "Thumbnail" in preset:
                base = Image.new("RGB", (1280, 720), color=bg_color)
            elif "Instagram" in preset:
                base = Image.new("RGB", (1080, 1080), color=bg_color)
            else:
                base = Image.new("RGB", (1920, 1080), color=bg_color)

        st.markdown("---")
        st.write("🔤 **Text Customization**")
        heading_text = st.text_input("Overlay Heading Text:", "BhagaTube Studio")
        heading_color = st.color_picker("Heading Color:", "#FFFFFF")
        pos_x = st.slider("Position X:", 0, base.width - 100, int(base.width * 0.1))
        pos_y = st.slider("Position Y:", 0, base.height - 100, int(base.height * 0.1))
        
        st.markdown("---")
        st.write("✨ **Effects & AI Filters**")
        filter_opt = st.selectbox("Apply Filter Effect:", ["None", "Grayscale", "Blur", "Contour", "Invert Color", "Detail Enhance"])
        brightness_val = st.slider("Brightness Boost:", 0.5, 2.0, 1.0)
        contrast_val = st.slider("Contrast Boost:", 0.5, 2.0, 1.0)

    with canvas_col:
        st.subheader("🖼️ Live Workspace Preview")
        
        working_img = base.copy()
        
        if filter_opt == "Grayscale":
            working_img = working_img.convert("L").convert("RGB")
        elif filter_opt == "Blur":
            working_img = working_img.filter(ImageFilter.BLUR)
        elif filter_opt == "Contour":
            working_img = working_img.filter(ImageFilter.CONTOUR)
        elif filter_opt == "Invert Color":
            working_img = ImageOps.invert(working_img)
        elif filter_opt == "Detail Enhance":
            working_img = working_img.filter(ImageFilter.DETAIL)

        working_img = ImageEnhance.Brightness(working_img).enhance(brightness_val)
        working_img = ImageEnhance.Contrast(working_img).enhance(contrast_val)
        
        draw = ImageDraw.Draw(working_img)
        draw.text((pos_x, pos_y), heading_text, fill=heading_color)
        
        st.image(working_img, use_container_width=True)
        
        buffer = io.BytesIO()
        working_img.save(buffer, format="PNG")
        byte_data = buffer.getvalue()
        
        st.download_button(
            label="📥 Download Exported Design (.png)",
            data=byte_data,
            file_name="bhagatube_export.png",
            mime="image/png",
            use_container_width=True
        )

# ==================== PAGE 5: AUTHENTICATION ====================
elif st.session_state.page == "auth":
    st.header("🔑 BhagaTube User Account")
    tab1, tab2 = st.tabs(["Sign In", "Register Account"])
    
    with tab1:
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                st.session_state.logged_in = True
                st.session_state.username = user if user else "Creator"
                st.success("Signed in successfully!")
                st.session_state.page = "home"
                st.rerun()
                
    with tab2:
        with st.form("signup_form"):
            fn = st.text_input("Full Name")
            em = st.text_input("Email Address")
            un = st.text_input("Choose Username")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account"):
                st.session_state.logged_in = True
                st.session_state.username = un if un else fn
                st.success("Account created!")
                st.session_state.page = "editor"
                st.rerun()
