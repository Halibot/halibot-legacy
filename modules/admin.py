from module import XMPPModule

class Admin(XMPPModule):

	terminate = True

	def recvMsg(self, msg):
		if self.xmpp.isadmin(jid=msg["from"].bare):
			self.handleMessage(msg)
		else:
			return

	def recvGroupMsg(self, msg):
		if self.xmpp.isadmin(room=msg["from"].bare, nick=msg["mucnick"]):
			self.handleMessage(msg)
		else:
			return

	def handleMessage(self, msg):
		cmd, string = (msg["body"].split(" ")[0], " ".join(msg["body"].split(" ")[1:]))
		if cmd == "!reloadmodules":
			mods = self.xmpp.load_modules()
			self.xmpp.reply(msg, "Modules reloaded successfully! Registered modules: " + ", ".join(mods))

	def help(self, feature):
		if feature == None:
			return '''
Admin module provides methods to manage the Bot while it is live.
 Features:
   !reloadmodules - Stop all modules, and reload all enabled modules'''
