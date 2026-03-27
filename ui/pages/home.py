import streamlit as st

def show():
    st.sidebar.title("🔐 Network IDS")

    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()

    if st.sidebar.button("🧪 Manual Detection"):
        st.session_state.page = "manual"
        st.rerun()

    if st.sidebar.button("📊 Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "hero"
        st.rerun()

    st.title("🏠 Home")
    st.success("Welcome! All pages are accessible.")
