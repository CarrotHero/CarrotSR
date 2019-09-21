import RPi.GPIO as GPIO
import time
import socket
from contextlib import closing
import struct
import sys

#Send setup
host = '169.254.181.155' #Raspberry Pi 3B IP addres
send_port = 60000 #Port nomber
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket setup
#Recive setup
recv_ip = ""
recv_port = 60000
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketrecv.bind((recv_ip, recv_port)) #socketを登録
sockrecv.setblocking(0) #nonblocking recive

with closing(socksend), closing(sockrecv):
    try:
        num = input()
        while True:
            # send_vol = struct.pack('>d', vol)
            sock.sendto(int(num), (host, send_port))

            time.sleep(0.1)
            #PlayStop Wait
            try:
                data, addr = sockrecv.recvfrom(1024)
            except socket.errot:
                pass
            else:
                GPIO.cleanup()
                sys.exit()

    except KeyboardInterrupt:
        pass

GPIO.cleanup()
