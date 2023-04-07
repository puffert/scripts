# ospf_stress_test.py

import sys
import argparse
from scapy.all import *
from scapy.layers.ospf import OSPF_Hdr, OSPF_Hello
from time import sleep

def stress_test_ospf(target_ip, num_messages):
    for i in range(num_messages):
        # Send OSPF Hello packet
        packet = IP(dst=target_ip) / OSPF_Hdr() / OSPF_Hello()
        send(packet)

        # Print the progress
        print(f"Sent {i+1}/{num_messages} OSPF packets to {target_ip}")

        # Sleep for a short duration to control the sending rate
        sleep(0.01)

def main():
    parser = argparse.ArgumentParser(description="OSPF stress test using Python and Scapy")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("num_messages", type=int, help="Number of messages to send")

    args = parser.parse_args()

    stress_test_ospf(args.target_ip, args.num_messages)

if __name__ == "__main__":
    main()
