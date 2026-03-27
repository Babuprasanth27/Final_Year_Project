# import streamlit as st
# from auth import login

# st.title("Login")

# u = st.text_input("Username")
# p = st.text_input("Password", type="password")

# if st.button("Login"):
#     if login(u,p):
#         st.session_state.user = u
#         st.success("Login successful")
#         st.switch_page("pages/Dashboard.py")
#     else:
#         st.error("Invalid credentials")
import streamlit as st
from auth import login

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Login | Network IDS",
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

/* ---- CENTER CARD ---- */
.login-container {
    max-width: 420px;
    margin: 12px auto;
    background: #ffffff;
    padding: 40px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

/* ---- HEADINGS ---- */
.login-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 8px;
}
.login-subtitle {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 30px;
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

/* ---- LOGIN BUTTON ---- */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px;
    border: none;
    margin-top: 20px;
}

/* ---- FOOTER ---- */
.login-footer {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN CARD ----------------
st.markdown("""
<div class="login-container">
    <div class="login-title">🚨 Network IDS Login</div>
    <div class="login-subtitle">
        Secure access to the Network Intrusion Detection Dashboard
    </div>
""", unsafe_allow_html=True)

# ---------------- LOGIN FORM ----------------
u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Login"):
    if login(u, p):
        st.session_state.user = u
        st.success("Login successful")
        st.switch_page("pages/Home.py")
    else:
        st.error("Invalid username or password")

st.markdown("""
    <div class="login-footer">
        © 2026 Network IDS | Authorized Access Only
    </div>
</div>
""", unsafe_allow_html=True)
