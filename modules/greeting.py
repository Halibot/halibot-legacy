from module import XMPPModule

class Greeting(XMPPModule):
	greetings = {}

	def help(self, string):
		if string in ["!greeting", "greeting"]:
			return '''
usage: !greeting <string>

Print the <string> when you join the chat room.
'''

		return '''
Set a custom greeting for yourself when you join the chatroom.
 Feature:
   !greeting - Set your greeting
'''


	def __init__(self, xmpp):
		XMPPModule.__init__(self,xmpp)
		for r in self.xmpp.rooms:
			self.greetings[r[0]] = {}

		print(self.greetings)
	def handleMucPresence(self, presence):
		if "join" not in presence['id']:
			return

		if presence['muc']['nick'] in self.greetings[presence['muc']['room']].keys():
			self.xmpp.sendGroupMsg(presence['muc']['room'], self.greetings[presence['muc']['room']][presence['muc']['nick']])

	def recvGroupMsg(self, msg):
		body = msg['body']
		if body.startswith("!greeting"):
			self.greetings[msg['mucroom']][msg["mucnick"]] = body.split(" ",1)[1]
			self.xmpp.reply(msg, "Greeting set!")
