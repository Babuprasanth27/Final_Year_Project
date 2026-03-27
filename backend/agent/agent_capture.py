# agent/agent_capture.py
import pyshark
import time
import threading
import requests
from ipaddress import ip_address

API_URL = "http://127.0.0.1:8000/predict"
FLOW_TIMEOUT = 2.0

flows = {}

# Optional: set your LAN range for direction detection
LOCAL_NET = None   # e.g. "192.168.1.0/24"


def is_forward(src):
    if not LOCAL_NET:
        return True
    return ip_address(src) in ip_address(LOCAL_NET)


def flow_key(pkt):
    try:
        ip = pkt.ip
        proto = int(ip.proto)
        src = ip.src
        dst = ip.dst
        sport = getattr(pkt[pkt.transport_layer], 'srcport', '0')
        dport = getattr(pkt[pkt.transport_layer], 'dstport', '0')
        return (src, dst, proto, sport, dport)
    except Exception:
        return None


def update_flow(pkt):
    k = flow_key(pkt)
    if not k:
        return

    now = time.time()
    pkt_len = int(pkt.length)
    f = flows.get(k)

    if not f:
        flows[k] = {
            "first_ts": now,
            "last_ts": now,
            "last_pkt_ts": now,
            "packets": 1,
            "bytes": pkt_len,
            "fwd_packets": 1,
            "bwd_packets": 0,
            "fwd_bytes": pkt_len,
            "bwd_bytes": 0,
            "iat_list": [],
            "src": k[0]
        }
    else:
        iat = now - f["last_pkt_ts"]
        f["iat_list"].append(iat)
        f["last_pkt_ts"] = now
        f["last_ts"] = now

        # Direction-aware counting
        if pkt.ip.src == f["src"]:
            f["fwd_packets"] += 1
            f["fwd_bytes"] += pkt_len
        else:
            f["bwd_packets"] += 1
            f["bwd_bytes"] += pkt_len


def flow_monitor():
    while True:
        now = time.time()
        to_close = []

        for k, f in list(flows.items()):
            if now - f["last_ts"] > FLOW_TIMEOUT:
                to_close.append(k)

        for k in to_close:
            f = flows.pop(k)
            payload = convert_flow_to_features(k, f)
            if not payload:
                continue

            try:
                resp = requests.post(API_URL, json=payload, timeout=3)
                print("Sent:", payload, "→", resp.text)
            except Exception as e:
                print("Send error:", e)

        time.sleep(0.5)


def convert_flow_to_features(key, f):
    src, dst, proto, sport, dport = key

    duration = max(f["last_ts"] - f["first_ts"], 0.1)
    forward_packets = f["fwd_packets"]
    backward_packets = f["bwd_packets"]
    forward_bytes = f["fwd_bytes"]
    backward_bytes = f["bwd_bytes"]

    # Ignore garbage flows
    if (forward_packets + backward_packets) < 2:
        return None

    forward_mean = forward_bytes / forward_packets if forward_packets else 0
    backward_mean = backward_bytes / backward_packets if backward_packets else 0

    fwd_pps = forward_packets / duration
    bwd_pps = backward_packets / duration
    iat_mean = sum(f["iat_list"]) / len(f["iat_list"]) if f["iat_list"] else 0

    return {
        "protocol": int(proto),
        "flow_duration": float(duration),
        "total_forward_packets": int(forward_packets),
        "total_backward_packets": int(backward_packets),
        "total_forward_packets_length": int(forward_bytes),
        "total_backward_packets_length": int(backward_bytes),
        "forward_packet_length_mean": float(forward_mean),
        "backward_packet_length_mean": float(backward_mean),
        "forward_packets_per_second": float(fwd_pps),
        "backward_packets_per_second": float(bwd_pps),
        "forward_iat_mean": float(iat_mean),
        "backward_iat_mean": float(iat_mean),
        "flow_iat_mean": float(iat_mean),
        "flow_packets_per_seconds": float((forward_packets + backward_packets) / duration),
        "flow_bytes_per_seconds": float((forward_bytes + backward_bytes) / duration),
        "src_ip": src,
        "dst_ip": dst
    }


if __name__ == "__main__":
    capture = pyshark.LiveCapture(interface="eth0")   # change interface if needed
    monitor_thread = threading.Thread(target=flow_monitor, daemon=True)
    monitor_thread.start()

    for pkt in capture.sniff_continuously():
        try:
            update_flow(pkt)
        except KeyboardInterrupt:
            break
