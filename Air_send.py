#on sub01
import RPi.GPIO as GPIO
import time
import socket
from contextlib import closing
import struct

host = '169.254.26.222' #IP addres
port = 60000 #Port nomber
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket setup

#GPIO nomber define
spi_clk = 11
spi_miso = 9
spi_mosi = 10
spi_cs = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO device setup
GPIO.setup(spi_mosi, GPIO.OUT)
GPIO.setup(spi_miso, GPIO.IN)
GPIO.setup(spi_clk , GPIO.OUT)
GPIO.setup(spi_cs, GPIO.OUT)

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

with closing(sock):
    try:
        while True:
            time.sleep(0.5)
            inputVal0 = readadc(0, spi_clk, spi_mosi, spi_miso , spi_cs)
            vol = inputVal0
            if inputVal0 < 2117:
                vol = 2117 + ( 2117 - inputVal0)
            elif vol > 4095:
                vol = 4095
            send_vol = struct.pack('>d', vol)
            sock.sendto(send_vol, (host, port))

    except KeyboardInterrupt:
        pass

GPIO.cleanup()

