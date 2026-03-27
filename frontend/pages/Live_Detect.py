# import streamlit as st
# import requests
# import pandas as pd
# from db import init_db, get_db
# from logger import log_attack
# from utils import get_severity

# API_URL = "http://127.0.0.1:8000/predict/live"

# st.set_page_config("Live Network IDS", "🌐", layout="wide")
# init_db()

# st.title("🌐 Live Network Intrusion Detection")

# st.info("Captures real network traffic and detects cyber attacks in real time.")

# duration = st.slider("Capture Duration (seconds)", 2, 30, 5)

# if st.button("Start Live Detection"):
#     resp = requests.get(f"{API_URL}?duration={duration}")

#     if resp.status_code != 200:
#         st.error("Live API error")
#         st.text(resp.text)
#         st.stop()

#     try:
#         res = resp.json()
#     except:
#         st.error("Invalid backend response")
#         st.text(resp.text)
#         st.stop()

#     st.subheader("📡 Live Detection Result")
#     st.json(res)

#     # Use meta for severity logic
#     meta = res.get("meta", {})
#     features = {
#         "flow_packets_per_seconds": meta.get("pps", 0),
#         "flow_bytes_per_seconds": meta.get("bps", 0)
#     }

#     severity, reason = get_severity(res["prediction"], features)
#     log_attack("LIVE", "NETWORK", res["prediction"], severity, reason)

import streamlit as st
import requests
from db import init_db
from logger import log_attack
from utils import get_severity

API_URL = "http://127.0.0.1:8000/predict/live"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Live Network IDS",
    page_icon="🌐",
    layout="wide"
)

init_db()

# ---------------- SESSION STATE ----------------
if "live_result" not in st.session_state:
    st.session_state.live_result = None

# ---------------- PAGE UI ----------------
st.title("🌐 Live Network Intrusion Detection")
st.info("Captures real network traffic and detects cyber attacks in real time.")

duration = st.slider("Capture Duration (seconds)", 2, 30, 5)

# ==========================
# START LIVE DETECTION
# ==========================
if st.button("🚀 Start Live Detection", use_container_width=True):

    with st.spinner("Capturing live network traffic..."):
        resp = requests.get(f"{API_URL}?duration={duration}")

    if resp.status_code != 200:
        st.error("❌ Live API error")
        st.text(resp.text)
        st.stop()

    try:
        res = resp.json()
    except Exception:
        st.error("❌ Invalid backend response")
        st.text(resp.text)
        st.stop()

    # Extract meta info safely
    meta = res.get("meta", {})
    features = {
        "flow_packets_per_seconds": meta.get("pps", 0),
        "flow_bytes_per_seconds": meta.get("bps", 0)
    }

    severity, reason = get_severity(res["prediction"], features)

    # Store everything in session_state
    st.session_state.live_result = {
        "res": res,
        "severity": severity,
        "reason": reason,
        "src_ip": meta.get("src_ip", "LIVE_SOURCE"),
        "dst_ip": meta.get("dst_ip", "NETWORK")
    }

    log_attack(
        st.session_state.live_result["src_ip"],
        st.session_state.live_result["dst_ip"],
        res["prediction"],
        severity,
        reason
    )

    st.success("✅ Live detection completed")

# ==========================
# RESULT POPUPS
# ==========================
if st.session_state.live_result:

    result = st.session_state.live_result

    res = result["res"]
    severity = result["severity"]
    reason = result["reason"]
    src_ip = result.get("src_ip", "LIVE_SOURCE")
    dst_ip = result.get("dst_ip", "NETWORK")

    # -------- CRITICAL / HIGH --------
    if severity in ["CRITICAL", "HIGH"]:

        @st.dialog("🚨 CRITICAL Live Threat Detected")
        def critical_live_popup():
            st.error("A **CRITICAL live intrusion** has been detected!")
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination:** `{dst_ip}`  
            **Capture Duration:** `{duration} sec`

            **Reason:**  
            {reason}
            """)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🚫 Block IP", use_container_width=True):
                    st.success(f"IP `{src_ip}` blocked successfully")
                    st.session_state.live_result = None
                    st.stop()

            with col2:
                if st.button("Ignore", use_container_width=True):
                    st.warning("Threat ignored by user")
                    st.session_state.live_result = None
                    st.stop()

        critical_live_popup()

    # -------- MEDIUM --------
    elif severity == "MEDIUM":

        @st.dialog("⚠️ Suspicious Activity Detected")
        def medium_live_popup():
            st.warning("Suspicious network behavior detected.")
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination:** `{dst_ip}`  

            **Reason:**  
            {reason}
            """)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("👁️ Monitor IP", use_container_width=True):
                    st.info(f"IP `{src_ip}` marked for monitoring")
                    st.session_state.live_result = None
                    st.stop()

            with col2:
                if st.button("Acknowledge", use_container_width=True):
                    st.session_state.live_result = None
                    st.stop()

        medium_live_popup()

    # -------- LOW / NORMAL --------
    else:

        @st.dialog("📡 Live Traffic Analysis Result")
        def normal_live_popup():
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination:** `{dst_ip}`  
            **Capture Duration:** `{duration} sec`

            **Reason:**  
            {reason}
            """)

            if st.button("Close", use_container_width=True):
                st.session_state.live_result = None
                st.stop()

        normal_live_popup()
