# PCAP Packet Network Anomaly Parser

A low-level network security and data engineering pipeline that parses binary **PCAP (Packet Capture)** files, decodes Link (Ethernet), Internet (IPv4), and Transport (TCP/UDP) protocol headers directly using struct unpack offsets, and analyzes network traffic to detect **Port Scanning** anomalies.

## Features
- **Binary PCAP Parser**: Decodes global headers, detects endianness (magic bytes `0xa1b2c3d4`), and reads sequential packet blocks.
- **Protocol Header Decoders**: Decodes Ethernet MAC addresses, IPv4 protocol fields, and TCP/UDP ports using standard byte offsets.
- **Intrusion Detection System (IDS)**: Audits traffic packets to flag IPs connecting to a suspicious number of unique ports.

## Project Structure
- `pcap_analyzer.py`: PCAP Global/Packet headers decoder, and anomaly auditors.
- `generate_pcap.py`: Mock network PCAP binary generator.
- `main.py`: Command-line interface driver.
- `test_analyzer.py`: Unit test suite verifying binary decoders and scans detections.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To analyze network packet captures:
```bash
python main.py --input traffic.pcap --threshold 5
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_analyzer.py
```
