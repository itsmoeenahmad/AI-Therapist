import os
import uuid
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/ask")

st.set_page_config(page_title="AI Therapist", page_icon="🧠")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🧠 AI Therapist")
st.write("Your AI mental health companion - here to listen and support you.")

st.warning(
    "⚠️ **Disclaimer:** This is an AI assistant, not a licensed therapist or doctor. "
    "For serious mental health concerns, please consult a professional."
)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("How are you feeling today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    BACKEND_URL, 
                    json={"message": user_input, "user_id": st.session_state.user_id}, 
                    timeout=60
                )
                if response.ok:
                    data = response.json()
                    reply = data.get("response", "I'm here for you.")
                else:
                    reply = "Sorry, I couldn't connect. Please try again."
            except Exception:
                reply = "Connection error. Make sure the backend is running."
            
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
