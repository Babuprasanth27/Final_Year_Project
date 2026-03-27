# # import streamlit as st

# # if "user" not in st.session_state:
# #     st.switch_page("pages/Login.py")

# # st.title("Welcome " + st.session_state.user)

# # if st.button("Manual Detection"):
# #     st.switch_page("pages/Manual_Detect.py")

# # if st.button("Live Detection"):
# #     st.switch_page("pages/Live_Detect.py")

# # if st.button("Logout"):
# #     del st.session_state.user
# #     st.switch_page("pages/Home.py")

# import streamlit as st
# import pandas as pd
# from db import get_db

# # ---------------- PAGE TITLE ----------------
# st.subheader("📊 Detection Logs")

# conn = get_db()
# df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC LIMIT 500", conn)

# # ---------------- SUMMARY METRICS ----------------
# col1, col2, col3, col4 = st.columns(4)

# col1.metric("Total Logs", len(df))
# col2.metric("Critical", len(df[df["severity"] == "CRITICAL"]))
# col3.metric("High", len(df[df["severity"] == "HIGH"]))
# col4.metric("Medium", len(df[df["severity"] == "MEDIUM"]))

# st.markdown("---")

# # ---------------- FILTERS ----------------
# with st.expander("🔍 Filter Logs"):
#     c1, c2 = st.columns(2)

#     with c1:
#         severity_filter = st.multiselect(
#             "Filter by Severity",
#             ["CRITICAL", "HIGH", "MEDIUM", "NORMAL"],
#             default=["CRITICAL", "HIGH", "MEDIUM", "NORMAL"]
#         )

#     with c2:
#         ip_search = st.text_input("Search by Source IP")

# # Apply filters
# filtered_df = df[df["severity"].isin(severity_filter)]

# if ip_search:
#     filtered_df = filtered_df[filtered_df["src_ip"].str.contains(ip_search, na=False)]

# # ---------------- SEVERITY COLORING ----------------
# def color_severity(val):
#     if val == "CRITICAL":
#         return "background-color:#fee2e2;color:#991b1b;font-weight:bold"
#     if val == "HIGH":
#         return "background-color:#ffedd5;color:#9a3412"
#     if val == "MEDIUM":
#         return "background-color:#fef9c3;color:#854d0e"
#     return "background-color:#dcfce7;color:#166534"

# # ---------------- LOG TABLE ----------------
# st.dataframe(
#     filtered_df.style.applymap(color_severity, subset=["severity"]),
#     use_container_width=True,
#     height=420
# )

# # ---------------- REFRESH BUTTON ----------------
# if st.button("🔄 Refresh Logs"):
#     st.rerun()


# # ---------------- FOOTER ----------------
# st.markdown("""
# <hr>
# <div style="text-align:center; color:#64748b; font-size:14px;">
# © 2026 Network Intrusion Detection System | Secure Monitoring Dashboard
# </div>
# """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import time
from db import get_db

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Network IDS Dashboard",
    page_icon="🚨",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "selected_log" not in st.session_state:
    st.session_state.selected_log = None

if "monitored_ips" not in st.session_state:
    st.session_state.monitored_ips = set()

# ---------------- AUTO REFRESH ----------------
with st.sidebar:
    st.header("⚙️ Controls")
    auto_refresh = st.checkbox("Auto Refresh Logs", value=False)
    refresh_interval = st.slider("Refresh interval (sec)", 5, 30, 10)

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# ---------------- LOAD LOGS ----------------
conn = get_db()
df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC LIMIT 500", conn)

# ---------------- METRICS ----------------
st.subheader("📊 Security Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Events", len(df))
c2.metric("Critical", len(df[df["severity"] == "CRITICAL"]))
c3.metric("High", len(df[df["severity"] == "HIGH"]))
c4.metric("Medium", len(df[df["severity"] == "MEDIUM"]))

st.markdown("---")

# ---------------- FILTERS ----------------
with st.expander("🔍 Filter Logs"):
    f1, f2 = st.columns(2)

    with f1:
        severity_filter = st.multiselect(
            "Severity",
            ["CRITICAL", "HIGH", "MEDIUM", "NORMAL"],
            default=["CRITICAL", "HIGH", "MEDIUM", "NORMAL"]
        )

    with f2:
        ip_filter = st.text_input("Search Source IP")

filtered_df = df[df["severity"].isin(severity_filter)]

if ip_filter:
    filtered_df = filtered_df[
        filtered_df["src_ip"].str.contains(ip_filter, na=False)
    ]

# ---------------- LOG TABLE ----------------
st.subheader("📋 Detection Logs")

def color_severity(val):
    if val == "CRITICAL":
        return "background-color:#fee2e2;color:#991b1b;font-weight:bold"
    if val == "HIGH":
        return "background-color:#ffedd5;color:#9a3412"
    if val == "MEDIUM":
        return "background-color:#fef9c3;color:#854d0e"
    return "background-color:#dcfce7;color:#166534"

st.dataframe(
    filtered_df.style.applymap(color_severity, subset=["severity"]),
    use_container_width=True,
    height=400
)

# ---------------- SELECT LOG ----------------
log_ids = filtered_df["id"].tolist()

selected_id = st.selectbox(
    "Select a log to inspect",
    options=[None] + log_ids,
    format_func=lambda x: "Select a log" if x is None else f"Log ID {x}"
)

if selected_id:
    st.session_state.selected_log = filtered_df[
        filtered_df["id"] == selected_id
    ].iloc[0]

# ---------------- LOG DETAILS POPUP ----------------
if st.session_state.selected_log is not None:
    log = st.session_state.selected_log
    severity = log["severity"]
    src_ip = log["src_ip"]
    dst_ip = log["dst_ip"]

    # ---------- CRITICAL / HIGH ----------
    if severity in ["CRITICAL", "HIGH"]:

        @st.dialog("🚨 High Risk Threat")
        def critical_popup():
            st.error("Immediate action recommended")
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{log['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  
            **Reason:** {log['reason']}
            """)

            c1, c2 = st.columns(2)

            with c1:
                if st.button("🚫 Block IP", use_container_width=True):
                    st.success(f"IP `{src_ip}` blocked")
                    st.session_state.selected_log = None
                    st.stop()

            with c2:
                if st.button("Ignore", use_container_width=True):
                    st.warning("Threat ignored")
                    st.session_state.selected_log = None
                    st.stop()

        critical_popup()

    # ---------- MEDIUM ----------
    elif severity == "MEDIUM":

        @st.dialog("⚠️ Suspicious Activity")
        def medium_popup():
            st.warning("Monitoring recommended")
            st.markdown(f"""
            **Prediction:** `{log['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  
            **Reason:** {log['reason']}
            """)

            c1, c2 = st.columns(2)

            with c1:
                if st.button("👁️ Monitor IP", use_container_width=True):
                    st.session_state.monitored_ips.add(src_ip)
                    st.info(f"IP `{src_ip}` added to monitor list")
                    st.session_state.selected_log = None
                    st.stop()

            with c2:
                if st.button("Acknowledge", use_container_width=True):
                    st.session_state.selected_log = None
                    st.stop()

        medium_popup()

    # ---------- NORMAL ----------
    else:

        @st.dialog("ℹ️ Informational Event")
        def NORMAL_popup():
            st.markdown(f"""
            **Severity:** `{severity}`  
            **Prediction:** `{log['prediction']}`  
            **Source IP:** `{src_ip}`  
            **Destination IP:** `{dst_ip}`  
            **Reason:** {log['reason']}
            """)

            if st.button("Close", use_container_width=True):
                st.session_state.selected_log = None
                st.stop()

        NORMAL_popup()

# ---------------- MONITORED IPS ----------------
if st.session_state.monitored_ips:
    st.markdown("---")
    st.subheader("👁️ Monitored IPs")

    for ip in st.session_state.monitored_ips:
        st.markdown(f"- `{ip}`")

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style="text-align:center;color:#64748b;font-size:14px;">
© 2026 Network Intrusion Detection System | SOC Dashboard
</div>
""", unsafe_allow_html=True)
