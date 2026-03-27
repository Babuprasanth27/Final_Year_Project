import ipaddress

def RESULT(label, reason):
    return {
        "mode": "firewall",
        "prediction": label,
        "predicted_class": -1 if label == "ANOMALY" else 0,
        "status": "success",
        "reason": reason
    }

def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def traffic_firewall(d):
    total_packets = d.total_forward_packets + d.total_backward_packets

    # IP sanity
    if not valid_ip(d.src_ip) or not valid_ip(d.dst_ip):
        return RESULT("ANOMALY", "Invalid IP address")

    # Invalid protocol
    if d.protocol < 0 or d.protocol > 255:
        return RESULT("ANOMALY", "Invalid protocol number")

    # Truly idle traffic
    if d.flow_duration == 0 and total_packets == 0:
        return RESULT("NORMAL", "Idle traffic")

    # Impossible traffic
    if total_packets > 0 and d.flow_bytes_per_seconds == 0:
        return RESULT("ANOMALY", "Packets exist but bytes/sec = 0")

    # Let small flows go to ML
    return None
