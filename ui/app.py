import streamlit as st
from db.database import init_db
from pages import hero, signup, login, home, manual, dashboard

st.set_page_config("Network IDS", "🚨", layout="wide")
init_db()

# Session defaults
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("page", "hero")

PUBLIC_PAGES = ["hero", "signup", "login"]

# 🔐 AUTH CHECK (GLOBAL)
if not st.session_state.logged_in and st.session_state.page not in PUBLIC_PAGES:
    st.session_state.page = "login"
    st.rerun()

# ROUTER
if st.session_state.page == "hero":
    hero.show()
elif st.session_state.page == "signup":
    signup.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "home":
    home.show()
elif st.session_state.page == "manual":
    manual.show()
elif st.session_state.page == "dashboard":
    dashboard.show()
