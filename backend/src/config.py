import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "data.csv")
MODEL_SAVE_DIR = os.path.join(BASE_DIR, "models", "saved")


os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

# ==========================================
# Label Map for Predictions
# ==========================================
LABEL_MAP = {
    0: "BENIGN",
    1: "DoS_DNS",
    2: "PortScan",
    3: "DDoS_DNS",
    4: "DrDoS_LDAP",
    5: "DrDoS_SNMP",
    6: "DrDoS_UDP",
    7: "DrDoS_TCP",
    8: "DrDoS_MSSQL",
    9: "DDoS_NTP",
    10: "DrDoS_DNS",
    11: "FTP_Patator",
    12: "SSH_Patator",
    13: "Infiltration",
    14: "Bot",
    15: "Web_Attack_Brute_Force",
    16: "Web_Attack_XSS",
    17: "Web_Attack_SQL_Injection",
    18: "Heartbleed",
}
