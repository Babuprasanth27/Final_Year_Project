def get_severity(prediction, payload=None):
    """
    Returns severity level and reason based on prediction.
    Example mapping:
    - 'Normal' -> LOW
    - 'DoS' -> HIGH
    - 'PortScan' -> MEDIUM
    """
    severity = "LOW"
    reason = "Normal traffic"

    if prediction.lower() != "normal":
        if prediction.lower() in ["dos", "ddos"]:
            severity = "CRITICAL"
        elif prediction.lower() in ["portscan", "malware"]:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        reason = f"Detected {prediction}"

    return severity, reason
