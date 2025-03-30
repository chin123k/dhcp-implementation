import socket
import struct

DHCP_SERVER_PORT = 67
DHCP_CLIENT_PORT = 68

def send_dhcp_discover():
    """Send a DHCP Discover message to request an IP address"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    transaction_id = 12345  # Random transaction ID
    client_mac = b'\xaa\xbb\xcc\xdd\xee\xff'  # Example MAC address
    dhcp_discover = struct.pack("!I6s", transaction_id, client_mac)

    client_socket.sendto(dhcp_discover, ("<broadcast>", DHCP_SERVER_PORT))
    print("Sent DHCP Discover")

    # Receive DHCP Offer
    data, _ = client_socket.recvfrom(1024)
    offered_ip, subnet_mask = struct.unpack("!4s4s", data)

    print(f"Received DHCP Offer: {offered_ip.decode()} with subnet {subnet_mask.decode()}")

    client_socket.close()

if __name__ == "__main__":
    send_dhcp_discover()
