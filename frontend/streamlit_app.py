import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Network IDS",
    page_icon="",
    layout="wide"
)

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>

/* ---- GLOBAL BACKGROUND ---- */
html, body, [data-testid="stApp"] {
    background-color: #ffffff;
}

/* ---- BASE TEXT ---- */
* {
    color: #111827;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont;
}

/* ---- HERO SECTION ---- */
.hero {
    padding: 0px 60px;
    background: linear-gradient(180deg, #f8fafc, #ffffff);
    border-bottom: 1px solid #e5e7eb;
}
.hero h1 {
    font-size: 56px;
    font-weight: 800;
    color: #0f172a;
}
.hero p {
    font-size: 20px;
    color: #475569;
    max-width: 760px;
    line-height: 1.6;
}

/* ---- SECTIONS ---- */
.section {
    padding: 70px 60px;
}

/* ---- CARDS ---- */
.card {
    background: #ffffff;
    padding: 32px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    height: 100%;
}
.card h3, .card h2 {
    color: #0f172a;
}
.card p {
    color: #475569;
    font-size: 16px;
    line-height: 1.6;
}

/* ---- TAGS ---- */
.tag {
    display: inline-block;
    background: #f1f5f9;
    color: #2563eb;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 13px;
    margin-right: 10px;
    margin-top: 12px;
}

/* ---- BUTTONS ---- */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: #ffffff;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 12px 24px;
}

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    color: #64748b;
    padding: 50px 0 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <h1> Network Intrusion Detection System</h1>
    <p>
        A professional cybersecurity platform designed to monitor, detect,
        and classify suspicious network activities using intelligent
        traffic analysis techniques.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- PROBLEM STATEMENT ----------------
st.markdown("""
<div class="section">
    <h2>🔍 Problem Statement</h2>
    <p style="font-size:18px; max-width:820px;">
        Modern organizations face increasing cyber threats such as
        denial-of-service attacks, unauthorized access attempts, and
        network reconnaissance. Traditional security mechanisms are
        insufficient against sophisticated attack patterns.
        A Network Intrusion Detection System (IDS) enables real-time
        analysis and proactive threat detection.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    padding: 14px 34px;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
    transition: all 0.3s ease;
    margin-left: 7rem;
}

div.stButton > button p {
    color: white !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 32px rgba(37, 99, 235, 0.45);
    background: linear-gradient(90deg, #1d4ed8, #1e40af);
}

</style>
""", unsafe_allow_html=True)
# ---------- CENTERED BUTTON ----------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button(" Start Detecting"):
        st.switch_page("pages/Home.py")

# ---------------- FEATURES ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h3>🧠 Intelligent Detection</h3>
        <p>
            Detects abnormal network behavior using intelligent
            traffic analysis to identify potential intrusions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>⚡ Real-Time Monitoring</h3>
        <p>
            Continuously monitors live network traffic and
            flags suspicious activities instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>🚦 Severity Classification</h3>
        <p>
            Categorizes detected intrusions into low, medium,
            and high severity levels for faster response.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SYSTEM WORKFLOW ----------------
st.markdown("""
<div class="section">
    <h2>🔄 System Workflow</h2>
    <p style="font-size:18px; max-width:820px;">
        Network traffic is captured and analyzed for suspicious behavior.
        Identified threats are classified by severity, and alerts are
        generated for security administrators.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- TECHNOLOGY STACK ----------------
st.markdown("""
<div class="section">
    <h2>⚙️ Technology Stack</h2>
    <div class="tag">Python</div>
    <div class="tag">Streamlit</div>
    <div class="tag">Machine Learning</div>
    <div class="tag">Network Security</div>
</div>
""", unsafe_allow_html=True)

# ---------------- CTA ----------------
st.markdown("""
<div class="section">
    <div class="card">
        <h2>🚀 Project Objective</h2>
        <p>
            To design and implement a scalable, efficient, and intelligent
            Network Intrusion Detection System that enhances network
            security and minimizes cyber risks.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    © 2026 Network IDS | Academic Project
</div>
""", unsafe_allow_html=True)

# ==========================
# Manual Detection Panel
# ==========================
# st.sidebar.header("Manual Traffic Input")

# src_ip = st.sidebar.text_input("Source IP", "192.168.1.10")
# dst_ip = st.sidebar.text_input("Destination IP", "192.168.1.1")

# protocol = st.sidebar.number_input("Protocol", 0, 255, 17)
# flow_duration = st.sidebar.number_input("Flow Duration (sec)", 0.0)
# fwd = st.sidebar.number_input("Forward Packets", 0)
# bwd = st.sidebar.number_input("Backward Packets", 0)
# fwd_len = st.sidebar.number_input("Forward Bytes", 0.0)
# bwd_len = st.sidebar.number_input("Backward Bytes", 0.0)
# fwd_mean = st.sidebar.number_input("Forward Mean Bytes", 0.0)
# bwd_mean = st.sidebar.number_input("Backward Mean Bytes", 0.0)
# fwd_pps = st.sidebar.number_input("Forward PPS", 0.0)
# bwd_pps = st.sidebar.number_input("Backward PPS", 0.0)
# fwd_iat = st.sidebar.number_input("Forward IAT Mean", 0.0)
# bwd_iat = st.sidebar.number_input("Backward IAT Mean", 0.0)
# flow_iat = st.sidebar.number_input("Flow IAT Mean", 0.0)
# flow_pps = st.sidebar.number_input("Flow PPS", 0.0)
# flow_bps = st.sidebar.number_input("Flow BPS", 0.0)

# if st.sidebar.button("Run Detection"):
#     payload = {
#         "src_ip": src_ip,
#         "dst_ip": dst_ip,
#         "protocol": protocol,
#         "flow_duration": flow_duration,
#         "total_forward_packets": fwd,
#         "total_backward_packets": bwd,
#         "total_forward_packets_length": fwd_len,
#         "total_backward_packets_length": bwd_len,
#         "forward_packet_length_mean": fwd_mean,
#         "backward_packet_length_mean": bwd_mean,
#         "forward_packets_per_second": fwd_pps,
#         "backward_packets_per_second": bwd_pps,
#         "forward_iat_mean": fwd_iat,
#         "backward_iat_mean": bwd_iat,
#         "flow_iat_mean": flow_iat,
#         "flow_packets_per_seconds": flow_pps,
#         "flow_bytes_per_seconds": flow_bps
#     }

#     resp = requests.post(API_URL, json=payload)

#     if resp.status_code != 200:
#         st.error("Backend API error")
#         st.text(resp.text)
#         st.stop()

#     try:
#         res = resp.json()
#     except:
#         st.error("Backend returned invalid response")
#         st.text(resp.text)
#         st.stop()

#     st.subheader("🔍 Prediction Result")
#     st.json(res)

#     severity, reason = get_severity(res["prediction"], payload)

#     log_attack(src_ip, dst_ip, res["prediction"], severity, reason)


# ==========================
# Logs Table
# ==========================
# st.subheader("📊 Detection Logs")
# conn = get_db()
# df = pd.read_sql("SELECT * FROM logs ORDER BY id DESC LIMIT 100", conn)

# def color_severity(val):
#     if val == "CRITICAL":
#         return "background-color:#ff4d4d"
#     if val == "HIGH":
#         return "background-color:#ff944d"
#     if val == "MEDIUM":
#         return "background-color:#ffd11a"
#     return "background-color:#a6ff4d"

# st.dataframe(df.style.applymap(color_severity, subset=["severity"]), use_container_width=True)
