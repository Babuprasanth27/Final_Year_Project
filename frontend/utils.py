def get_severity(label, flow):
    pps = flow["flow_packets_per_seconds"]
    bps = flow["flow_bytes_per_seconds"]

    # Clean traffic
    if label == "NORMAL":
        return "NORMAL", "Traffic is within safe thresholds"

    # Malformed traffic
    if label == "ANOMALY":
        return "MEDIUM", "Malformed or suspicious traffic pattern"

    # Real attack traffic
    if pps > 3000 or bps > 1_000_000:
        return "CRITICAL", "Massive flooding attack detected"

    if pps > 1000 or bps > 500_000:
        return "HIGH", "High traffic rate indicates DoS behavior"

    return "MEDIUM", "Suspicious abnormal traffic"
