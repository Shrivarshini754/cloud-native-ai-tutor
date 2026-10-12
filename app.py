import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8080")

st.set_page_config(page_title="AI Tutor", layout="wide")

# Sidebar: Cloud Infrastructure Diagnostics
with st.sidebar:
    st.markdown("### ☁️ Cloud Diagnostics")
    
    # 1. CI/CD Pipeline Status
    st.markdown("**CI/CD Pipeline**")
    st.markdown("[![Build Status](https://github.com/your-username/repo-name/actions/workflows/deploy.yml/badge.svg)](https://github.com/)")
    st.caption(f"**Git Commit:** {os.getenv('GITHUB_SHA', 'Local-Dev-Mode')[:7]}")
    st.caption(f"**Last Deployed:** {os.getenv('LAST_UPDATED', 'Pending Build')}")
    st.divider()
    
    # 2. Load Balancer & Node Health
    st.markdown("**Active Compute Node**")
    try:
        health_data = requests.get(f"{BACKEND_URL}/health", timeout=3).json()
        st.metric(label="Server Status", value=health_data["status"])
        st.caption(f"**Docker Container ID:** {health_data['compute_node_id']}")
    except Exception:
        st.error("Backend Unreachable")
    st.divider()
    
    # 3. Persistent Database (MongoDB)
    st.markdown("**Database Analytics**")
    try:
        analytics = requests.get(f"{BACKEND_URL}/analytics", timeout=3).json()
        st.metric(label="Total Queries Processed", value=analytics["total_queries"])
        if analytics["recent_activity"]:
            st.dataframe(analytics["recent_activity"], use_container_width=True)
    except Exception:
        st.warning("MongoDB cluster disconnected")

# Main Interface: AI Tutor
st.title("AI Tutor")

prompt = st.chat_input("Ask a question...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        try:
            # The Gemini model is hardcoded in the backend payload now
            res = requests.post(
                f"{BACKEND_URL}/chat", 
                json={"prompt": prompt, "model": "gemini-1.5-flash"}
            ).json()
            
            st.write(res["response"])
            
            # 4. Distributed Caching Visualizer (Redis)
            if res["cache_status"] == "hit":
                st.success(f"⚡ Cache Hit ({res['latency']:.4f}s)")
            else:
                st.info(f"🔄 Cache Miss ({res['latency']:.4f}s) - Processed by LLM")
                
        except Exception as e:
            st.error("Failed to fetch response from compute node.")