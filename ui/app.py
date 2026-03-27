import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Legal AI Assistant", layout="wide")

st.title("⚖️ Indian Legal AI Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
query = st.chat_input("Ask your legal question...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Call backend API
    response = requests.post(API_URL, params={"query": query})

    if response.status_code == 200:
        answer = response.json()["answer"]
    else:
        answer = "Error connecting to backend."

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])