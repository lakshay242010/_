import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(
    page_title="Bhagat GPT - Smart AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom Styling for Light Theme & Clean Chat UI
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F5F7;
        color: #0E1318;
    }
    .main-header {
        font-size: 36px;
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🤖 Bhagat GPT</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Your personal AI assistant, ready to answer any question!</div>", unsafe_allow_html=True)

# Sidebar for API Key configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get a free API key from Google AI Studio](https://aistudio.google.com/)")
    st.write("---")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am Bhagat GPT. How can I help you today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask Bhagat GPT anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not api_key:
            response_text = "⚠️ Please enter your Google Gemini API key in the sidebar to start chatting with Bhagat GPT!"
            message_placeholder.markdown(response_text)
        else:
            try:
                # Configure Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generate response from Gemini
                response = model.generate_content(prompt)
                response_text = response.text
                message_placeholder.markdown(response_text)
            except Exception as e:
                response_text = f"An error occurred: {e}"
                message_placeholder.markdown(response_text)
                
        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
