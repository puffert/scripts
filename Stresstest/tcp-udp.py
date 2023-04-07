import sys
import argparse
from scapy.all import *
from time import sleep

# Function to generate a random alphanumeric string
def random_string(length):
    import string
    import random

    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Main function to send packets
def stress_test(protocol, target_ip, target_port, num_messages):
    for i in range(num_messages):
        # Generate random values for the packet
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        src_port = random.randint(1024, 65535)
        payload = random_string(64)

        # Create and send the packet based on the chosen protocol
        if protocol == "udp":
            packet = IP(dst=target_ip, src=src_ip) / UDP(dport=target_port, sport=src_port) / Raw(load=payload)
            send(packet)
        elif protocol == "tcp":
            packet = IP(dst=target_ip, src=src_ip) / TCP(dport=target_port, sport=src_port) / Raw(load=payload)
            send(packet)

        # Print the progress
        print(f"Sent {i+1}/{num_messages} {protocol.upper()} packets to {target_ip}:{target_port}")

        # Sleep for a short duration to control the sending rate
        sleep(0.01)

def main():
    parser = argparse.ArgumentParser(description="TCP/UDP stress test using Python and Scapy")
    parser.add_argument("protocol", choices=["tcp", "udp"], help="Protocol to use for stress test (tcp or udp)")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port")
    parser.add_argument("num_messages", type=int, help="Number of messages to send")

    args = parser.parse_args()

    stress_test(args.protocol, args.target_ip, args.target_port, args.num_messages)

if __name__ == "__main__":
    main()
