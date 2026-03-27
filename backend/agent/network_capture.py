from scapy.all import sniff, IP
import numpy as np, time

def capture_live_flow(duration=5):
    
    """Capture packets for a few seconds and compute features."""
    packets = sniff(timeout=duration)
    
    # Initialize counters
    total_forward_packets = total_backward_packets = 0
    total_forward_length = total_backward_length = 0
    forward_times, backward_times = [], []
    start_time = time.time()

    src_ip = None
    dst_ip = None
    protocol = 0

    for pkt in packets:
        if IP in pkt:
            protocol = pkt[IP].proto
            if src_ip is None:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst

            if pkt[IP].src == src_ip:
                total_forward_packets += 1
                total_forward_length += len(pkt)
                forward_times.append(time.time() - start_time)
            else:
                total_backward_packets += 1
                total_backward_length += len(pkt)
                backward_times.append(time.time() - start_time)

    flow_duration = time.time() - start_time
    forward_packet_length_mean = total_forward_length / (total_forward_packets or 1)
    backward_packet_length_mean = total_backward_length / (total_backward_packets or 1)
    forward_iat_mean = np.mean(np.diff(forward_times)) if len(forward_times) > 1 else 0
    backward_iat_mean = np.mean(np.diff(backward_times)) if len(backward_times) > 1 else 0
    flow_iat_mean = (forward_iat_mean + backward_iat_mean) / 2
    flow_packets_per_seconds = (total_forward_packets + total_backward_packets) / (flow_duration or 1)
    flow_bytes_per_seconds = (total_forward_length + total_backward_length) / (flow_duration or 1)

    return np.array([[
        protocol, flow_duration, total_forward_packets, total_backward_packets,
        total_forward_length, total_backward_length, forward_packet_length_mean,
        backward_packet_length_mean, total_forward_packets / (flow_duration or 1),
        total_backward_packets / (flow_duration or 1), forward_iat_mean, backward_iat_mean,
        flow_iat_mean, flow_packets_per_seconds, flow_bytes_per_seconds
    ]])
