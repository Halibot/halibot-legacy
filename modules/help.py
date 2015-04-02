from module import XMPPModule


class Help(XMPPModule):

	terminate = True

	def help(self, feature):
		if feature != None:
			return 'help: There is no such subfeature to the help module.'
		return 'help: The glorious module that provides you with this glorious help.'

	def handleMessage(self, msg):
		cmds = msg['body'].split(' ')
		if cmds[0] == '!help':
			if len(cmds) == 1:
				message = self.topLevel()
			else:
				mod = None
				cmds[1] = cmds[1].capitalize()
				if cmds[1] in self.xmpp.modules:
					mod = self.xmpp.modules[cmds[1]]

				if mod:
					if len(cmds) == 2:
						message = mod.help(None)
					else:
						message = mod.help(cmds[2])
				else:
					message = 'There is no such module loaded.'
			self.xmpp.reply(msg, message)

	def topLevel(self):
		s = 'halibot help module\n\nUsage: !help [module] [feature]\n\nModules loaded: '
		return s + ", ".join(self.xmpp.modules.keys())
