# icmp_stress_test.py

import sys
import argparse
from scapy.all import *
from time import sleep

def stress_test_icmp(target_ip, num_messages):
    for i in range(num_messages):
        # Send ICMP Echo Request packet
        send(IP(dst=target_ip) / ICMP())

        # Print the progress
        print(f"Sent {i+1}/{num_messages} ICMP packets to {target_ip}")

        # Sleep for a short duration to control the sending rate
        sleep(0.01)

def main():
    parser = argparse.ArgumentParser(description="ICMP stress test using Python and Scapy")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("num_messages", type=int, help="Number of messages to send")

    args = parser.parse_args()

    stress_test_icmp(args.target_ip, args.num_messages)

if __name__ == "__main__":
    main()
