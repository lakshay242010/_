import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

# 1. Page Configuration
st.set_page_config(
    page_title="BhagaTube",
    page_icon="🔴",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #FF0000; }
    .sub-text { font-size: 16px; color: #888888; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-title'>🔴 BhagaTube Studio & Video Hub</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Watch videos, upload content, and edit thumbnails!</div><br>", unsafe_allow_html=True)

# Initialize Session State
if "videos" not in st.session_state:
    st.session_state.videos = [
        {
            "id": 1,
            "title": "Big Buck Bunny - Animated Classic",
            "url": "https://www.w3schools.com/html/mov_bbb.mp4",
            "uploader": "BhagaTube Official",
            "likes": 12,
            "comments": ["Awesome quality!", "Love this clip!"]
        },
        {
            "id": 2,
            "title": "Streamlit Web Dev Tutorial",
            "url": "https://www.youtube.com/watch?v=owUSRrLkCdA",
            "uploader": "TechCreator",
            "likes": 45,
            "comments": ["Super helpful tutorial."]
        }
    ]

# Sidebar Navigation
mode = st.sidebar.radio("Navigation", ["📺 Watch Videos", "📸 Thumbnail Creator & Camera", "📤 Upload Video"])

# --- TAB 1: WATCH VIDEOS ---
if mode == "📺 Watch Videos":
    search_query = st.sidebar.text_input("🔍 Search BhagaTube:")
    
    filtered_videos = [
        v for v in st.session_state.videos 
        if search_query.lower() in v["title"].lower()
    ]

    if not filtered_videos:
        st.warning("No videos found matching your search.")
    else:
        for idx, video in enumerate(filtered_videos):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(video["title"])
                st.caption(f"Uploaded by: {video['uploader']}")
                st.video(video["url"])
                
                # Likes button
                if st.button(f"👍 Like ({video['likes']})", key=f"like_{idx}"):
                    video["likes"] += 1
                    st.rerun()

            with col2:
                st.write("### 💬 Comments")
                new_comment = st.text_input("Add a comment:", key=f"input_{idx}")
                if st.button("Post", key=f"post_{idx}"):
                    if new_comment:
                        video["comments"].append(new_comment)
                        st.success("Comment added!")
                        st.rerun()

                for c in reversed(video["comments"]):
                    st.info(c)
            st.divider()

# --- TAB 2: CAMERA & PHOTO EDITOR ---
elif mode == "📸 Thumbnail Creator & Camera":
    st.header("📸 Photo Studio & Thumbnail Editor")
    
    option = st.radio("Choose Image Source:", ["Take Photo with Camera", "Upload Image File"])
    img = None
    
    if option == "Take Photo with Camera":
        camera_photo = st.camera_input("Take a photo for your thumbnail")
        if camera_photo:
            img = Image.open(camera_photo)
    else:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            
    if img:
        st.write("### 🎨 Edit Your Image")
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Original Image", use_container_width=True)
            
        # Filters & Adjustments
        filter_type = st.selectbox("Apply Filter", ["None", "Grayscale", "Blur", "Contour", "Detail"])
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
        
        # Process image
        processed_img = img.copy()
        
        if filter_type == "Grayscale":
            processed_img = processed_img.convert("L")
        elif filter_type == "Blur":
            processed_img = processed_img.filter(ImageFilter.BLUR)
        elif filter_type == "Contour":
            processed_img = processed_img.filter(ImageFilter.CONTOUR)
        elif filter_type == "Detail":
            processed_img = processed_img.filter(ImageFilter.DETAIL)
            
        enhancer = ImageEnhance.Brightness(processed_img)
        processed_img = enhancer.enhance(brightness)
        
        enhancer = ImageEnhance.Contrast(processed_img)
        processed_img = enhancer.enhance(contrast)
        
        with col2:
            st.image(processed_img, caption="Edited Result", use_container_width=True)

# --- TAB 3: UPLOAD VIDEO ---
elif mode == "📤 Upload Video":
    st.header("📤 Post a New Video to BhagaTube")
    
    title = st.text_input("Video Title:")
    uploader = st.text_input("Your Channel Name:")
    video_link = st.text_input("Video URL (YouTube or Direct MP4 Link):")
    
    if st.button("Publish Video"):
        if title and uploader and video_link:
            new_video = {
                "id": len(st.session_state.videos) + 1,
                "title": title,
                "url": video_link,
                "uploader": uploader,
                "likes": 0,
                "comments": []
            }
            st.session_state.videos.append(new_video)
            st.success("Video published successfully! Go to 'Watch Videos' tab to view it.")
        else:
            st.error("Please fill in all fields.")
