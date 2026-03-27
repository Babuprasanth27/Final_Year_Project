import streamlit as st
from db.database import get_db

def show():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db()
        cur = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        if cur.fetchone():
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
