from module import XMPPModule
from subprocess import check_output as px




class Toys(XMPPModule):
	cowsay = False
	fortune = False
	pom = False


	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		self.enable_features()

	def help(self, feature):
		d = " [Disabled]"
		if feature in ['cowsay', '!cowsay']:
			return '''
A cowfigurable cow to play with.

usage: !cowsay [arguments to cowsay]
usage: !cowsay <!fortune|!pom>{}
'''.format("\n\nNote: The binary for this could not be found, please install cowsay to use this feature" if not self.cowsay else "")
		if feature in ['fortune', '!fortune']:
			return '''
Forsees the future.

usage: !fortune{}
'''.format("\n\nNote: The binary for this could not be found, please install fortune to use this feature" if not self.fortune else "")
		if feature in ['pom', '!pom']:
			return '''
The current phase of the moon.

usage: !pom
'''.format("\n\nNote: The binary for this could not be found, please install pom to use this feature" if not self.pom else "")

		return '''
A modules to provides some nice toys to play with.

Module features:
 cowsay  - A configurable cow to play with.abs{}
 fortune - Forsees the future.{}
 pom     - The current phase of the moon.{}
'''.format(d if not self.cowsay else "",
           d if not self.fortune else "",
           d if not self.pom else "")

	def enable_features(self):
		try:
			px(["cowsay", "test"])
			self.cowsay = True
		except:
			self.cowsday = False

		try:
			px(["fortune"])
			self.fortune = True
		except:
			self.fortune = False

		try:
			px(["pom"])
			self.pom = True
		except:
			self.pom = False

	def handleMessage(self, msg):
		command, string = (msg['body'].split(" ")[0]," ".join(msg['body'].split(' ')[1:]))
		if command in self.commands.keys():
			reply = self.commands[command](self, string)
			self.xmpp.reply(msg, reply) if reply else None

	def get_fortune(self):
		if not self.fortune:
			return None
		try:
			out = px("fortune",universal_newlines=True)
		except:
			return None
		return out

	def get_pom(self):
		if not self.pom:
			return None
		try:
			out = px("pom",universal_newlines=True)
		except:
			return None
		return out

	def handle_fortune(self, string):
		return self.get_fortune()

	def handle_pom(self, string):
		return self.get_pom()

	def handle_cowsay(self, string):
		if not self.cowsay or not string:
			return None

		if string == "!fortune":
			string = self.get_fortune()
			if string == None:
				return None
		if string == "!pom":
			string = self.get_pom()
			if string == None:
				return None

		try:
			out = px(["cowsay"] + string.split(" "),universal_newlines=True)
		except:
			return None

		return '\n' + out

	commands = {
		"!cowsay":handle_cowsay,
		"!fortune":handle_fortune,
		"!pom":handle_pom
	}
