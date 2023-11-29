# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1,write_timeout=0)
def read_com():
	arduino.flush()
	arduino.write(bytes("TRIG:IMM", 'utf-8'))
	data=""
	while(data==""):
		data = arduino.readline()
	return data.decode().replace("\r\n","")