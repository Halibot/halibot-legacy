from module import XMPPModule
import cleverbot

class Cleverbot(XMPPModule):
	
	sessions = []
	c = None

	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		c = cleverbot.Cleverbot()


	def recvMessage(self, msg):
		if msg['body'].startswith("!cleverbot "):
			arg = msg['body'].split(" ")[1]
			if arg == "enable":
				if msg['from'] in self.sessions:
					return
				self.sessions.append(msg['from'])
			elif arg == "disable":
				self.sessions = [s for s in self.sessions if s != msg['from']]

		elif msg['from'] in sessions:
			self.xmpp.reply(msg, c.ask(msg['body']))
