from module import XMPPModule
from subprocess import check_output as px




class Toys(XMPPModule):
	cowsay = False
	fortune = False
	pom = False
	morse = False
	ppt = False
	bcd = False

	def init(self):
		self.enable_features()

	def help(self, feature):
		d = " [Disabled]"
		if feature in ['cowsay', '!cowsay']:
			return '''
A cowfigurable cow to play with.

usage: !cowsay [arguments to cowsay]
usage: !cowsay <!fortune|!pom>{}
'''.format("\n\nNote: The binary for this could not be found, please install cowsay to use this feature" if not self.cowsay else "")
		if feature in ['bcd', '!bcd']:
			return '''
Displays input as a punch card.

usage: !bcd [arguments to bcd]
usage: !bcd <!fortune|!pom>{}
'''.format("\n\nNote: The binary for this could not be found, please install bcd to use this feature" if not self.bcd else "")
		if feature in ['ppt', '!ppt']:
			return '''
Displays input as a paper tape.

usage: !ppt [arguments to ppt]
usage: !ppt <!fortune|!pom>{}
'''.format("\n\nNote: The binary for this could not be found, please install ppt to use this feature" if not self.ppt else "")
		if feature in ['morse', '!morse']:
			return '''
Displays input as a morse code.

usage: !morse [arguments to morse]
usage: !morse <!fortune|!pom>{}
'''.format("\n\nNote: The binary for this could not be found, please install morse to use this feature" if not self.morse else "")
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
 bcd     - Display input as a punch card.{}
 ppt     - Display input as paper tape.{}
 morse   - Display input as morse code.{}
'''.format(d if not self.cowsay else "",
           d if not self.fortune else "",
           d if not self.pom else "",
           d if not self.bcd else "",
           d if not self.ppt else "",
           d if not self.morse else "")

	def enable_features(self):
		try:
			px(["cowsay", "test"])
			self.cowsay = True
		except:
			self.cowsay = False

		try:
			px(["bcd", "test"])
			self.bcd = True
		except:
			self.bcd = False

		try:
			px(["ppt", "test"])
			self.ppt = True
		except:
			self.ppt = False

		try:
			px(["morse", "test"])
			self.morse = True
		except:
			self.morse = False

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
		return out.rstrip()

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

	def pipable_string(self, string):
		if string == "!fortune":
			string = self.get_fortune()
		if string == "!pom":
			string = self.get_pom()
		return string

	def handle_cowsay(self, string):
		if not self.cowsay or not string:
			return None

		string = self.pipable_string(string)

		try:
			out = px(["cowsay"] + string.split(" "),universal_newlines=True)
		except:
			return None

		return '\n' + out

	def handle_bcd(self, string):
		if not self.bcd or not string:
			return None

		string = self.pipable_string(string)

		try:
			out = px(["bcd"] + string.split(" "),universal_newlines=True)
		except:
			return None

		return '\n' + out

	def handle_ppt(self, string):
		if not self.ppt or not string:
			return None

		string = self.pipable_string(string)

		try:
			out = px(["ppt"] + string.split(" "),universal_newlines=True)
		except:
			return None

		return '\n' + out

	def handle_morse(self, string):
		if not self.morse or not string:
			return None

		string = self.pipable_string(string)

		try:
			out = px(["morse"] + string.split(" "),universal_newlines=True)
		except:
			return None

		return '\n' + out

	commands = {
		"!cowsay":handle_cowsay,
		"!fortune":handle_fortune,
		"!pom":handle_pom,
		"!bcd":handle_bcd,
		"!ppt":handle_ppt,
		"!morse":handle_morse
	}
