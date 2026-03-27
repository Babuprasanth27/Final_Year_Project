import streamlit as st

def show():
    st.markdown(
        "<h1 style='text-align:center;'>Hybrid Network Intrusion Detection System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "A hybrid ML & DL based system for detecting and preventing "
        "network attacks in real time."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Start Detecting", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()
