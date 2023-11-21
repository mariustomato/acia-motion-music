# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
def read_com():
	arduino.write(bytes("TRIG:IMM", 'utf-8'))
	time.sleep(0.05)
	data = arduino.readline()
	return data