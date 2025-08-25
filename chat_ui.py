import streamlit as st
from api_utils import get_api_response

st.set_page_config(page_title="Mental Health AI Assistant", page_icon="💬")
st.title("💬 Mental Health AI Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "model" not in st.session_state:
    st.session_state.model = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

def chat_interface():
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get API response
        with st.spinner("Generating response..."):
            response = get_api_response(
                prompt, st.session_state.session_id, st.session_state.model
            )

            if response and "answer" in response:
                st.session_state.session_id = response.get("session_id")
                st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

                with st.chat_message("assistant"):
                    st.markdown(response["answer"])

                # Optional debug info
                with st.expander("Details"):
                    st.subheader("Generated Answer")
                    st.code(response["answer"])
                    st.subheader("Model Used")
                    st.code(response["model"])
                    st.subheader("Session ID")
                    st.code(response["session_id"])
            else:
                st.error("Failed to get a response from the API. Please try again.")

# Display chat interface
chat_interface()