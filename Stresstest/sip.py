import sys
import argparse
from scapy.all import *
from time import sleep

# Define a template for the SIP INVITE message
sip_invite_template = (
    "INVITE sip:user@{target_ip} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {src_ip}:{src_port};branch={branch}\r\n"
    "From: \"Stress Tester\" <sip:stress_tester@{src_ip}:{src_port}>;tag={tag}\r\n"
    "To: <sip:user@{target_ip}:{target_port}>\r\n"
    "Call-ID: {call_id}@{src_ip}:{src_port}\r\n"
    "CSeq: 1 INVITE\r\n"
    "Content-Type: application/sdp\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

# Function to generate a random alphanumeric string
def random_string(length):
    import string
    import random

    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Main function to send the SIP INVITE messages
def stress_test_sip(target_ip, target_port, num_messages):
    for i in range(num_messages):
        # Generate random values for the SIP message
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        src_port = random.randint(1024, 65535)
        branch = random_string(8)
        tag = random_string(8)
        call_id = random_string(16)

        # Format the SIP INVITE message with the random values
        sip_invite = sip_invite_template.format(
            target_ip=target_ip,
            src_ip=src_ip,
            src_port=src_port,
            branch=branch,
            tag=tag,
            call_id=call_id,
            target_port=target_port
        )

        # Create the packet with Scapy
        packet = IP(dst=target_ip, src=src_ip) / UDP(dport=target_port, sport=src_port) / Raw(load=sip_invite)

        # Send the packet
        send(packet)

        # Print the progress
        print(f"Sent {i+1}/{num_messages} SIP INVITE messages to {target_ip}:{target_port}")

        # Sleep for a short duration to control the sending rate
        sleep(0.01)

def main():
    parser = argparse.ArgumentParser(description="SIP protocol stress test using Python and Scapy")
    parser.add_argument("target_ip", help="Target IP address of the SIP server")
    parser.add_argument("target_port", type=int, help="Target port for the SIP server")
    parser.add_argument("num_messages", type=int, help="Number of messages to send")

    args = parser.parse_args()

    stress_test_sip(args.target_ip, args.target_port, args.num_messages)

if __name__ == "__main__":
    main()
