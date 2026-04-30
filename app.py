import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import os

# Page setup
st.set_page_config(page_title="Dr. Aquib JAT AI", page_icon="🤖")

st.title("🤖 Dr. Aquib JAT AI")
st.caption("Hindi + English AI Assistant")

# Sidebar
st.sidebar.info("Developed by: Dr. Md Aquib")

# API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY")

# ✅ Correct model (AI Studio compatible)
model = genai.GenerativeModel("gemini-1.5-flash")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Voice input
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording")

user_input = st.chat_input("Type your question...")

prompt = None
if audio and audio.get("text"):
    prompt = audio["text"]
elif user_input:
    prompt = user_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🤔 Soch raha hoon..."):

                response = model.generate_content(
                    f"Answer in Hindi + simple English: {prompt}"
                )

                reply = response.text
                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

        except Exception as e:
            st.error(f"Error: {e}")
