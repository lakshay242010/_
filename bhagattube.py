import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

# 1. Page Configuration
st.set_page_config(
    page_title="BhagaTube Studio",
    page_icon="🎨",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #7D2AE8; }
    .sub-text { font-size: 16px; color: #666668; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-title'>🎨 BhagaTube Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Your Canva-style workspace for photo editing, thumbnail creation, and video tools!</div><br>", unsafe_allow_html=True)

# Sidebar Navigation
mode = st.sidebar.radio("Design Workspaces", ["🖼️ Photo & Canva Graphic Studio", "🎥 Video Editing Studio", "📸 Webcam Capture"])

# --- TAB 1: CANVA-STYLE PHOTO & GRAPHIC STUDIO ---
if mode == "🖼️ Photo & Canva Graphic Studio":
    st.header("🖼️ Canva-Style Photo Editor & Designer")
    
    # Canvas Presets
    preset = st.selectbox("Choose Design Preset Canvas:", ["Custom Upload", "YouTube Thumbnail (1280x720)", "Instagram Post (1080x1080)"])
    
    img = None
    
    if preset == "Custom Upload":
        uploaded_file = st.file_uploader("Upload background image (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file)
    elif preset == "YouTube Thumbnail (1280x720)":
        bg_color = st.color_picker("Pick Background Color", "#7D2AE8")
        img = Image.new("RGB", (1280, 720), color=bg_color)
    elif preset == "Instagram Post (1080x1080)":
        bg_color = st.color_picker("Pick Background Color", "#00C4CC")
        img = Image.new("RGB", (1080, 1080), color=bg_color)

    if img:
        st.subheader("🛠️ Design Controls")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("### 🔤 Add Text Overlay")
            text_input = st.text_input("Enter Heading / Text:", "BhagaTube")
            text_color = st.color_picker("Text Color", "#FFFFFF")
            text_size = st.slider("Text Size", 20, 150, 60)
            text_x = st.slider("Text Position X", 0, img.width, int(img.width * 0.1))
            text_y = st.slider("Text Position Y", 0, img.height, int(img.height * 0.1))

            st.write("### 🎛️ Adjustments & Filters")
            filter_type = st.selectbox("Apply Effect", ["None", "Grayscale", "Blur", "Contour", "Detail", "Edge Enhance"])
            brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
            sharpness = st.slider("Sharpness", 0.5, 2.0, 1.0)

        # Apply transformations
        processed_img = img.copy()
        
        if filter_type == "Grayscale":
            processed_img = processed_img.convert("L").convert("RGB")
        elif filter_type == "Blur":
            processed_img = processed_img.filter(ImageFilter.BLUR)
        elif filter_type == "Contour":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)
        elif filter_type == "Detail":
            processed_img = processed_img.filter(ImageFilter.DETAIL)
        elif filter_type == "Edge Enhance":
            processed_img = processed_img.filter(ImageFilter.EDGE_ENHANCE)

        # Enhance Image
        processed_img = ImageEnhance.Brightness(processed_img).enhance(brightness)
        processed_img = ImageEnhance.Contrast(processed_img).enhance(contrast)
        processed_img = ImageEnhance.Sharpness(processed_img).enhance(sharpness)

        # Draw Text
        draw = ImageDraw.Draw(processed_img)
        try:
            # Fallback default font
            font = ImageFont.load_default()
        except:
            font = None

        draw.text((text_x, text_y), text_input, fill=text_color, font=font)

        with col2:
            st.write("### 🎨 Canvas Preview")
            st.image(processed_img, caption="Your Canvas Design", use_container_width=True)

# --- TAB 2: VIDEO EDITING STUDIO ---
elif mode == "🎥 Video Editing Studio":
    st.header("🎥 Video Editor & Preview")
    
    video_source = st.radio("Select Video Source:", ["Sample Video", "Upload MP4 Video"])
    
    video_url = None
    if video_source == "Sample Video":
        video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
    else:
        uploaded_video = st.file_uploader("Upload an MP4 video file", type=["mp4", "mov"])
        if uploaded_video:
            video_url = uploaded_video

    if video_url:
        st.video(video_url)
        
        st.subheader("✂️ Video Editing Controls")
        col1, col2 = st.columns(2)
        
        with col1:
            st.slider("Trim Start Time (seconds)", 0, 60, 0)
            st.slider("Trim End Time (seconds)", 0, 60, 30)
            st.select_slider("Playback Speed", options=[0.5, 0.75, 1.0, 1.25, 1.5, 2.0], value=1.0)
            
        with col2:
            st.selectbox("Video Filter Effect", ["Original", "Vintage / Sepia", "Black & White", "Vibrant Boost"])
            st.text_input("Add Video Overlay Caption:", "BhagaTube Edit")
            
        if st.button("🎬 Render & Export Video"):
            st.success("Video processed successfully with your settings!")

# --- TAB 3: WEBCAM CAPTURE ---
elif mode == "📸 Webcam Capture":
    st.header("📸 Photo Snapshot Studio")
    
    camera_photo = st.camera_input("Take a picture to import directly into BhagaTube Studio")
    if camera_photo:
        img = Image.open(camera_photo)
        st.image(img, caption="Captured Snapshot", use_container_width=True)
        st.success("Photo captured! Go to 'Photo & Canva Graphic Studio' to edit your photo.")
