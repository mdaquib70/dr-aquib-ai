import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Dr. Aquib JAT AI", page_icon="🤖")

st.title("🤖 Dr. Aquib JAT AI")
st.sidebar.info("Developed by: Dr. Md Aquib")

# AI Setup (Secrets se key uthayega)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Sabse stable model use kar rahe hain
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets mein API Key nahi mili. Please check Streamlit settings.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("🎤 Bol kar command dein:")
audio = mic_recorder(start_prompt="Recording shuru karein", stop_prompt="Stop karein", key='recorder')

user_input = st.chat_input("Ya phir yahan type karein...")

prompt = None
if audio and audio.get('text'):
    prompt = audio['text']
elif user_input:
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
            st.error(f"Opps! Kuch error aa gaya. Check API key ya model. Error: {e}")
            
