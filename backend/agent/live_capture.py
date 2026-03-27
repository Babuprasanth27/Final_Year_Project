# from scapy.all import sniff, IP
# import numpy as np
# import time
# import socket

# def capture_live_flow(duration=10, filter_ip=None, return_meta=False):
#     """
#     Capture live packets for a few seconds and extract basic flow-level features.
#     Automatically filters by local IP if provided, to capture only relevant packets.
#     """

#     print(f"🔍 Capturing live packets for {duration} seconds...")
#     if not filter_ip:
#         # Automatically detect and use local IP for filtering
#         try:
#             filter_ip = socket.gethostbyname(socket.gethostname())
#             print(f"📡 Auto-detected local IP: {filter_ip}")
#         except Exception as e:
#             print(f"⚠️ Could not auto-detect IP: {e}")
#             filter_ip = None
#     else:
#         print(f"📡 Filtering packets for IP: {filter_ip}")

#     # Start packet capture
#     start_time = time.time()
#     packets = sniff(timeout=duration)
#     end_time = time.time()

#     total_forward_packets = total_backward_packets = 0
#     total_forward_length = total_backward_length = 0
#     forward_times, backward_times = [], []

#     src_ip = dst_ip = None
#     protocol = 0

#     for pkt in packets:
#         if IP in pkt:
#             src = pkt[IP].src
#             dst = pkt[IP].dst
#             protocol = pkt[IP].proto

#             # Skip unrelated traffic if filter is applied
#             if filter_ip and (src != filter_ip and dst != filter_ip):
#                 continue

#             if src_ip is None:
#                 src_ip = src
#                 dst_ip = dst

#             now = time.time() - start_time

#             if src == filter_ip or src == src_ip:
#                 total_forward_packets += 1
#                 total_forward_length += len(pkt)
#                 forward_times.append(now)
#             else:
#                 total_backward_packets += 1
#                 total_backward_length += len(pkt)
#                 backward_times.append(now)

#     flow_duration = max(end_time - start_time, 1e-6)  # prevent div by zero

#     # Derived features
#     forward_packet_length_mean = total_forward_length / (total_forward_packets or 1)
#     backward_packet_length_mean = total_backward_length / (total_backward_packets or 1)

#     forward_iat_mean = np.mean(np.diff(forward_times)) if len(forward_times) > 1 else 0
#     backward_iat_mean = np.mean(np.diff(backward_times)) if len(backward_times) > 1 else 0
#     flow_iat_mean = (forward_iat_mean + backward_iat_mean) / 2

#     forward_pps = total_forward_packets / flow_duration
#     backward_pps = total_backward_packets / flow_duration

#     flow_packets_per_seconds = (total_forward_packets + total_backward_packets) / flow_duration
#     flow_bytes_per_seconds = (total_forward_length + total_backward_length) / flow_duration

#     total_packets = total_forward_packets + total_backward_packets

#     print(f"✅ Capture complete. Total packets: {total_packets}")

#     # Handle empty capture
#     if total_packets == 0:
#         print("⚠️ Warning: No packets captured. Returning zero vector.")
#         features = np.zeros((1, 15))
#     else:
#         features = np.array([[
#             protocol,
#             flow_duration,
#             total_forward_packets,
#             total_backward_packets,
#             total_forward_length,
#             total_backward_length,
#             forward_packet_length_mean,
#             backward_packet_length_mean,
#             forward_pps,
#             backward_pps,
#             forward_iat_mean,
#             backward_iat_mean,
#             flow_iat_mean,
#             flow_packets_per_seconds,
#             flow_bytes_per_seconds
#         ]])

#     if return_meta:
#         return {
#             "features": features,
#             "meta": {
#                 "packet_count": total_packets,
#                 "src_ip": src_ip,
#                 "dst_ip": dst_ip,
#                 "duration": round(flow_duration, 4),
#                 "protocol": protocol
#             },
#         }

#     return features
from scapy.all import sniff, IP
import numpy as np
import time
import socket

def capture_live_flow(duration=10, filter_ip=None, return_meta=False):
    """
    Capture live packets for a few seconds and extract basic flow-level features.
    Automatically filters by local IP if provided, to capture only relevant packets.
    """

    print(f"\n🔍 Capturing live packets for {duration} seconds...")
    if not filter_ip:
        # Automatically detect and use local IP for filtering
        try:
            filter_ip = socket.gethostbyname(socket.gethostname())
            print(f"📡 Auto-detected local IP: {filter_ip}")
        except Exception as e:
            print(f"⚠️ Could not auto-detect IP: {e}")
            filter_ip = None
    else:
        print(f"📡 Filtering packets for IP: {filter_ip}")

    # Start packet capture
    start_time = time.time()
    packets = sniff(timeout=duration)
    end_time = time.time()

    total_forward_packets = total_backward_packets = 0
    total_forward_length = total_backward_length = 0
    forward_times, backward_times = [], []

    src_ip = dst_ip = None
    protocol = 0

    for pkt in packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            protocol = pkt[IP].proto

            # Skip unrelated traffic if filter is applied
            if filter_ip and (src != filter_ip and dst != filter_ip):
                continue

            if src_ip is None:
                src_ip = src
                dst_ip = dst

            now = time.time() - start_time

            if src == filter_ip or src == src_ip:
                total_forward_packets += 1
                total_forward_length += len(pkt)
                forward_times.append(now)
            else:
                total_backward_packets += 1
                total_backward_length += len(pkt)
                backward_times.append(now)

    flow_duration = max(end_time - start_time, 1e-6)  # prevent division by zero

    # Derived features
    forward_packet_length_mean = total_forward_length / (total_forward_packets or 1)
    backward_packet_length_mean = total_backward_length / (total_backward_packets or 1)

    forward_iat_mean = np.mean(np.diff(forward_times)) if len(forward_times) > 1 else 0
    backward_iat_mean = np.mean(np.diff(backward_times)) if len(backward_times) > 1 else 0
    flow_iat_mean = (forward_iat_mean + backward_iat_mean) / 2

    forward_pps = total_forward_packets / flow_duration
    backward_pps = total_backward_packets / flow_duration

    flow_packets_per_seconds = (total_forward_packets + total_backward_packets) / flow_duration
    flow_bytes_per_seconds = (total_forward_length + total_backward_length) / flow_duration

    total_packets = total_forward_packets + total_backward_packets

    print(f"✅ Capture complete. Total packets: {total_packets}")

    # Handle empty capture
    if total_packets == 0:
        print("⚠️ Warning: No packets captured. Returning zero vector.")
        features = np.zeros((1, 15))
    else:
        features = np.array([[
            protocol,
            flow_duration,
            total_forward_packets,
            total_backward_packets,
            total_forward_length,
            total_backward_length,
            forward_packet_length_mean,
            backward_packet_length_mean,
            forward_pps,
            backward_pps,
            forward_iat_mean,
            backward_iat_mean,
            flow_iat_mean,
            flow_packets_per_seconds,
            flow_bytes_per_seconds
        ]])

        #  Define names for each feature
        feature_names = [
            "protocol",
            "flow_duration",
            "total_forward_packets",
            "total_backward_packets",
            "total_forward_length",
            "total_backward_length",
            "forward_packet_length_mean",
            "backward_packet_length_mean",
            "forward_pps",
            "backward_pps",
            "forward_iat_mean",
            "backward_iat_mean",
            "flow_iat_mean",
            "flow_packets_per_seconds",
            "flow_bytes_per_seconds"
        ]

        # ✅ Print features neatly to the terminal
        print("\n📊 Extracted Flow Features:")
        for name, value in zip(feature_names, features[0]):
            print(f"   {name:<30}: {value:.6f}")

    if return_meta:
        return {
            "features": features,
            "meta": {
                "packet_count": total_packets,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "duration": round(flow_duration, 4),
                "protocol": protocol
            },
        }

    return features


#  Run it directly for testing (prints results in terminal)
if __name__ == "__main__":
    while True:
        capture_live_flow(duration=10)
        print("\n--- Waiting 3 seconds before next capture ---\n")
        time.sleep(3)
