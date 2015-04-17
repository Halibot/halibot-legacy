from module import XMPPModule

class Admin(XMPPModule):

	def handleMessage(self, msg):
		cmd, string = (msg["body"].split(" ")[0], " ".join(msg["body"].split(" ")[1:]))
		if cmd == "!reloadmodules" and self.xmpp.isadmin(msg=msg):
			mods = self.xmpp.load_modules()
			self.xmpp.reply(msg, "Modules reloaded successfully! Registered modules: " + ", ".join(mods))

	def help(self, feature):
		if feature == None:
			return '''
Admin module provides methods to manage the Bot while it is live.
 Features:
   !reloadmodules - Stop all modules, and reload all enabled modules'''
