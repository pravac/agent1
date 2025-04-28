import streamlit as st
import requests, uuid, os

BASE_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:6000")
st.write("hello world")
st.write(BASE_BACKEND_URL)
CHAT_URL = f"{BASE_BACKEND_URL}/chat"
st.write(CHAT_URL)
HISTORY_URL = f"{BASE_BACKEND_URL}/history"
SESSION_RESET_URL = f"{BASE_BACKEND_URL}/reset_session"
st.write(HISTORY_URL)
st.write(SESSION_RESET_URL)

with st.sidebar:
    st.title("⚙️  Controls")
    if st.button("🗘  New chat", key="new_chat"):
        r = requests.post(
            SESSION_RESET_URL,
            json={"session_id": st.session_state["session_id"]},
        )

# ───────────────── Page title ────────────────
st.markdown(
    "<h1 style='display:flex; align-items:center;'>AI Chat Assistant 🤖</h1>",
    unsafe_allow_html=True,
)

# ───────────── Load or initialize session ────────────────
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
conversation_history = []
# Fetch existing history from backend
response = requests.get(f"{HISTORY_URL}/{st.session_state['session_id']}")
if response.status_code == 200:
    history_data = response.json()
    conversation_history = history_data.get("history", [])
prompt = st.chat_input("Type a message...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Assistant is thinking..."):
        r = requests.post(
            CHAT_URL,
            json={"session_id": st.session_state["session_id"], "prompt": prompt},
        )
        r.raise_for_status()
        answer = r.json()["response"]

    with st.chat_message("assistant"):
        st.markdown(answer)
