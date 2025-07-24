import streamlit as st
import requests
import json
import os

# Constants
MODEL_NAME = "llama3.2:3b"
HISTORY_FILE = "chat_history.json"

# Load chat history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save chat history to file
def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f)

# Clear chat history
def reset_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.session_state.messages = []

# Setup session
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.set_page_config(page_title="🦙 Llama 3.2 Chat", layout="wide")
st.title("🦙 Chat with Llama 3.2 (3B)")
st.markdown("AI Powered Chatbot by Haris")

# Sidebar: Reset button and conversation history
with st.sidebar:
    st.header("🧾 Conversation History")
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            short = msg["content"][:40] + ("..." if len(msg["content"]) > 40 else "")
            st.markdown(f"**{role.title()} {i+1}:** {short}")
    else:
        st.info("No messages yet.")

    if st.button("🔁 Reset Conversation"):
        reset_history()
        st.experimental_rerun()

# Display messages in main chat area
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your message...")

# On submit
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": MODEL_NAME,
                        "prompt": user_input,
                        "stream": False
                    }
                )
                reply = response.json()["response"]
            except Exception as e:
                reply = f"⚠️ Error: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_history(st.session_state.messages)
