class XMPPModule():
	xmpp = None
	threadfunc = None
	priority = 0
	terminate = False


	# Default constructor. Try to avoid overriding __init__, use init() instead
	def __init__(self, xmpp):
		self.xmpp = xmpp

	# Initialize the module. Use this, do not override __init__
	def init(self):
		pass

	# User-implemented deconstructor called when a module is unloaded
	def deinit(self):
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
