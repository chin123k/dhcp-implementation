import socket
import struct
import random

DHCP_SERVER_PORT = 67
DHCP_CLIENT_PORT = 68

LEASED_IPS = {}
AVAILABLE_IPS = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]  # IPs to assign

def create_dhcp_offer(transaction_id, client_mac):
    """Create a DHCP Offer packet"""
    offered_ip = AVAILABLE_IPS.pop(0) if AVAILABLE_IPS else "0.0.0.0"
    LEASED_IPS[client_mac] = offered_ip

    dhcp_offer = struct.pack("!4s4s", bytes(offered_ip, 'utf-8'), bytes("255.255.255.0", 'utf-8'))
    return dhcp_offer

def start_dhcp_server():
    """Start a simple DHCP server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", DHCP_SERVER_PORT))

    print("DHCP Server listening on port 67...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        transaction_id, client_mac = struct.unpack("!I6s", data[:10])

        print(f"Received DHCP Discover from {client_mac.hex()}")

        # Send DHCP Offer
        dhcp_offer = create_dhcp_offer(transaction_id, client_mac)
        server_socket.sendto(dhcp_offer, ("<broadcast>", DHCP_CLIENT_PORT))
        print(f"Sent DHCP Offer: {LEASED_IPS[client_mac]} to {client_mac.hex()}")

if __name__ == "__main__":
    start_dhcp_server()
