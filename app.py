import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Dr. Aquib JAT AI", page_icon="🤖")

st.title("🤖 Dr. Aquib JAT AI")
st.sidebar.info("Developed by: Dr. Md Aquib")

# AI Setup
# Maine model name update kar diya hai
api_key = "AIzaSyDNPvHtbFLj04VJkFWzSv9BJ0fcp7blzB4"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- VOICE SEARCH SECTION ---
st.write("🎤 Bol kar command dein:")
audio = mic_recorder(start_prompt="Recording shuru karein", stop_prompt="Stop karein", key='recorder')

user_input = st.chat_input("Ya phir yahan type karein...")

# Agar voice recording milti hai
if audio:
    prompt = audio['text']
else:
    prompt = user_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_prompt = f"Tum Dr. Aquib JAT AI ho, jise Dr. Md Aquib ne banaya hai. Answer this: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Opps! Ek error aaya hai. Shayad API key active nahi hai. Error: {e}")
