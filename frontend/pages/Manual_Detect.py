import streamlit as st
import requests
import os
from db import init_db
from logger import log_attack
from utils import get_severity
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

MANUAL_API = f"{BASE_URL}/predict/manual"


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Network IDS Dashboard",
    page_icon="🚨",
    layout="wide"
)

init_db()

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = None

if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False

# ==========================
# MANUAL DETECTION PANEL
# ==========================
st.markdown("## 🧪 Manual Traffic Analysis")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔗 Connection Details")
        src_ip = st.text_input("Source IP", "192.168.1.10")
        dst_ip = st.text_input("Destination IP", "192.168.1.1")
        protocol = st.number_input("Protocol", 0, 255, 17)
        flow_duration = st.number_input("Flow Duration (sec)", 0.0)

    with col2:
        st.subheader("📦 Packet Statistics")
        fwd = st.number_input("Forward Packets", 0)
        bwd = st.number_input("Backward Packets", 0)
        fwd_len = st.number_input("Forward Bytes", 0.0)
        bwd_len = st.number_input("Backward Bytes", 0.0)

with st.container():
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📊 Traffic Metrics")
        fwd_mean = st.number_input("Forward Mean Bytes", 0.0)
        bwd_mean = st.number_input("Backward Mean Bytes", 0.0)
        fwd_pps = st.number_input("Forward PPS", 0.0)
        bwd_pps = st.number_input("Backward PPS", 0.0)

    with col4:
        st.subheader("⏱ Timing Metrics")
        fwd_iat = st.number_input("Forward IAT Mean", 0.0)
        bwd_iat = st.number_input("Backward IAT Mean", 0.0)
        flow_iat = st.number_input("Flow IAT Mean", 0.0)
        flow_pps = st.number_input("Flow PPS", 0.0)
        flow_bps = st.number_input("Flow BPS", 0.0)

st.markdown("---")

# ==========================
# RUN DETECTION
# ==========================
if st.button("🚀 Run Detection", use_container_width=True):

    payload = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol": protocol,
        "flow_duration": flow_duration,
        "total_forward_packets": fwd,
        "total_backward_packets": bwd,
        "total_forward_packets_length": fwd_len,
        "total_backward_packets_length": bwd_len,
        "forward_packet_length_mean": fwd_mean,
        "backward_packet_length_mean": bwd_mean,
        "forward_packets_per_second": fwd_pps,
        "backward_packets_per_second": bwd_pps,
        "forward_iat_mean": fwd_iat,
        "backward_iat_mean": bwd_iat,
        "flow_iat_mean": flow_iat,
        "flow_packets_per_seconds": flow_pps,
        "flow_bytes_per_seconds": flow_bps
    }

    with st.spinner("Analyzing traffic..."):
        resp = requests.post(MANUAL_API, json=payload)

    if resp.status_code != 200:
        st.error("❌ Backend API error")
        st.text(resp.text)
        st.stop()

    try:
        res = resp.json()
    except Exception:
        st.error("❌ Invalid backend response")
        st.text(resp.text)
        st.stop()

    severity, reason = get_severity(res["prediction"], payload)

    st.session_state.result = {
        "res": res,
        "severity": severity,
        "reason": reason,
        "src_ip": src_ip,
        "dst_ip": dst_ip
    }

    st.session_state.show_dialog = True

    log_attack(src_ip, dst_ip, res["prediction"], severity, reason)
    st.rerun()

# ==========================
# RESULT DIALOGS
# ==========================
if st.session_state.show_dialog and st.session_state.result:

    r = st.session_state.result
    res = r["res"]
    severity = r["severity"]
    reason = r["reason"]
    src_ip = r["src_ip"]
    dst_ip = r["dst_ip"]

    # -------- CRITICAL / HIGH --------
    if severity in ["CRITICAL", "HIGH"]:

        @st.dialog("🚨 High Risk Threat Detected")
        def critical_popup():
            st.error("Immediate action required")
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  

            **Reason:**  
            {reason}
            """)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🚫 Block IP", key="block"):
                    st.success(f"IP `{src_ip}` blocked")
                    st.session_state.result = None
                    st.session_state.show_dialog = False
                    st.rerun()

            with col2:
                if st.button("Ignore", key="ignore"):
                    st.session_state.result = None
                    st.session_state.show_dialog = False
                    st.rerun()

        critical_popup()

    # -------- MEDIUM --------
    elif severity == "MEDIUM":

        @st.dialog("⚠️ Suspicious Activity Detected")
        def medium_popup():
            st.warning("Suspicious behavior observed. Monitoring advised.")
            st.markdown(f"""
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  

            **Reason:**  
            {reason}
            """)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("👁️ Monitor IP", key="monitor"):
                    st.info(f"IP `{src_ip}` marked for monitoring")
                    st.session_state.result = None
                    st.session_state.show_dialog = False
                    st.rerun()

            with col2:
                if st.button("Acknowledge", key="ack"):
                    st.session_state.result = None
                    st.session_state.show_dialog = False
                    st.rerun()

        medium_popup()

    # -------- LOW / NORMAL --------
    else:

        @st.dialog("ℹ️ Traffic Analysis Result")
        def normal_popup():
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{res['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  

            **Reason:**  
            {reason}
            """)

            if st.button("Close", key="close"):
                st.session_state.result = None
                st.session_state.show_dialog = False
                st.rerun()

        normal_popup()


# ==========================
# LOGS TABLE
# ==========================
# st.markdown("---")
# st.subheader("📊 Detection Logs")

# conn = get_db()
# df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC LIMIT 100", conn)

# def color_severity(val):
#     if val == "CRITICAL":
#         return "background-color:#ff4d4d;color:white"
#     if val == "HIGH":
#         return "background-color:#ff944d"
#     if val == "MEDIUM":
#         return "background-color:#ffd11a"
#     return "background-color:#a6ff4d"

# if not df.empty:
#     st.dataframe(
#         df.style.applymap(color_severity, subset=["severity"]),
#         use_container_width=True
#     )
# else:
#     st.info("No detection logs available yet.")
