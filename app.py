import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import os

st.set_page_config(page_title="Dr. Aquib JAT AI", page_icon="🤖")

st.title("🤖 Dr. Aquib JAT AI")
st.caption("Hindi + English AI Assistant")

# API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ NEW METHOD (important)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# voice
audio = mic_recorder(start_prompt="🎙️ Start", stop_prompt="⏹️ Stop")

user_input = st.chat_input("Type here...")

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
