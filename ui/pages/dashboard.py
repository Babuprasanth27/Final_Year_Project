import streamlit as st
import pandas as pd
from db.database import get_db
from services.block_ip import block_ip

def show():
    st.title("📊 Security Dashboard")

    conn = get_db()
    df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC", conn)

    st.dataframe(df, use_container_width=True)

    attack = st.session_state.get("last_attack")

    if attack and attack["severity"] in ["HIGH", "CRITICAL"]:
        st.error("🚨 Severe Attack Detected")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Block Attacker IP"):
                block_ip(attack["ip"])
                st.success(f"IP {attack['ip']} blocked successfully")

        with col2:
            st.button("Ignore")
