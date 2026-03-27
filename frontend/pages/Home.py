import streamlit as st
from db import init_db, get_db
import requests
import pandas as pd
from logger import log_attack
from utils import get_severity
# ---------------- AUTH CHECK ----------------
if "user" not in st.session_state:
    st.switch_page("pages/Login.py")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Dashboard | Network IDS",
    page_icon="🚨",
    layout="wide"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>

/* ---- GLOBAL ---- */
html, body, [data-testid="stApp"] {
    background-color: #f8fafc;
    font-family: "Segoe UI", system-ui;
}

/* ---- HEADER ---- */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 60px;
    border-bottom: 1px solid #e5e7eb;
    background: #ffffff;
}
.header h1 {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
}
.header span {
    color: #2563eb;
}

/* ---- HERO ---- */
.hero {
    padding: 50px 60px;
}
.hero h2 {
    font-size: 34px;
    font-weight: 800;
    color: #0f172a;
}
.hero p {
    font-size: 18px;
    color: #475569;
    max-width: 900px;
    line-height: 1.7;
}

/* ---- CARDS ---- */
.section {
    padding: 20px 60px 60px;
}
.card {
    background: #ffffff;
    padding: 36px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    height: 100%;
}
.card h3 {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
}
.card p {
    color: #475569;
    font-size: 16px;
    line-height: 1.6;
}

/* ---- BUTTONS ---- */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 600;
    border-radius: 14px;
    padding: 14px;
    border: none;
    margin-top: 20px;
}

/* ---- LOGOUT BUTTON ---- */
.logout button {
    background: #fee2e2 !important;
    color: #991b1b !important;
}

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    color: #94a3b8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(f"""
<div class="header">
    <h1>🚨 Network IDS Dashboard</h1>
    <div>Welcome, <span>{st.session_state.user}</span></div>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO (UPDATED CONTENT) ----------------
st.markdown("""
<div class="hero">
    <h2>Security Monitoring Console</h2>
    <p>
        This dashboard acts as the central control panel for the Network Intrusion
        Detection System. It enables security analysts to monitor network activity,
        analyze suspicious traffic, and respond to potential threats efficiently.
        The system supports both manual packet inspection and live traffic monitoring
        to ensure comprehensive network protection.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- ACTION CARDS ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    # Open the card
    st.markdown("""
    <style>
    .ids-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }
    .ids-card h3 {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .ids-card p {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 24px;
    }
    </style>

    <div class="ids-card">
        <h3>📥 Manual Detection</h3>
        <p>
            Upload or enter network traffic details manually to inspect packets,
            analyze behavior, and identify potential intrusions using detection logic.
        </p>
    """, unsafe_allow_html=True)

    # Button is NOW INSIDE the card
    if st.button("Start Manual Detection", key="manual_detect"):
        st.switch_page("pages/Manual_Detect.py")

    # Close the card
    st.markdown("</div>", unsafe_allow_html=True)


with c2:
    st.markdown("""
    <style>
    .ids-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }
    .ids-card h3 {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .ids-card p {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    </style>
    <div class="card">
        <h3>📡 Live Detection</h3>
        <p>
            Monitor real-time network traffic continuously to detect malicious
            activities as they occur and respond immediately to threats.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Live Detection"):
        st.switch_page("pages/Live_Detect.py")

with c3:
    # Open card
    st.markdown("""
   <style>
    .ids-card {
        background: #ffffff;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }
    .ids-card h3 {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .ids-card-p {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 44px;
    }
    </style>
    <div class="card">
        <h3>🔐 Logout</h3>
        <p class="ids-card-p">
            Securely end your session and log out of the dashboard to
            prevent unauthorized access to the system.
        </p>
    """, unsafe_allow_html=True)

    # Button INSIDE the card
    if st.button("Logout", key="logout"):
        del st.session_state.user
        st.switch_page("pages/Home.py")

    # Attach CSS class to button via JS-free trick
    st.markdown("""
    <script>
    const btn = window.parent.document.querySelector(
        'button[kind="secondary"]'
    );
    if (btn) btn.classList.add('logout-btn');
    </script>
    """, unsafe_allow_html=True)

    # Close card
    st.markdown("</div>", unsafe_allow_html=True)

