import streamlit as st
from auth import signup

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Signup | Network IDS",
    page_icon="🚨",
    layout="centered"
)

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>

/* ---- PAGE BACKGROUND ---- */
html, body, [data-testid="stApp"] {
    background-color: #f8fafc;
}

/* ---- SIGNUP CARD ---- */
.signup-container {
    max-width: 440px;
    margin: 10px auto;
    background: #ffffff;
    padding: 42px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

/* ---- HEADINGS ---- */
.signup-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
}
.signup-subtitle {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 28px;
}

/* ---- INPUT LABELS ---- */
label {
    font-weight: 600;
    color: #334155 !important;
}

/* ---- INPUT FIELDS ---- */
input {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 10px !important;
}

/* ---- SIGNUP BUTTON ---- */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px;
    border: none;
    margin-top: 22px;
}

/* ---- FOOTER ---- */
.signup-footer {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIGNUP CARD ----------------
st.markdown("""
<div class="signup-container">
    <div class="signup-title"> Create an Account</div>
    <div class="signup-subtitle">
        Get started with the Network Intrusion Detection System
    </div>
""", unsafe_allow_html=True)

# ---------------- SIGNUP FORM ----------------
u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Create Account"):
    if signup(u, p):
        st.success("Account created successfully")
        st.switch_page("pages/Dashboard.py")
    else:
        st.error("Username already exists")

st.markdown("""
    <div class="signup-footer">
        © 2026 Network IDS | Secure Signup
    </div>
</div>
""", unsafe_allow_html=True)
