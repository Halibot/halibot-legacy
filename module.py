class XMPPModule():
	xmpp = None
	threadfunc = None


	# Initialize the module, start any passive threads here
	def __init__(self, xmpp):
		self.xmpp = xmpp

	# Start the passive thread if one is set
	def start(self):
		pass

	# Stop the passive thread
	def stop(self):
		pass

	# Called when a message is received. Passes in whole message object
	def recvMsg(self, msg):
		self.handleMessage(msg)

	# Called when a group message is received, useful for early separation
	def recvGroupMsg(self, msg):
		self.handleMessage(msg)

	# Default, handle all messages the same
	def handleMessage(self, msg):
		pass

	# Put some functionality on users sending a presence to a MUC
	def handleMucPresence(self, presence):
		pass

	# Default help method
	def help(self, bloop):
		return 'This module does not implement a help method.'

