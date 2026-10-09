import streamlit as st
import os
import requests

# Dynamically fetch the backend URL from environment variables (defaults to load_balancer for local Docker)
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://load_balancer").rstrip("/")

st.set_page_config(page_title="Cloud-Native Adaptive Language Tutor", page_icon="☁️", layout="centered")

st.title("☁️ Cloud-Native Adaptive Spanish Tutor")
st.markdown("*Architecture: Streamlit UI ➔ Nginx Load Balancer ➔ Clustered FastAPI Backends ➔ Gemini Cloud AI*")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! I am your cloud-backed Spanish tutor. Send a message to test the distributed cluster!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Routing request through cloud load balancer..."):
            try:
                # Send request to the configured backend or load balancer
                res = requests.post(f"{BACKEND_URL}/chat", json={"prompt": prompt})
                
                if res.status_code == 200:
                    data = res.json()
                    ai_reply = data["response"]
                    node_id = data["processed_by_cloud_node"]
                    
                    # Display response along with the backend node ID to prove load balancing!
                    full_output = f"{ai_reply}\n\n---\n*🧩 [Cloud Diagnostics] Handled by Backend Node: `{node_id}`*"
                    st.markdown(full_output)
                    st.session_state.messages.append({"role": "assistant", "content": full_output})
                else:
                    st.error(f"Cloud Cluster Error: {res.text}")
            except Exception as e:
                st.error(f"Failed to communicate with load balancer: {e}")