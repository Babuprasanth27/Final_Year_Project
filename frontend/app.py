import streamlit as st
from auth import init_users
init_users()

if "user" not in st.session_state:
    st.switch_page("pages/Home.py")
else:
    st.switch_page("pages/dashboard.py")
