import socket
import struct
from contextlib import closing
UDP_IP = ""
UDP_PORT = 60000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
with closing(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(data)

