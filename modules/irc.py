from module import XMPPModule
import pydle, threading

class IrcClient(pydle.Client):

	module = None

	def on_connect(self):
		super().on_connect()
		self.join(self.module.xmpp.config['irc']['channel'])

	def on_channel_message(self, target, by, msg):
		self.module.ircRecv(by, msg)

	def on_xmpp_msg(self, user, msg):
		self.message(self.module.xmpp.config['irc']['channel'], "<XMPP> {}: {}".format(user,msg))

	
class Irc(XMPPModule):

	bot = None
	thread = None
	priority = 100

	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		self.bot = IrcClient(self.xmpp.config['irc']['nick'])
		self.bot.connect(self.xmpp.config['irc']['server'], port=self.xmpp.config['irc']['port'])
		self.bot.module = self
	
		self._create_thread()

	def _create_thread(self):
		self.thread = threading.Thread(target=self.bot.handle_forever)
		self.thread.start()

	# TODO: Relay messages from IRC to XMPP
	def ircRecv(self, by, msg):
		self.xmpp.sendGroupMsg(self.xmpp.config['irc']['muc'],"<IRC> {}: {}".format(by,msg))

	def recvGroupMsg(self, msg):
		string = msg['body']
		name = msg['mucnick']

		self.bot.on_xmpp_msg(name, string)	

	def help(self, feature):
		return '''Irc: Unifies an IRC channel and an XMPP server. All messages sent to either is relayed to the other.'''
