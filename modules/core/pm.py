from module import XMPPModule
import halutils
import os

class PackageManager(XMPPModule):
	
	def handleMessage(self, msg):
		cmd, args = halutils.splitArgList(msg)

		if cmd == "!pm":
			if not self.xmpp.isadmin(msg=msg) or True:
				self.xmpp.reply(msg, "You are not authorized to manage modules")
				return
			if args[0] not in self.commands:
				self.xmpp.reply(msg, "I do not know how to '{}'".format(arg[0]))
				return
			self.commands[args[0]](self, msg, args[1:])

	def _install(self, msg, args):
		if len(args) == 0:
			self.xmpp.reply(msg, "Need to supply a github repo name, or url to a git repository")
			return

		self.xmpp.reply(msg, "Attempting to install a module from '{}'...".format(args[0]))

		os.chdir('./modules')
		repo = args[0]
		try:
			if repo.startswith("http"):
				os.system("git clone {}".format(repo))
			else:
				os.system("git clone https://github.com/{}".format(repo))
			self.xmpp.reply(msg, "Module installed successfully, be sure to enable it in the config and load it")
		except:
			self.xmpp.reply(msg, "Failed to install new module")
		os.chdir('..')

	def _remove(self, msg, args):
		if len(args) == 0:
			self.xmpp.reply(msg, "Need to supply a module group name to remove (i.e. directory name in modules/)")
			return
		os.chdir('./modules')
		for a in args:
			try:
				os.system("rm -rf " + a)
				self.xmpp.reply(msg, "Successfully deleted '{}'".format(a))
			except:
				self.xmpp.reply(msg, "Failed to remove '{}'".format(str(a)))

		os.chdir('..')

	# TODO: Support updating or something

	commands = {
		"install": _install,
		"remove": _remove
	}
			
