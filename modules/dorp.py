from module import XMPPModule
import halutils
import requests
import re

class Dorp(XMPPModule):
	
	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		self.regex = re.compile("Door:\\t(.)")

	def handleMessage(self, msg):
		cmd, args = halutils.splitArgStr(msg)
		if cmd == "!dorp":
			self.xmpp.reply(msg, self.getDorp())

	def getDorp(self):
		r = requests.get("http://k2cc.clarkson.edu:8080")
		if not r.ok:
			return "There was an error getting dorp status"

		m = r.search(r.text)
		if not m:
			return "There was an error parsing the HTML"

		if m.group(1) == "✘":
			return "K2CC is closed :("
		else:
			return "K2CC is open :D"


		
