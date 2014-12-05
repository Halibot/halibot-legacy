from module import XMPPModule

def topLevel(xmpp):
	s = 'halibot help module\n\nUsage: !help [module] [feature]\n\nModules loaded: '
	return s + ", ".join([m.__class__.__name__ for m in xmpp.modules])

class Help(XMPPModule):
	def help(self, feature):
		if feature != None:
			return 'help: There is no such subfeature to the help module.'
		return 'help: The glorious module that provides you with this glorious help.'

	def handleMessage(self, msg):
		cmds = msg['body'].split(' ')
		if cmds[0] == '!help':
			if len(cmds) == 1:
				message = topLevel(self.xmpp)
			else:
				mod = None
				for m in self.xmpp.modules:
					if cmds[1].lower() == m.__class__.__name__.lower():
						mod = m
						break
				if mod:
					if len(cmds) == 2:
						message = mod.help(None)
					else:
						message = mod.help(cmds[2])
				else:
					message = 'There is no such module loaded.'
			self.xmpp.reply(msg, message)

