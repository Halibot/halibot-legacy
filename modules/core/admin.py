from module import XMPPModule
import halutils

class Admin(XMPPModule):

	def handleMessage(self, msg):
		cmd, args = halutils.splitArgList(msg)
		if cmd == "!reloadmodules" and self.xmpp.isadmin(msg=msg):
			mods = self.xmpp.load_modules()
			self.xmpp.reply(msg, "Modules reloaded successfully! Registered modules: " + ", ".join(mods))
		elif cmd == "!load":
			if len(args) == 0:
				self.xmpp.reply(msg, "Please supply names of modules to load!")
				return
			for m in args:
				if self.xmpp.load_module(m):
					self.xmpp.reply(msg, "Successfully loaded " + m)
				else:
					self.xmpp.reply(msg, "Failed to load " + m)
		elif cmd == "!unload":
			if len(args) == 0:
				self.xmpp.reply(msg, "Please supply names of modules to unload!")
				return
			for m in args:
				if self.xmpp.unload_module(m):
					self.xmpp.reply(msg, "Successfully unloaded " + m)
				else:
					self.xmpp.reply(msg, "Failed to unload " + m)

	def help(self, feature):
		if feature == None:
			return '''
Admin module provides methods to manage the Bot while it is live.
 Features:
   !reloadmodules - Stop all modules, and reload all enabled modules'''
