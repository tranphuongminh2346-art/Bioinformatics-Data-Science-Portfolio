"""
Unit Tests for PCAP Traffic Analyzer
Author: Portfolio Creator
Description: Verify binary header parsing, TCP port extractions, and scan detections.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import struct

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pcap_analyzer import PCAPAnalyzer
from generate_pcap import generate_packet

class TestPCAPAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a temp PCAP file
        self.db_fd, self.temp_pcap_path = tempfile.mkstemp(suffix=".pcap")
        os.close(self.db_fd)
        
        # Write magic number and packet list
        # Little endian global header (24 bytes)
        global_header = struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
        
        with open(self.temp_pcap_path, 'wb') as f:
            f.write(global_header)
            
            # Write 6 packets from host 10.0.0.1 to unique ports (representing a scan)
            for port in [80, 21, 22, 23, 25, 443]:
                payload = generate_packet("10.0.0.1", "192.168.1.1", 12345, port, protocol=6)
                incl_len = len(payload)
                orig_len = incl_len
                ts_sec = 1718000000
                ts_usec = 0
                
                f.write(struct.pack('<IIII', ts_sec, ts_usec, incl_len, orig_len))
                f.write(payload)
                
        self.analyzer = PCAPAnalyzer(self.temp_pcap_path)

    def tearDown(self):
        if os.path.exists(self.temp_pcap_path):
            try:
                os.remove(self.temp_pcap_path)
            except PermissionError:
                pass

    def test_endianness_and_parse(self):
        self.analyzer.parse()
        self.assertEqual(self.analyzer.endian, '<')
        self.assertEqual(len(self.analyzer.packets), 6)

    def test_header_decoding(self):
        self.analyzer.parse()
        pkt = self.analyzer.packets[0]
        
        self.assertEqual(pkt["src_ip"], "10.0.0.1")
        self.assertEqual(pkt["dst_ip"], "192.168.1.1")
        self.assertEqual(pkt["protocol"], "TCP")
        self.assertEqual(pkt["dst_port"], 80)

    def test_scan_intrusion_detection(self):
        self.analyzer.parse()
        # Scan threshold = 5 unique ports.
        # Host 10.0.0.1 visited 6 ports -> should be flagged
        anomalies = self.analyzer.detect_port_scans(scan_threshold=5)
        
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["src_ip"], "10.0.0.1")
        self.assertEqual(anomalies[0]["unique_ports_count"], 6)
        self.assertIn(443, anomalies[0]["ports"])

if __name__ == "__main__":
    unittest.main()
