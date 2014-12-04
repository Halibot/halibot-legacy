from module import XMPPModule

def relmod(xmpp, to):
	mods = xmpp.load_modules()
	xmpp.sendMsg(to, "Modules reloaded successfully! Registered modules: " + ", ".join(mods))

class Admin(XMPPModule):
	
	commands = {
		"!reloadmodules":relmod
	}

	def recvMsg(self, msg):
		if msg['body'].split(" ")[0] in self.commands.keys():
			self.commands[msg['body'].split(" ")[0]](self.xmpp, msg['from'].bare)
			

	def recvGroupMsg(self, msg):
		if msg['body'] == "Hello World!":
			self.xmpp.sendGroupMsg(msg['from'].bare, "Hello World!")
