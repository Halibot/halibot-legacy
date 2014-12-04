#!/usr/bin/env python3
import inspect
import os
import imp
import logging
import time
import json
import getpass

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from module import XMPPModule

admins = []

import sys
sys.path.append(".")
import module


def loadConfig():
	global admins
	with open("config.json","r") as f:
		data = json.loads(f.read())

	admins = data["admins"] if "admins" in data.keys() else []	
	pwd = getpass.getpass()
	jid = data["jid"] if "jid" in data.keys() else None # TODO: Make this an error
	rooms = []
	if "muc" in data.keys():
		for r in data["muc"]:
			rooms.append((r["room"],r["nick"]))
	return (jid,pwd,rooms)



class Bot(ClientXMPP):

	modules = []

	def __init__(self, jid, password, rooms):
		ClientXMPP.__init__(self,jid,password)
	
		self.load_modules()
	
		self.rooms = rooms

		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("groupchat_message", self.groupmsg)

	def load_modules(self):
		# TODO: Put this dir in config?
		self.modules = []
		mods = []
		names = []
		for f in os.listdir("./modules"): 
			if f[-2:] != "py":
				continue
			file,pathname,description = imp.find_module("./modules/" + f[:-3])
			mods.append(imp.load_module(f[:-3],file,pathname,description))

		for m in mods:
			for name, obj in inspect.getmembers(m):
				if inspect.isclass(obj) and issubclass(obj,XMPPModule) and name != "XMPPModule":
					self.modules.append(obj(self))	
					names.append(name)
		return names

	def session_start(self, event):
		self.send_presence()
		for r in self.rooms:
			self.plugin['xep_0045'].joinMUC(r[0], r[1], wait=True)
		
		# self.get_roster()

	def message(self, msg):
		if msg['type'] not in ('chat', 'normal'):
			return

		for m in self.modules:
			try:
				m.recvMsg(msg)
			except Exception as e:
				print(e)

	def groupmsg(self, msg):
		if msg['type'] not in ("groupchat") or msg['mucnick'] in [n[1] for n in self.rooms]:
			return

		for m in self.modules:
			try:
				m.recvGroupMsg(msg)
			except Exception as e:
				print(e)

	def sendMsg(self, to, text):
		self.send_message(mto=to, mbody=text, mtype="chat")

	def sendGroupMsg(self, to, text):
		self.send_message(mto=to, mbody=text, mtype="groupchat")
	
	def reply(self, msg, string):
		if msg['type'] in ("chat", "normal"):
			self.sendMsg(msg['from'].bare, string)
		elif msg['type'] in ("groupchat"):
			self.sendGroupMsg(msg['from'].bare, string)
		else:
			print("Error replying")

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
	
	jid,pwd,rooms = loadConfig()

	xmpp = Bot(jid, pwd, rooms)
	xmpp.register_plugin('xep_0045')
	xmpp.connect()
	xmpp.process(block=True)
