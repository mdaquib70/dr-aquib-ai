import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Dr. Aquib JAT AI", page_icon="🤖")

# Interface ko thoda aur sundar banaya
st.title("🤖 Dr. Aquib JAT AI")
st.markdown("---")
st.sidebar.info("Developed by: Dr. Md Aquib")

# AI Setup
api_key = "AIzaSyC2Myp0FM1GcK7o8hLRfIcJusUT8S96nV4"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Puchiye, main aapki kya madad kar sakta hoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # AI ko instructions taaki wo aapke Assistant ki tarah behave kare
        system_instruction = f"Tum Dr. Aquib JAT AI ho, jise Dr. Md Aquib ne banaya hai. Tumhe hamesha helpful aur intelligent answers dene hain. User ka sawal: {prompt}"
        
        response = model.generate_content(system_instruction)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
      
