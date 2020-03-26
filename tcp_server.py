# Node1 branch

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

def KillMetaTrader5Process():
	if datetime.now().hour == 8 and datetime.now().minute == 1:
		for proc in psutil.process_iter():
			if proc.name() == 'metatester64.exe':
				proc.kill() 

def DifferenceBetweenDate(date1,date2):
	duration = date2 - date1
	duration_in_s = duration.total_seconds() # Total number of seconds between dates
	days = divmod(duration_in_s, 86400)        # Get days (without [0]!)
	hours = divmod(days[1], 3600)               # Use remainder of days to calc hours
	minutes = divmod(hours[1], 60)                # Use remainder of hours to calc minutes
	seconds = divmod(minutes[1], 1)               # Use remainder of minutes to calc seconds
	return "%d days, %d hours, %d mins %d sec" % (days[0], hours[0], minutes[0], seconds[0])

def DifferenceBetweenDateSec(date1,date2):
	duration = date2 - date1
	return duration.total_seconds() # Total number of seconds between dates

class BaseBackup_class():
	def __init__(self,name,path,file_prefix,Expiration):
		self.name = name
		self.path = path
		self.file_prefix = file_prefix
		self.Expiration = Expiration
	
	def modification_date(self,filename):
		t = os.path.getmtime(filename)
		return datetime.fromtimestamp(t)

	def last_file_in_list(self,file_list):
		backups_time = []
		for file in file_list:
			backups_time.append(self.modification_date(self.path+'\\'+file))
		return max(backups_time)	

	def get_last_backup_date(self):
		dirs = os.listdir(self.path)
		file_list = []
		for file in dirs:
			if file.find(self.file_prefix)>-1:
				file_list.append(file)
		return self.last_file_in_list(file_list)

	def get_last_backup_name(self):
		dirs = os.listdir(self.path)
		file_list = []
		for file in dirs:
			if file.find(self.file_prefix)>-1:
				file_list.append(file)
		last_date = self.last_file_in_list(file_list)
		for file in dirs:
			if self.modification_date(self.path+'\\'+file) == last_date:
				return file			
		return None

	def get_last_backup_timediff(self):
		last_backup = self.get_last_backup_date()
		return DifferenceBetweenDateSec(last_backup,datetime.now())

	def get_last_backup_ctimediff(self):
		last_backup = self.get_last_backup_date()
		return DifferenceBetweenDate(last_backup,datetime.now())

	def backup_expiration_bool(self):
		if DifferenceBetweenDateSec(self.get_last_backup_date(),datetime.now()) > self.Expiration and datetime.now().isoweekday() != 1:
			return True
		else:
			return False
#									(name,path,file_prefix,time expiration in sec)
Trade2019backupFull = BaseBackup_class('Trade2019full','f:\\backup\\full','Trade2019_backup_',612000)
Trade2019backupDiff = BaseBackup_class('Trade2019diff','f:\\backup\\Diff\\Trade2019','Trade2019_backup_',90000)
BuhBackupFull = BaseBackup_class('BuhFull','f:\\backup\\full','buh_backup_',612000)
BuhBackupDiff = BaseBackup_class('BuhDiff','f:\\backup\\Diff\\buh','buh_backup_',90000)
ZupBackupFull = BaseBackup_class('ZupFull','f:\\backup\\full','zup_backup_',612000)
ZupBackupDiff = BaseBackup_class('ZupDiff','f:\\backup\\Diff\\zup','zup_backup_',90000)
UATBackupFull = BaseBackup_class('UATFull','f:\\backup\\full','UAT_backup_',612000)
UATBackupDiff = BaseBackup_class('UATDiff','f:\\backup\\Diff\\uat','UAT_backup_',90000)

backup_base_list = [Trade2019backupFull,Trade2019backupDiff,BuhBackupFull,BuhBackupDiff,ZupBackupFull,ZupBackupDiff,UATBackupFull,UATBackupDiff]					 

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
		try:
			# Обработка событий TCP сервера
			connection, address = server_socket.accept()
			print("new connection from {address}".format(address=address))
			data = ClerStr(connection.recv(1024))
			print(f'data: {data}')
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
			elif data.find('get_last_backup_timediff') > -1:
				split = data.split(' ')
				basename = split[1]
				finded = False
				for base in backup_base_list:
					if base.name == basename:
						answer = str(base.get_last_backup_timediff())
						finded = True
						break
				if not finded:
					answer = 'unknown base name'
			elif data.find('get_last_backup_ctimediff') > -1:
				split = data.split(' ')
				basename = split[1]
				finded = False
				for base in backup_base_list:
					if base.name == basename:
						answer = str(base.get_last_backup_ctimediff())
						finded = True
						break
				if not finded:
					answer = 'unknown base name'
			elif data.find('backup_expiration_bool') > -1:
				split = data.split(' ')
				basename = split[1]
				finded = False
				for base in backup_base_list:
					if base.name == basename:
						answer = str(base.backup_expiration_bool())
						finded = True
						break
				if not finded:
					answer = 'unknown base name'
			elif data.find('get_last_backup_name') > -1:
				split = data.split(' ')
				basename = split[1]
				finded = False
				for base in backup_base_list:
					if base.name == basename:
						answer = str(base.get_last_backup_name())
						finded = True
						break
				if not finded:
					answer = 'unknown base name'
			elif data.find('get_last_backup_date') > -1:
				split = data.split(' ')
				basename = split[1]
				finded = False
				for base in backup_base_list:
					if base.name == basename:
						answer = str(base.get_last_backup_date())
						finded = True
						break
				if not finded:
					answer = 'unknown base name'								
			else:
				answer = 'unknown command'														
					
			connection.send(bytes(answer, encoding='UTF-8'))
			connection.close()
		except:
			pass
		sleep(0.5)		

TCPServerThread = threading.Thread(target=TCPServer, args=(), daemon=True)
TCPServerThread.start()

while True:
	cpu_percent = psutil.cpu_percent(interval=5)
	virtual_memory = psutil.virtual_memory()[2]
	KillMetaTrader5Process()
	sleep(5)