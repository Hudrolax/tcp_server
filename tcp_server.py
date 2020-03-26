# Golden1 branch

import socket
import os
import psutil
from time import sleep
from datetime import datetime
import threading

OWN_TCP_SERVER_ADDRESS = ('', 8686)
cpu_percent = 0
virtual_memory = 0
starttime = datetime.now() 

def DifferenceBetweenDate(date1,date2):
	duration = date2 - date1
	duration_in_s = duration.total_seconds() # Total number of seconds between dates
	days = divmod(duration_in_s, 86400)        # Get days (without [0]!)
	hours = divmod(days[1], 3600)               # Use remainder of days to calc hours
	minutes = divmod(hours[1], 60)                # Use remainder of hours to calc minutes
	seconds = divmod(minutes[1], 1)               # Use remainder of minutes to calc seconds
	return "%d days, %d hours, %d mins %d sec" % (days[0], hours[0], minutes[0], seconds[0]) 

def ClerStr(str_):
	str_ = str(str_)
	str_ = str_.replace("\\r\\n",'')
	str_ = str_.replace("b'",'')
	str_ = str_.replace("'",'')
	return str_
	
def TCPServer():
	# Настраиваем сокет
	global cpu_percent
	global virtual_memory
	global starttime

	server_socket = socket.socket()
	server_socket.bind(OWN_TCP_SERVER_ADDRESS)
	server_socket.listen(1)
	while True:
		# Обработка событий TCP сервера
		connection, address = server_socket.accept()
		print("new connection from {address}".format(address=address))
		data = ClerStr(connection.recv(1024))
		print(data)
		answer = 'unknown command'
		if data == 'ping':
			answer = 'ping'
		elif data.startswith('reboot'):
			arr = data.split(' ')
			delay = 5
			try:
				if len(arr)>1:
					delay=int(arr[1])
				answer = 'shutdown /r /t '+str(delay)
				os.system(answer)	
			except:
				answer = 'error int(arr[1])'
		elif data.startswith('shutdown'):
			arr = data.split(' ')
			delay = 5
			try:
				if len(arr)>1:
					delay=int(arr[1])
				answer = 'shutdown /s /t '+str(delay)
				os.system(answer)	
			except:
				answer = 'error int(arr[1])'
		elif data == 'cpu_percent':
			answer = str(cpu_percent)
		elif data == 'virtual_memory':
			answer = str(virtual_memory)
		elif data == 'uptime':
			answer = str(DifferenceBetweenDate(starttime,datetime.now()))									
				
		connection.send(bytes(answer, encoding='UTF-8'))
		connection.close()

TCPServerThread = threading.Thread(target=TCPServer, args=(), daemon=True)
TCPServerThread.start()

while True:
	cpu_percent = psutil.cpu_percent(interval=5)
	virtual_memory = psutil.virtual_memory()[2]
	sleep(5)