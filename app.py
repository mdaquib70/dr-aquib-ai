import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import os

# Page config
st.set_page_config(page_title="Dr. Aquib AI", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Dr. Aquib JAT AI")
st.caption("Smart AI Assistant | Voice + Chat")

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Developed by Md Aquib")

# Secure API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ API Key not found. Please add in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Model (latest working)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Voice input
st.subheader("🎤 Voice Command")
audio = mic_recorder(
    start_prompt="▶️ Start Recording",
    stop_prompt="⏹️ Stop",
    key="recorder"
)

# Text input
user_input = st.chat_input("Type your message...")

# Decide input
prompt = None
if audio and audio.get("text"):
    prompt = audio["text"]
elif user_input:
    prompt = user_input

# Process input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                full_prompt = f"""
You are Dr. Aquib JAT AI.
Answer in simple English + Hindi mix.
Keep answer short and clear.

User: {prompt}
"""

                response = model.generate_content(full_prompt)

                reply = response.text if hasattr(response, "text") else "No response"

                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")
