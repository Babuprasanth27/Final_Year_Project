import streamlit as st
from db.database import get_db

def show():
    st.title("📝 Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if not username or not password:
            st.warning("Please fill all fields")
            return

        conn = get_db()

        # Check if user already exists
        cur = conn.execute(
            "SELECT id FROM users WHERE username=?",
            (username,)
        )

        if cur.fetchone():
            st.warning("Account already exists. Please login.")
            st.session_state.page = "login"
            st.rerun()

        # Create new user
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

        # AUTO LOGIN FOR NEW USER
        st.session_state.logged_in = True
        st.session_state.page = "home"

        st.success("Account created successfully!")
        st.rerun()
