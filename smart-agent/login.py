import streamlit as st

users = {
    "anoushaa": "ai123",
    "admin": "1234"
}

def login_page():
    st.title("🔐 Login to Anoushaa AI")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")
