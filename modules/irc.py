from module import XMPPModule
import pydle, threading, halutils

class IrcClient(pydle.Client):

	module = None

	def on_connect(self):
		super().on_connect()
		self.join(self.module.xmpp.config['irc']['channel'])

	def on_channel_message(self, target, by, msg):
		if msg.startswith("!list"):
			self.message(self.module.xmpp.config['irc']['channel'], "\n".join(self.module.xmpp.mucusers[self.module.xmpp.config['irc']['muc']].keys()))
			return

		self.module.ircRecv(by, msg)

	def on_xmpp_msg(self, user, msg):
		self.message(self.module.xmpp.config['irc']['channel'], "<xmpp-{}>: {}".format(user,msg))

	
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
		self.xmpp.sendGroupMsg(self.xmpp.config['irc']['muc'],"<irc-{}>: {}".format(by,msg))

	def recvGroupMsg(self, msg):
		string = msg['body']
		name = msg['mucnick']

		if string.startswith("!irc"):
			foo, args = halutils.splitArgList(msg)
			if args[0] == "list":
				self.xmpp.reply(msg, "\n" + "\n".join(self.bot.channels[self.xmpp.config['irc']['channel']]['users']))
			return


		self.bot.on_xmpp_msg(name, string)	

	def help(self, feature):
		return '''Irc: Unifies an IRC channel and an XMPP server. All messages sent to either is relayed to the other.

Usage: Just talk, or use !irc to interact with the irc side, sorta.
 !irc list - get a list of the nicknames on the IRC channel'''
