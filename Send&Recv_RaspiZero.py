import RPi.GPIO as GPIO
import time
import socket
from contextlib import closing
import struct
import sys

#Send setup
host = '169.254.26.222' #Raspberry Pi 3B IP addres
send_port = 60000 #Port nomber
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket setup
#Recive setup
recv_ip = ""
recv_port = 60000
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrecv.setblocking(0) #nonblocking recive

#GPIO nomber define
spi_clk = 11
spi_miso = 9
spi_mosi = 10
spi_cs = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO device setup
#ADcon
GPIO.setup(spi_mosi, GPIO.OUT)
GPIO.setup(spi_miso, GPIO.IN)
GPIO.setup(spi_clk , GPIO.OUT)
GPIO.setup(spi_cs, GPIO.OUT)
#finger
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(14,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(6,GPIO.OUT)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3   
    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0

    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

with closing(socksend), closing(sockrecv):
    GPIO.output(6, GPIO.HIGH)
    try:
        count = 0
        vol = 0
        while True:
            inputVal0 = readadc(0, spi_clk, spi_mosi, spi_miso , spi_cs)
            count += 1
            vol += inputVal0
            if count >= 10:
                vol = 4096 - (vol / 10)
                send_str = (str(int(vol)) + ':' + str(GPIO.input(23)) + str(GPIO.input(24)) + str(GPIO.input(4)) + str(GPIO.input(17)) + str(GPIO.input(27)) + str(GPIO.input(22)) + str(GPIO.input(14)) + str(GPIO.input(15))).encode('utf-8')
                # send_vol = struct.pack('>d', vol)
                sock.sendto(send_str, (host, send_port))
                count = 0
                vol = 0
            time.sleep(0.01)


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
