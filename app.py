import streamlit as st
import requests
import uuid

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{str(uuid.uuid4())[:8]}"

def display_message():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def invoke_chat(prompt):
    data = {
        "query": prompt,
        "user_id": st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "model_name": "claude-haiku-3.5"
    }
    
    # Use Render backend API
    API_URL = "https://mhelp-ai-backend.onrender.com/chat"
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        return response.json()
    
    else:
        return None

def handle_user_input(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        result = invoke_chat(prompt)
        
        if result:
            ai_response = result["response"]
            st.markdown(ai_response)
            
            st.session_state.session_id = result["session_id"]
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

        else:
            st.error("Error calling API")

def main():
    st.title("Mental Health AI Assistant")
    initialize_state()
    
    display_message()

    if prompt := st.chat_input("Type your message..."):
        handle_user_input(prompt)

if __name__ == "__main__":
    main()
