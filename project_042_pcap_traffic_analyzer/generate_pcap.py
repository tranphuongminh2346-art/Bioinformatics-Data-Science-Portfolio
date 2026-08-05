"""
Helper script to generate a mock traffic.pcap file
Author: Portfolio Creator
Description: Creates a valid binary PCAP file containing simulated Ethernet/IPv4/TCP packet headers.
Language: English (100%)
"""

import struct

def generate_packet(src_ip, dst_ip, src_port, dst_port, protocol=6):
    """
    Constructs a mock Ethernet + IPv4 + TCP packet payload.
    TCP protocol = 6, UDP = 17.
    """
    # 1. Ethernet Header (14 bytes)
    dst_mac = b'\x00\x11\x22\x33\x44\x55'
    src_mac = b'\x00\xaa\xbb\xcc\xdd\xee'
    ethertype = b'\x08\x00'  # IPv4
    eth_header = dst_mac + src_mac + ethertype
    
    # 2. IP Header (20 bytes)
    version_ihl = 0x45  # IPv4, IHL = 5 (20 bytes)
    tos = 0x00
    total_length = 40  # 20 (IP) + 20 (TCP)
    packet_id = 1234
    flags_fragment = 0x4000  # Don't fragment
    ttl = 64
    ip_proto = protocol
    checksum = 0x0000  # Dummy
    src_bytes = bytes(int(x) for x in src_ip.split('.'))
    dst_bytes = bytes(int(x) for x in dst_ip.split('.'))
    
    ip_header = struct.pack(
        '>BBHHHBBH4s4s',
        version_ihl, tos, total_length, packet_id, flags_fragment,
        ttl, ip_proto, checksum, src_bytes, dst_bytes
    )
    
    # 3. TCP Header (20 bytes)
    seq = 1000
    ack = 0
    offset_res = 0x5000  # Header length = 5 (20 bytes)
    flags = 0x02  # SYN
    window = 1024
    tcp_checksum = 0
    urg_ptr = 0
    
    tcp_header = struct.pack(
        '>HHIIHHHH',
        src_port, dst_port, seq, ack, offset_res | flags, window, tcp_checksum, urg_ptr
    )
    
    return eth_header + ip_header + tcp_header

def main():
    pcap_path = "traffic.pcap"
    
    # Global Header (24 bytes)
    # Magic (4B), Maj (2B), Min (2B), Gmt (4B), Acc (4B), Snap (4B), LinkType (4B)
    global_header = struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
    
    # Let's generate a list of packets
    # Host 192.168.1.50 sends normal packets to 192.168.1.1 on port 80
    # Host 10.0.0.99 performs a port scan on 192.168.1.1, visiting ports 21, 22, 23, 25, 80, 443
    packets_to_write = [
        # Normal traffic
        ("192.168.1.50", "192.168.1.1", 50001, 80),
        ("192.168.1.50", "192.168.1.1", 50001, 80),
        ("192.168.1.50", "192.168.1.1", 50002, 80),
        # Port scan probes
        ("10.0.0.99", "192.168.1.1", 60000, 21),
        ("10.0.0.99", "192.168.1.1", 60000, 22),
        ("10.0.0.99", "192.168.1.1", 60000, 23),
        ("10.0.0.99", "192.168.1.1", 60000, 25),
        ("10.0.0.99", "192.168.1.1", 60000, 80),
        ("10.0.0.99", "192.168.1.1", 60000, 443),
    ]
    
    with open(pcap_path, 'wb') as f:
        f.write(global_header)
        
        for idx, (src_ip, dst_ip, src_port, dst_port) in enumerate(packets_to_write):
            payload = generate_packet(src_ip, dst_ip, src_port, dst_port)
            incl_len = len(payload)
            orig_len = incl_len
            ts_sec = 1718000000 + idx
            ts_usec = 0
            
            # Write Packet Header (16 bytes)
            f.write(struct.pack('<IIII', ts_sec, ts_usec, incl_len, orig_len))
            # Write Packet Payload
            f.write(payload)

    print(f"[+] Successfully generated mock PCAP file: {pcap_path}")

if __name__ == "__main__":
    main()
