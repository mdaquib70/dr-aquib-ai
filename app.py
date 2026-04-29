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

# ✅ Secure API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# ✅ Latest working model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎤 Voice input
st.write("🎤 Bol kar ya type karke puchiye:")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="recorder"
)

user_input = st.chat_input("Type your question...")

# Decide input
prompt = None
if audio and audio.get("text"):
    prompt = audio["text"]
elif user_input:
    prompt = user_input

# If user asks something
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🤔 Soch raha hoon..."):
                
                # ✅ Hindi + English mix instruction
                full_prompt = f"""
                Tum ek helpful AI ho. Hindi aur simple English mix me answer do.
                Easy language use karo.
                Question: {prompt}
                """

                response = model.generate_content(full_prompt)

                reply = response.text if hasattr(response, "text") else "No response"

                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

        except Exception as e:
            st.error("⚠️ Kuch error aa gaya. Check API key ya model.")
            st.write(e)
