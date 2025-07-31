import streamlit as st

st.set_page_config(page_title="Mental Health AI MVP", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Login", "Chat", "Mood Tracker", "Reports"])

if page == "Login":
    st.title("Login Page")
    st.write("Placeholder for AWS Cognito Login")

elif page == "Chat":
    st.title("Chat with AI")
    st.write("Casual & Therapy Chat Placeholder")

elif page == "Mood Tracker":
    st.title("Mood Tracker")
    st.write("Calendar Visualization Placeholder")

elif page == "Reports":
    st.title("Weekly Reports")
    st.write("Reports from S3 Placeholder")