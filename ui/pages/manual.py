import streamlit as st
import requests
from db.database import get_db
from utils.severity import get_severity

API_URL = "http://127.0.0.1:8000/predict/manual"

def show():
    st.title("🧪 Manual Traffic Detection")

    # Manual input form
    with st.form("manual_form"):
        col1, col2 = st.columns(2)

        with col1:
            src_ip = st.text_input("Source IP", "192.168.1.10")
            dst_ip = st.text_input("Destination IP", "192.168.1.1")
            protocol = st.number_input("Protocol", 0, 255, 17)
            flow_duration = st.number_input("Flow Duration (sec)", 0.0)

        with col2:
            fwd = st.number_input("Forward Packets", 0)
            bwd = st.number_input("Backward Packets", 0)
            fwd_len = st.number_input("Forward Bytes", 0.0)
            bwd_len = st.number_input("Backward Bytes", 0.0)

        run = st.form_submit_button("🚀 Run Detection")

    if run:
        payload = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "flow_duration": flow_duration,
            "total_forward_packets": fwd,
            "total_backward_packets": bwd,
            "total_forward_packets_length": fwd_len,
            "total_backward_packets_length": bwd_len
        }

        try:
            resp = requests.post(API_URL, json=payload)
            resp.raise_for_status()
            res = resp.json()
        except Exception as e:
            st.error(f"API request failed: {e}")
            return

        severity, reason = get_severity(res["prediction"], payload)

        # Save log to SQLite
        conn = get_db()
        conn.execute(
            "INSERT INTO logs (src_ip, dst_ip, attack_type, severity, reason) VALUES (?,?,?,?,?)",
            (src_ip, dst_ip, res["prediction"], severity, reason)
        )
        conn.commit()

        # Store last attack for dashboard or notification
        st.session_state.last_attack = {
            "ip": src_ip,
            "severity": severity
        }

        st.success(f"Detection Complete! Severity: {severity}")
        st.session_state.page = "dashboar_
