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


import sys
sys.path.append(".")
import module


class Bot(ClientXMPP):

	jid = ""
	rooms = []
	modules = []
	config = None
	mucusers = {}

	def __init__(self, pwd):
		self.load_config()

		ClientXMPP.__init__(self,self.jid,pwd)

		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("groupchat_message", self.groupmsg)
		self.add_event_handler("groupchat_presence", self.muc_presence)


		self.load_modules()


	def load_config(self):
		with open("config.json","r") as f:
			self.config = json.loads(f.read())

		self.jid = self.config["jid"] if "jid" in self.config.keys() else None # TODO: Make this an error

		self.rooms = []
		if "muc" in self.config.keys():
			for r in self.config["muc"]:
				self.rooms.append((r["room"],r["nick"]))
				self.mucusers[r["room"]] = {}

	def write_config(self):
		with open("config.json", "w") as f:
			f.write(json.dumps(self.config, indent=4, sort_keys=True))

	def load_modules(self):
		# TODO: Put this dir in config?
		self.modules = []
		mods = []
		names = []
		for f in os.listdir("./modules"):
			if f[-2:] != "py":
				continue
			file,pathname,description = imp.find_module("./modules/" + f[:-3])
			try:
				mods.append(imp.load_module(f[:-3],file,pathname,description))
			except Exception as e:
				print(e)

		for m in mods:
			for name, obj in inspect.getmembers(m):
				if inspect.isclass(obj) and issubclass(obj,XMPPModule) and name != "XMPPModule" and name in self.config["modules"]:
					self.modules.append(obj(self))
					names.append(name)
		return names

	def muc_presence(self, presence):
		if presence['muc']['jid'] == self.jid:
			return
		self.mucusers[presence['muc']['room']][presence['muc']['nick']] = presence['muc']['jid'].bare
		
		for m in self.modules:
			try:
				m.handleMucPresence(presence)
			except Exception as e:
				print(e)

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

	def isadmin(self, jid=None, nick=None, room=None, msg=None):
		if msg:
			if "mucnick" in msg.keys():
				name = self.mucusers[msg['mucroom']][msg["mucnick"]]
			else:
				name = msg["jid"]
	
		elif jid:
			name = jid
		elif nick and room:
			name = self.mucusers[room][nick]
		else:
			print("isadmin check failed")
			raise Exception("Improper use of isadmin")
		return name in self.config["admins"]

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

	xmpp = Bot(getpass.getpass())
	xmpp.register_plugin('xep_0045')
	xmpp.connect()
	xmpp.process(block=True)
