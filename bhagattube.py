import streamlit as st

# Page configuration
st.set_page_config(page_title="MiniTube", page_icon="📺", layout="wide")

st.title("📺 MiniTube App")
st.write("Welcome to your custom video streaming app built with Streamlit!")

# Dictionary of sample videos (Title -> YouTube URL)
videos = {
    "Python Streamlit Tutorial": "https://www.youtube.com/watch?v=owUSRrLkCdA",
    "Lo-Fi Beats to Relax/Study to": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
    "Build a Web App Fast": "https://www.youtube.com/watch?v=ZZ5LpwO-An4"
}

# Sidebar for video selection
st.sidebar.header("Navigation")
selected_video_title = st.sidebar.selectbox("Choose a video:", list(videos.keys()))

# Get the selected URL
video_url = videos[selected_video_title]

# Main layout: Video player and comments side-by-side
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(selected_video_title)
    # Embed the video using Streamlit's built-in video player
    st.video(video_url)

with col2:
    st.subheader("💬 Comments")
    
    # Simple comment section state
    if "comments" not in st.session_state:
        st.session_state.comments = ["Awesome app!", "Cool video choice!"]
        
    # Input for new comment
    new_comment = st.text_input("Add a public comment:")
    if st.button("Post"):
        if new_comment:
            st.session_state.comments.append(new_comment)
            st.success("Comment posted!")
            
    # Display comments
    for comment in reversed(st.session_state.comments):
        st.info(comment)
