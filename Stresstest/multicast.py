import sys
from scapy.all import *
from time import sleep
from random import randint

def main():
    if len(sys.argv) < 4:
        print("Usage: python multicast_stress_test.py <multicast_group> <port> <interval>")
        sys.exit(1)

    multicast_group = sys.argv[1]
    port = int(sys.argv[2])
    interval = float(sys.argv[3])

    if not is_valid_multicast_address(multicast_group):
        print("Invalid multicast address")
        sys.exit(1)

    while True:
        # Generate a random payload
        payload = RandString(randint(100, 1500))

        # Create an IP packet
        ip_packet = IP(dst=multicast_group, ttl=5)

        # Create a UDP packet
        udp_packet = UDP(sport=RandShort(), dport=port) / payload

        # Combine the IP and UDP packets
        packet = ip_packet / udp_packet

        # Send the packet
        send(packet, verbose=0)

        # Wait for the specified interval
        sleep(interval)

def is_valid_multicast_address(address):
    try:
        ip = IPAddress(address)
        return ip.is_multicast()
    except AddrFormatError:
        return False

if __name__ == "__main__":
    main()
