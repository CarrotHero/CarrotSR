import socket #UDP送信
import time
import struct
from contextlib import closing
import os

#送信の設定
host = 192.168.11.20
send_port = 60000
#受信の設定
recv_ip = ""
recv_port = 60000
#2つのsocketを設定
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #送信
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #受信
sockrecv.bind((recv_ip, recv_port)) #socketを登録


with closing(socksend), closing(sockrecv):
	
	try:
		while True:

			#受信
			print("Waiting for receive...")
			data, addr = sockrecv.recvfrom(1024) #受信する dataに文字列が収納
			#--受信するまでここで止まる--
			num = struct.unpack('>i', data)[0] #data(バイト列)を整数型に変換
			if num == 1:
				#Raspi Zeroにデータ送信
				#送信 dataのところは送信したい変数に書き換えてOK
				socksend.sendto(num, (host, send_port))
				break
			elif num == 0:
				#shutdown
				os.system("sudo shutdown -h now")
				break

			
    except KeyboardInterrupt:
        pass
