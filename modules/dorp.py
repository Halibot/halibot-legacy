from module import XMPPModule
import halutils
import requests

class Dorp(XMPPModule):
	
	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		self.regex = re.compile("Door:\\t(.)")

	def handleMessage(self, msg):
		cmd, args = halutils.splitArgStr(msg)
		if cmd == "!dorp":
			self.xmpp.reply(msg, self.getDorp())

	def getDorp(self):
		r = requests.get("http://k2cc.clarkson.edu:8080/get")
		if not r.ok:
			return "There was an error getting dorp status"

		return "The K2CC door is {door} and the light is {light}".format(**r.json())

		
