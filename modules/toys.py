from module import XMPPModule
from subprocess import check_output as px

def get_fortune():
	try:
		out = px("fortune",universal_newlines=True)
	except:
		return None

	return out

def handle_fortune(string):
	return get_fortune()

def handle_cowsay(string):
	if string == None:
		return None

	if string == "!fortune":
		string = get_fortune()
		if string == None:
			return None

	try:
		out = px(["cowsay"] + string.split(" "),universal_newlines=True)
	except:
		return None

	return '\n' + out


class Toys(XMPPModule):

	def handleMessage(self, msg):
		command, string = (msg['body'].split(" ")[0]," ".join(msg['body'].split(' ')[1:]))
		if command in commands.keys():
			self.xmpp.reply(msg,commands[command](string))

commands = {
	"!cowsay":handle_cowsay,
	"!fortune":handle_fortune
}
