#!/usr/bin/env python
from db import Database
from datetime import datetime
import re
import select
import socket
import sys
import threading
from time import time
connString = 'postgresql://ctf:14881488@localhost:5432/ctf'

class FlagServer:
	def __init__(self):
		self.host = '0.0.0.0'
		self.port = 14900
		self.server = None
		self.threads = []
		self.backlog = 5
		self.flagpattern = re.compile('^\w{33}=$') # compiled pattern for flag search

	def open_socket(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.host,self.port))
			self.server.settimeout(5)
			self.server.listen(50)
		except socket.error as ex:
			if self.server:
				self.server.close()
			print (">> Could not open socket: " + ex)
			sys.exit(1)

	def run(self):
		self.open_socket()
		input = [self.server,sys.stdin]
		print ('>> listen on {} port'.format(self.port))
		while True:
			try:
				inputready,outputready,exceptready = select.select(input,[],[])
				for s in inputready:

					if s == self.server:
						# handle the server socket
						c = Client(self.server.accept())
						c.start()
						self.threads.append(c)
						print('>> new connection, thread {}.'.format(c.name))
			except (KeyboardInterrupt, SystemExit) as ex:
				print ('>> Exit from keyboard. Shut down server')
				break
		# close all threads
		for c in self.threads:
			c.join()
		self.server.close()

	# def chat_msg_sending(self,msg,msg_sender):
	# 	for c in self.threads:
	# 		if c.client != msg_sender.client:
	# 			c.client.send( str(msg) )

class Client(threading.Thread):
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.client = conn[0]
		self.address = conn[1][0]
		self.client.settimeout(60)
		# print (self.client, self.address, type(self))
		self.send("Hi!")
		try:
			self.team = DB.getTeamByIP(self.address)
			self.send("Welcome, {}! You can send flags now!".format(self.team.name))
		except Exception:
			self.send("Your IP not found! Bye!")
			self.client.close()

	def run(self):
		while True:
			try:
				data = self.recv()
				if data == "":
					print ('>> user {} disconnect'.format(self.name))
					server.threads.remove(self)
					self.client.close()
					break
				# print (data.decode('utf-8'))
				self.check(data)
				# else:
			except socket.error as ex:
				print (">> WARN: Connection closed by peer")
				server.threads.remove(self)
				self.client.close()
	def send(self, data):
		response = bytes("{}\n".format(data), 'ascii')
		self.client.send(response)

	def recv(self, length=1024):
		return str(self.client.recv(length), 'ascii').rstrip()

	def check(self, data):
		"""
		Function for flags checking.

		INPUT:
		Data - string (stripped)

		TODO: Do all checks in database (improve performace)
		"""
		try:
			if not server.flagpattern.match(data):
				self.send("Flag doesn\'t matches pattern: {}".format(server.flagpattern))
				return

			flag = DB.findFlag(data)

			if not flag:
				self.send("Flag not found in DB")
				return
			if self.team.id == flag.team_id:
				self.send("This flag is yours")
				return
			if float(flag.timestamp) <= time():
				self.send("This flag too old")
				return
			if not DB.saveFlag(flag.id, self.team.id):
				self.send("This flag is already stolen by someone")
				return
			self.send("Success")
			return

		except Exception as ex:
			print(ex)
			server.threads.remove(self)
			self.client.close()

if __name__ == "__main__":
	DB = Database(connString)
	server = FlagServer()
	server.run()
