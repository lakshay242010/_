import os
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="Bhagat GPT | Bhagat Industries",
    page_icon="📚",
    layout="centered",
)

# App Header & Branding
st.markdown(
    "<h1 style='text-align: center; color: #1f77b4;'>📚 Bhagat GPT</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>Created by <b>Lakshay</b> | Powered by <b>Bhagat Industries</b></p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Sidebar for Settings & Scope Info
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Enter Google Gemini API Key:", type="password"
    )

    st.markdown("---")
    st.subheader("🎯 Scope & Guidelines")
    st.markdown("""
    * **Target Audience:** Class 8, 9, & 10 Students
    * **Subjects:** Science, Mathematics, Social Science, English, etc.
    * **Content:** NCERT solutions, concept explanations, and exam prep.
    """)

# Check for API Key
if not api_key_input:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.warning(
            "⚠️ Please enter your Gemini API Key in the sidebar or configure it in Streamlit Secrets to start chatting."
        )
        st.stop()
else:
    api_key = api_key_input

# Initialize the Google GenAI Client
client = genai.Client(api_key=api_key)

# Strict System Instruction
system_instruction = (
    "You are Bhagat GPT, an elite educational AI assistant created by Lakshay under Bhagat Industries. "
    "Your sole purpose is to help Class VIII, IX, and X students with their studies, including NCERT solutions, "
    "concept explanations, homework help, and exam preparation. "
    "CRITICAL RULE: If a user asks questions outside the Class 8-10 school curriculum, general non-educational queries, "
    "or anything inappropriate, politely decline and remind them that you are strictly designed for Class 8-10 academic support. "
    "Keep explanations clear, structured, encouraging, and easy to understand for teenagers."
)

# Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Handling
if prompt := st.chat_input(
    "Ask a Class 8-10 concept, NCERT doubt, or exam question..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            formatted_contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=m["content"])],
                    )
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=formatted_contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                ),
            )

            bot_response = response.text
            message_placeholder.markdown(bot_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": bot_response}
            )

        except Exception as e:
            error_msg = f"An error occurred: {e}"
            message_placeholder.markdown(error_msg)
