import socket #UDP
import time
import struct
from contextlib import closing
import os


host = "192.168.11.10"
send_port = 60000

recv_ip = ""
recv_port = 60000

socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrecv.bind((recv_ip, recv_port))


with closing(socksend), closing(sockrecv):
	
        try:
            while True:
                print("Waiting for receive...")
                data, addr = sockrecv.recvfrom(1024) 
                num = struct.unpack('>i', data)[0]
                if num == 1:
                    send_num = struct.pack('>i', num)
                    socksend.sendto(send_num, (host, send_port))
                    break
                elif num == 0:
                    #shutdown
                    os.system("sudo shutdown -h now")
                    break
        except KeyboardInterrupt:
            pass
