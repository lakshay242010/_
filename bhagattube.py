import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageOps
import io
import datetime

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="BhagaTube - Canva Master Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables for Complete App Persistence
if "page" not in st.session_state:
    st.session_state.page = "home"
if "show_business_modal" not in st.session_state:
    st.session_state.show_business_modal = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_plan" not in st.session_state:
    st.session_state.user_plan = "Free Creator"
if "saved_users" not in st.session_state:
    st.session_state.saved_users = {"admin": "password123"}
if "saved_palettes" not in st.session_state:
    st.session_state.saved_palettes = ["#7D2AE8", "#00C4CC", "#FF6B35", "#F8F9FA"]
if "recent_designs" not in st.session_state:
    st.session_state.recent_designs = [
        {"id": 1, "title": "YouTube Tech Review Thumbnail", "type": "Thumbnail (1280x720)", "date": "1 day ago", "status": "Ready"},
        {"id": 2, "title": "Startup Pitch Deck Presentation", "type": "Presentation (1920x1080)", "date": "3 days ago", "status": "Shared"},
        {"id": 3, "title": "Instagram Summer Event Promo", "type": "Social Post (1080x1080)", "date": "5 days ago", "status": "Draft"}
    ]
if "presentation_slides" not in st.session_state:
    st.session_state.presentation_slides = [
        {"title": "Slide 1: Welcome & Introduction", "bg": "#7D2AE8", "text": "Welcome to BhagaTube Presentation"},
        {"title": "Slide 2: Core Features & AI", "bg": "#00C4CC", "text": "Powered by Advanced AI Tools"},
        {"title": "Slide 3: Conclusion & Q&A", "bg": "#FF6B35", "text": "Thank You! Let's Create Together"}
    ]
if "current_slide_idx" not in st.session_state:
    st.session_state.current_slide_idx = 0

# ==========================================
# 2. STRICT LIGHT-THEME CANVA CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* Force Light Theme Background and Eliminate Black Gaps */
    .stApp {
        background-color: #F4F5F7 !important;
        color: #0E1318 !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        background-color: #F4F5F7 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }

    /* Typography Defaults */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #0E1318 !important;
    }

    /* Hero Gradient Title */
    .hero-title {
        font-size: 46px !important;
        font-weight: 800 !important;
        text-align: center !important;
        background: linear-gradient(90deg, #7D2AE8, #00C4CC) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-top: 10px !important;
        margin-bottom: 5px !important;
    }

    .hero-sub {
        font-size: 16px !important;
        text-align: center !important;
        color: #5E6267 !important;
        margin-bottom: 30px !important;
    }

    /* Interactive Canva Cards */
    .card-yellow {
        background-color: #FFD43B !important;
        padding: 30px !important;
        border-radius: 20px !important;
        color: #0E1318 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        height: 100%;
    }
    .card-yellow h3, .card-yellow p {
        color: #0E1318 !important;
    }

    .card-orange {
        background-color: #FF6B35 !important;
        padding: 30px !important;
        border-radius: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        height: 100%;
    }
    .card-orange h3, .card-orange p {
        color: #FFFFFF !important;
    }

    .card-purple {
        background-color: #7D2AE8 !important;
        padding: 30px !important;
        border-radius: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        height: 100%;
    }
    .card-purple h3, .card-purple p {
        color: #FFFFFF !important;
    }

    .card-green {
        background-color: #D1E7DD !important;
        padding: 25px !important;
        border-radius: 18px !important;
        color: #0F5132 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        height: 100%;
    }
    .card-green h4, .card-green p {
        color: #0F5132 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION MENU
# ==========================================
with st.sidebar:
    st.title("🎨 BhagaTube")
    st.caption("Visual Suite & Canva Master Studio")
    st.write("---")
    
    if st.button("🏠 Home Dashboard", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📊 Presentation Maker", use_container_width=True):
        st.session_state.page = "presentation_maker"
        st.rerun()
    if st.button("📁 Projects & Folders", use_container_width=True):
        st.session_state.page = "projects"
        st.rerun()
    if st.button("🖼️ Design Workspace", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    if st.button("👑 Brand Kit & Hub", use_container_width=True):
        st.session_state.page = "brand_kit"
        st.rerun()
    if st.button("👥 Team Collaboration", use_container_width=True):
        st.session_state.page = "teams"
        st.rerun()
    if st.button("🛍️ Print & Merchandise", use_container_width=True):
        st.session_state.page = "editor"
        st.rerun()
    if st.button("⚙️ Account Settings", use_container_width=True):
        st.session_state.page = "settings"
        st.rerun()
        
    st.write("---")
    if not st.session_state.logged_in:
        if st.button("🔑 Log In / Sign Up", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    else:
        st.success(f"👤 {st.session_state.username}")
        st.caption(f"Plan: {st.session_state.user_plan}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_plan = "Free Creator"
            st.session_state.page = "home"
            st.rerun()

# ==========================================
# 4. BUSINESS & PRO MODAL POPUP SYSTEM
# ==========================================
if st.session_state.show_business_modal:
    st.info("👑 **Try BhagaTube Business for Free (30-Day Trial)**")
    st.write("Unlock unlimited AI usage, background removal, brand kits, and real-time team collaboration.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        selected_tier = st.radio("Choose Subscription Tier:", ["Pro (Individual) - $12.99/mo", "Business (Teams) - $14.99/user/mo", "Enterprise Suite - Custom"])
    with col_p2:
        seat_count = st.number_input("Team Seat Count:", min_value=1, max_value=500, value=5)
        
    m_c1, m_c2 = st.columns(2)
    with m_c1:
        if st.button("🚀 Start 30-Day Free Trial", use_container_width=True):
            st.session_state.user_plan = selected_tier.split(" - ")[0]
            st.success("Business Trial Activated Successfully!")
            st.session_state.show_business_modal = False
            st.rerun()
    with m_c2:
        if st.button("✕ Close Window", use_container_width=True):
            st.session_state.show_business_modal = False
            st.rerun()
    st.divider()

# ==========================================
# 5. PAGE ROUTING CONTROLLER
# ==========================================

# --- HOME DASHBOARD ---
if st.session_state.page == "home":
    top_c1, top_c2, top_c3 = st.columns([3, 1.2, 1])
    with top_c1:
        st.text_input("🔍 Search 100,000+ templates, documents, videos, or AI tools...", label_visibility="collapsed")
    with top_c2:
        if st.button("👑 Try Business Free"):
            st.session_state.show_business_modal = True
    with top_c3:
        if not st.session_state.logged_in:
            if st.button("Sign In / Up"):
                st.session_state.page = "auth"
                st.rerun()
        else:
            st.caption(f"🔔 Notifications (2)")

    st.markdown("<div class='hero-title'>What will you design today?</div>", unsafe_allow_html=True)
    st.markdown("<p class='hero-sub'>All the tools to create like a pro</p>", unsafe_allow_html=True)
    
    # 13 Category Toolbar Pills
    cat_cols = st.columns(13)
    categories = ["Templates", "Presentation", "Social media", "Video", "Printables", "Doc", "Whiteboard", "Sheet", "Website", "Magic Layers", "Custom size", "Upload", "More"]
    for idx, cat in enumerate(categories):
        with cat_cols[idx]:
            if st.button(cat, key=f"cat_{idx}", use_container_width=True):
                if cat == "Presentation":
                    st.session_state.page = "presentation_maker"
                else:
                    st.session_state.page = "editor"
                st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.markdown("""
            <div class='card-yellow'>
                <h3>Swap distracting backgrounds & transform your photos</h3>
                <p>Instantly remove or replace image backgrounds with AI.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change background"):
            st.session_state.page = "editor"
            st.rerun()
            
    with r1_col2:
        st.markdown("""
            <div class='card-orange'>
                <h3>Capture the essence of your brand in a logo</h3>
                <p>Generate professional vectors and custom branding from prompts.</p>
            </div>
        """, unsafe_allow_html=True)
        logo_input = st.text_input("Logo design for...", placeholder="e.g. Coffee shop, Gaming clan...")
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
            <div class='card-yellow'>
                <h3>Generate natural-sounding AI voices</h3>
                <p>Convert text straight into engaging audio voiceovers and avatars.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Generate voice"):
            st.session_state.page = "editor"
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    st.subheader("🪄 Try Image Generator")
    st.write("Turn pure text to art with Magic Media™ and our range of AI art generator tools.")
    
    img_gen_1, img_gen_2 = st.columns([2, 1])
    with img_gen_1:
        ai_prompt = st.text_input("Prompt:", value="Moon rising over the mountains")
        ai_style = st.selectbox("Style Preset:", ["Dreamy", "Anime", "Watercolor", "Filmic", "3D Render"])
        if st.button("Generate Art"):
            st.session_state.page = "editor"
            st.rerun()
    with img_gen_2:
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", caption="AI Generation Preview")

    st.divider()

    st.subheader("Our Business Features")
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown("""
            <div class='card-green'>
                <h4>Set up a Brand Kit to unify your designs</h4>
                <p>Ensure logos, fonts, and colors stay consistent across all team exports.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Learn more", key="b1"):
            st.session_state.page = "brand_kit"
            st.rerun()
    with b_col2:
        st.markdown("""
            <div class='card-green'>
                <h4>Empower your team to scale content</h4>
                <p>Manage permissions, lock templates, and collaborate seamlessly.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Learn more", key="b2"):
            st.session_state.show_business_modal = True
            st.rerun()
    with b_col3:
        st.markdown("""
            <div class='card-green'>
                <h4>Collaborate & create in real time</h4>
                <p>Multi-user editing, comments, and unified project workflows.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View plans", key="b3"):
            st.session_state.show_business_modal = True
            st.rerun()

# --- PRESENTATION MAKER WORKSPACE ---
elif st.session_state.page == "presentation_maker":
    st.header("📊 BhagaTube Presentation Maker")
    st.write("Create, edit, and organize multi-slide presentation decks just like Canva.")
    
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        
    st.divider()
    
    # Slide Navigation Bar
    slide_tabs = st.columns(len(st.session_state.presentation_slides) + 1)
    for idx, s in enumerate(st.session_state.presentation_slides):
        with slide_tabs[idx]:
            if st.button(f"Slide {idx+1}", use_container_width=True, key=f"sl_btn_{idx}"):
                st.session_state.current_slide_idx = idx
                st.rerun()
                
    with slide_tabs[-1]:
        if st.button("➕ Add Slide", use_container_width=True):
            new_idx = len(st.session_state.presentation_slides) + 1
            st.session_state.presentation_slides.append({
                "title": f"Slide {new_idx}: New Section",
                "bg": "#20C997",
                "text": "Type slide presentation text here..."
            })
            st.session_state.current_slide_idx = len(st.session_state.presentation_slides) - 1
            st.rerun()

    st.divider()
    
    curr_idx = st.session_state.current_slide_idx
    active_slide = st.session_state.presentation_slides[curr_idx]
    
    p_tool, p_canvas = st.columns([1, 2])
    
    with p_tool:
        st.subheader(f"Editing Slide {curr_idx + 1}")
        slide_title = st.text_input("Slide Heading Title", active_slide["title"])
        slide_text = st.text_area("Slide Body Content", active_slide["text"])
        slide_bg = st.color_picker("Slide Background Color", active_slide["bg"])
        
        active_slide["title"] = slide_title
        active_slide["text"] = slide_text
        active_slide["bg"] = slide_bg
        
        if st.button("🗑️ Delete Current Slide", use_container_width=True):
            if len(st.session_state.presentation_slides) > 1:
                st.session_state.presentation_slides.pop(curr_idx)
                st.session_state.current_slide_idx = max(0, curr_idx - 1)
                st.rerun()
            else:
                st.warning("You must have at least one slide in your presentation.")

    with p_canvas:
        st.subheader("🖼️ Live Slide Preview (1920x1080)")
        slide_img = Image.new("RGB", (1920, 1080), color=slide_bg)
        draw = ImageDraw.Draw(slide_img)
        draw.text((150, 200), slide_title, fill="#FFFFFF")
        draw.text((150, 400), slide_text, fill="#FFFFFF")
        
        st.image(slide_img, use_container_width=True)
        
        buf = io.BytesIO()
        slide_img.save(buf, format="PNG")
        st.download_button(
            label=f"📥 Download Slide {curr_idx + 1} (.png)",
            data=buf.getvalue(),
            file_name=f"slide_{curr_idx + 1}.png",
            mime="image/png",
            use_container_width=True
        )

# --- PROJECTS MANAGER ---
elif st.session_state.page == "projects":
    st.header("📁 Projects & Folders Manager")
    st.write("Access your saved designs, team folders, and uploaded assets.")
    
    new_proj_name = st.text_input("Create New Project:", placeholder="Enter design title...")
    if st.button("Create Project"):
        if new_proj_name:
            st.session_state.recent_designs.insert(0, {"id": len(st.session_state.recent_designs)+1, "title": new_proj_name, "type": "Custom Canvas", "date": "Just now", "status": "Draft"})
            st.success(f"Project '{new_proj_name}' created successfully!")
            st.rerun()

    st.divider()
    for item in st.session_state.recent_designs:
        c1, c2, c3, c4 = st.columns([2.5, 2, 1, 1])
        with c1: st.markdown(f"**{item['title']}**")
        with c2: st.caption(f"{item['type']} • {item['date']}")
        with c3: st.caption(f"Status: {item['status']}")
        with c4:
            if st.button("Open", key=f"proj_{item['id']}"):
                st.session_state.page = "editor"
                st.rerun()
        st.divider()

# --- BRAND KIT HUB ---
elif st.session_state.page == "brand_kit":
    st.header("👑 BhagaTube Brand Hub")
    st.write("Manage your brand logos, color palettes, and typography.")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Color Palettes", "🔤 Brand Typography", "🖼️ Logo Assets"])
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        with c1: p1 = st.color_picker("Primary Color", st.session_state.saved_palettes[0])
        with c2: p2 = st.color_picker("Secondary Color", st.session_state.saved_palettes[1])
        with c3: p3 = st.color_picker("Accent Color", st.session_state.saved_palettes[2])
        with c4: p4 = st.color_picker("Background Fill", st.session_state.saved_palettes[3])
        if st.button("Save Palette"):
            st.session_state.saved_palettes = [p1, p2, p3, p4]
            st.success("Brand Palette Saved Successfully!")
    with tab2:
        st.selectbox("Heading Font Family", ["Sans-Serif Bold", "Serif Elegant", "Monospace Tech", "Display Script"])
        st.selectbox("Body Font Family", ["Inter", "Roboto", "Open Sans", "Lato"])
    with tab3:
        st.file_uploader("Upload PNG or SVG brand logos", type=["png", "svg"])

# --- TEAM COLLABORATION HUB ---
elif st.session_state.page == "teams":
    st.header("👥 Team Collaboration Workspace")
    st.write("Invite team members, assign design permissions, and manage real-time co-editing.")
    
    invite_email = st.text_input("Invite Teammate by Email:", placeholder="colleague@company.com")
    member_role = st.selectbox("Assign Role:", ["Editor", "Viewer", "Brand Admin"])
    if st.button("Send Invitation"):
        if invite_email:
            st.success(f"Invitation sent successfully to {invite_email} as {member_role}!")
            
    st.divider()
    st.markdown("👤 **BhagaTube Creator** (Owner) — *Online*")
    st.markdown("👤 **Sarah Jenkins** (Editor) — *Active 5 mins ago*")

# --- ACCOUNT SETTINGS ---
elif st.session_state.page == "settings":
    st.header("⚙️ Account Settings & Preferences")
    with st.form("settings_form"):
        st.text_input("Display Name", value=st.session_state.username)
        st.text_input("Email Address", value=st.session_state.user_email)
        st.selectbox("Language Preference", ["English (US)", "Spanish", "French", "German", "Hindi"])
        if st.form_submit_button("Save Changes"):
            st.success("Account settings updated successfully!")

# --- DESIGN WORKSPACE ---
elif st.session_state.page == "editor":
    st.header("🎨 Interactive Design Workspace")
    if st.button("← Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()
        
    st.divider()
    tool_col, canvas_col = st.columns([1, 2])
    
    with tool_col:
        st.subheader("🛠️ Editing Toolkit")
        preset = st.selectbox("Format Size Preset", ["YouTube Thumbnail (1280x720)", "Instagram Post (1080x1080)", "Presentation (1920x1080)", "Custom Upload"])
        
        uploaded_image = None
        if preset == "Custom Upload":
            file_up = st.file_uploader("Upload background image", type=["jpg", "png", "jpeg"])
            if file_up: uploaded_image = Image.open(file_up)
                
        bg_color = st.color_picker("Background Color", st.session_state.saved_palettes[0])
        
        if uploaded_image:
            base = uploaded_image.convert("RGB")
        else:
            base = Image.new("RGB", (1280, 720) if "Thumbnail" in preset else (1080, 1080), color=bg_color)

        st.markdown("---")
        heading_text = st.text_input("Heading Text", "BhagaTube Creation")
        heading_color = st.color_picker("Text Color", st.session_state.saved_palettes[1])
        pos_x = st.slider("Position X", 0, base.width - 100, int(base.width * 0.1))
        pos_y = st.slider("Position Y", 0, base.height - 100, int(base.height * 0.1))
        
        st.markdown("---")
        filter_opt = st.selectbox("Apply Visual Filter", ["None", "Grayscale", "Blur", "Contour", "Invert Color", "Detail Enhance"])
        brightness_val = st.slider("Brightness Boost", 0.5, 2.0, 1.0)

    with canvas_col:
        st.subheader("🖼️ Live Workspace Preview")
        working_img = base.copy()
        
        if filter_opt == "Grayscale": working_img = working_img.convert("L").convert("RGB")
        elif filter_opt == "Blur": working_img = working_img.filter(ImageFilter.BLUR)
        elif filter_opt == "Contour": working_img = working_img.filter(ImageFilter.CONTOUR)
        elif filter_opt == "Invert Color": working_img = ImageOps.invert(working_img)
        elif filter_opt == "Detail Enhance": working_img = working_img.filter(ImageFilter.DETAIL)

        working_img = ImageEnhance.Brightness(working_img).enhance(brightness_val)
        
        draw = ImageDraw.Draw(working_img)
        draw.text((pos_x, pos_y), heading_text, fill=heading_color)
        
        st.image(working_img, use_container_width=True)
        
        buffer = io.BytesIO()
        working_img.save(buffer, format="PNG")
        st.download_button("📥 Download Exported Design (.png)", data=buffer.getvalue(), file_name="bhagatube_export.png", mime="image/png", use_container_width=True)

# --- AUTHENTICATION PAGE ---
elif st.session_state.page == "auth":
    st.header("🔑 BhagaTube User Account Access")
    tab1, tab2 = st.tabs(["Sign In", "Register Account"])
    
    with tab1:
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                if u in st.session_state.saved_users and st.session_state.saved_users[u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success("Signed in successfully!")
                    st.session_state.page = "home"
                    st.rerun()
                elif u == "admin" and p == "password123":
                    st.session_state.logged_in = True
                    st.session_state.username = "admin"
                    st.success("Signed in successfully!")
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
    with tab2:
        with st.form("signup_form"):
            fn = st.text_input("Full Name")
            em = st.text_input("Email Address")
            un = st.text_input("Choose Username")
            pw = st.text_input("Create Password", type="password")
            if st.form_submit_button("Create Account"):
                if un and pw:
                    st.session_state.saved_users[un] = pw
                    st.session_state.logged_in = True
                    st.session_state.username = un
                    st.session_state.user_email = em
                    st.success("Account created successfully!")
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Please fill in username and password.")
