import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="BhagatGPT v1.0",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 BhagatGPT v1.0")
st.caption("Powered by high-speed open LLM streaming API")

# Sidebar for API Key Input
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.markdown("[Get a free Groq API Key](https://console.groq.com)")

if not api_key:
    st.info("Please enter your API Key in the sidebar to begin chatting.", icon="🔑")
    st.stop()

# Initialize API client
client = Groq(api_key=api_key)

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are BhagatGPT v1.0, a helpful, intelligent, and accurate AI assistant."}
    ]

# Display Existing Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Process User Input & Stream Response
if prompt := st.chat_input("Ask BhagatGPT anything..."):
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream Assistant Output
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=0.7,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"An error occurred: {e}"
            message_placeholder.markdown(full_response)

    # Append response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
