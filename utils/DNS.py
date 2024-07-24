import socket
import struct



def start_dns_server():
    addr = socket.getaddrinfo('0.0.0.0', 53)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)

    while True:
        data, addr = s.recvfrom(1024)
        s.sendto(data, addr)
