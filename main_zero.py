import RPi.GPIO as GPIO
import time
import socket
from contextlib import closing
import struct
import sys
import os


#Send setup
host = '169.254.56.166'
sendport = 60000
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Recive setup
recvip = ""
recvport = 60000
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrecv.bind((recvip, recvport))
#sockrecv.setblocking(0)

with closing(socksend), closing(sockrecv):
    try:
        while True:
            data, addr = sockrecv.recvfrom(1024)
            num = struct.unpack('>i', data)[0]
            if num == 1:
                #Recorder.py do
            elif num == 0:
                os.system("sudo shutdown -h now")
                break
    except KeyboardInterrupt:
        pass
 
