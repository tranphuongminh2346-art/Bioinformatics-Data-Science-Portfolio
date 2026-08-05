"""
PCAP Traffic Analyzer CLI
Author: Portfolio Creator
Description: CLI driver to parse PCAP files, print packet reports, and detect port scans.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pcap_analyzer import PCAPAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description="PCAP Traffic Analyzer - Decode TCP packet headers and detect scans."
    )
    parser.add_argument(
        "-i", "--input",
        default="traffic.pcap",
        help="Path to input binary PCAP file (default: traffic.pcap)."
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=5,
        help="Unique port visits scan threshold (default: 5)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("PCAP Binary Network Traffic Analyzer & Intrusion Detector")
    print("=" * 60)
    print(f"[*] Input PCAP: {args.input}")
    print(f"[*] Threshold : {args.threshold} unique ports")

    # If the file does not exist, check if we can run the generator locally
    if not os.path.exists(args.input):
        print(f"[-] PCAP file '{args.input}' not found.")
        print("[*] Generating mock PCAP file dynamically...")
        try:
            import generate_pcap
            generate_pcap.main()
        except Exception as e:
            print(f"[-] Failed to generate mock PCAP: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        analyzer = PCAPAnalyzer(args.input)
        print("[*] Reading binary streams and headers...")
        analyzer.parse()
        
        print(f"[+] Successfully parsed {len(analyzer.packets)} IPv4 packets.")
        
        # Protocol stats
        protocols = {}
        for pkt in analyzer.packets:
            proto = pkt["protocol"]
            protocols[proto] = protocols.get(proto, 0) + 1
            
        print("\nProtocol Distribution Summary:")
        for proto, count in protocols.items():
            print(f"    - {proto:8}: {count} packets")
            
        # Detect scans
        print("\n[*] Auditing traffic patterns for port scan anomalies...")
        scans = analyzer.detect_port_scans(scan_threshold=args.threshold)
        
        print("\n" + "=" * 60)
        print("Flagged Intrusion Anomalies")
        print("=" * 60)
        print(f"[*] Total Flagged IPs: {len(scans)}")
        print("-" * 60)
        for idx, scan in enumerate(scans):
            print(f"[{idx+1}] Source IP      : {scan['src_ip']}")
            print(f"    - Unique Ports : {scan['unique_ports_count']}")
            print(f"    - Visited Ports: {scan['ports']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] PCAP Analyzer failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
