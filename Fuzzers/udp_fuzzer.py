import argparse
import socket
import sys
from scapy.all import *


def check_target(ip, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(b"", (ip, port))
        sock.recvfrom(1024)
        return True
    except socket.timeout:
        return False
    except ConnectionResetError:
        return False


def udp_fuzzer(ip, port, prefix, interval, timeout):
    payload_length = 0

    while True:
        try:
            payload_length += 100
            payload = prefix + str(RandString(payload_length))
            packet = IP(dst=ip) / fuzz(UDP(dport=port) / Raw(load=payload))

            send(packet, verbose=0, inter=interval)

            response = check_target(ip, port, timeout)
            if not response:
                print(f"Target crashed. Payload length: {payload_length}, Prefix: '{prefix}'")
                break
        except KeyboardInterrupt:
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="UDP Fuzzer")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("port", type=int, help="Target port number")
    parser.add_argument("-p", "--prefix", default="", help="Optional prefix for the payload")
    parser.add_argument("-i", "--interval", type=float, default=0.1, help="Time interval between sending packets")
    parser.add_argument("-t", "--timeout", type=float, default=5, help="Timeout for target response check")

    args = parser.parse_args()

    udp_fuzzer(args.ip, args.port, args.prefix, args.interval, args.timeout)


if __name__ == "__main__":
    main()
