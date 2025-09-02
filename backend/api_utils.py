import requests
import streamlit as st

def get_api_response(question, session_id, model):
    data = {"question": question, "model": model}
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post("http://localhost:8000/chat", json=data, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API request failed: {str(e)}")
        return None
