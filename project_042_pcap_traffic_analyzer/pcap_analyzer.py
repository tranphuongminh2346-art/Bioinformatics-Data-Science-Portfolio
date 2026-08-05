"""
Binary PCAP Network Traffic Analyzer
Author: Portfolio Creator
Description: Parses raw binary PCAP packet streams, decodes Ethernet, IPv4,
             and TCP/UDP headers, and logs port scan traffic anomalies.
Language: English (100%)
"""

import os
import struct

class PCAPAnalyzer:
    """Parses binary PCAP files and extracts IP and port layer statistics."""
    
    def __init__(self, pcap_path: str):
        self.pcap_path = pcap_path
        self.packets = []
        self.endian = '='  # '=' means standard/native alignment
        
    def parse(self):
        """Parses the global header and all packets within the PCAP file."""
        if not os.path.exists(self.pcap_path):
            raise FileNotFoundError(f"PCAP file not found: {self.pcap_path}")
            
        with open(self.pcap_path, 'rb') as f:
            # 1. Parse Global Header (24 bytes)
            global_header = f.read(24)
            if len(global_header) < 24:
                raise ValueError("Invalid PCAP: Global header too short.")
                
            magic = struct.unpack('I', global_header[0:4])[0]
            if magic == 0xa1b2c3d4:
                self.endian = '<'  # Little endian
            elif magic == 0xd4c3b2a1:
                self.endian = '>'  # Big endian
            else:
                # Default fallback
                self.endian = '<'
                
            network_type = struct.unpack(self.endian + 'I', global_header[20:24])[0]
            
            # We only support Link-Layer Type 1 (Ethernet)
            if network_type != 1:
                raise ValueError(f"Unsupported Link Type: {network_type}. Only Ethernet (1) is supported.")
                
            # 2. Parse Packet Stream
            while True:
                header_bytes = f.read(16)
                if len(header_bytes) < 16:
                    break  # End of file
                    
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(self.endian + 'IIII', header_bytes)
                
                packet_data = f.read(incl_len)
                if len(packet_data) < incl_len:
                    break  # Truncated file
                    
                self.parse_packet(packet_data, ts_sec + ts_usec / 1e6)

    def parse_packet(self, data: bytes, timestamp: float):
        """Decodes Layer 2, 3, and 4 protocol headers from a raw Ethernet frame."""
        if len(data) < 14:
            return  # Invalid Ethernet frame
            
        # EtherType at bytes 12-13
        ethertype = struct.unpack('>H', data[12:14])[0]
        if ethertype != 0x0800:
            return  # We only support IPv4 (0x0800) in this parser
            
        # IPv4 Header starts at 14
        ip_data = data[14:]
        if len(ip_data) < 20:
            return
            
        # IP header length is in the lower 4 bits of the first byte * 4
        ihl = (ip_data[0] & 0x0F) * 4
        protocol = ip_data[9]
        
        # Source & Dest IPs
        src_ip = ".".join(str(b) for b in ip_data[12:16])
        dst_ip = ".".join(str(b) for b in ip_data[16:20])
        
        # Layer 4 Header starts at 14 + ihl
        l4_data = ip_data[ihl:]
        if len(l4_data) < 4:
            return
            
        # Parse ports
        src_port = struct.unpack('>H', l4_data[0:2])[0]
        dst_port = struct.unpack('>H', l4_data[2:4])[0]
        
        proto_name = "UNKNOWN"
        if protocol == 6:
            proto_name = "TCP"
        elif protocol == 17:
            proto_name = "UDP"
            
        self.packets.append({
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": proto_name,
            "src_port": src_port,
            "dst_port": dst_port,
            "length": len(data)
        })

    def detect_port_scans(self, scan_threshold: int = 5) -> list:
        """
        Detects potential port scanning IPs.
        A scan is flagged if a source IP visits more than 'scan_threshold' unique ports.
        
        Returns:
            list: List of dicts representing flagged IPs and visited ports count.
        """
        ip_ports = {}
        for pkt in self.packets:
            src = pkt["src_ip"]
            port = pkt["dst_port"]
            if src not in ip_ports:
                ip_ports[src] = set()
            ip_ports[src].add(port)
            
        anomalies = []
        for ip, ports in ip_ports.items():
            if len(ports) > scan_threshold:
                anomalies.append({
                    "src_ip": ip,
                    "unique_ports_count": len(ports),
                    "ports": sorted(list(ports))
                })
        return anomalies
