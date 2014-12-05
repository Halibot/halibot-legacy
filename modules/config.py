from module import XMPPModule

class Config(XMPPModule):
	def handleMessage(self, msg):
		if self.xmpp.isadmin(msg=msg):
			cmd,args = (msg['body'].split(" ",1)[0], msg['body'].split(" ")[1:])
			if cmd == "!config" and len(args) >= 1:
				if args[0] == "enable":
					if args[1] not in self.xmpp.config["modules"]:
						self.xmpp.config["modules"].append(args[1])
						self.xmpp.reply(msg, "Enabled " + args[1])
				elif args[0] == "disable":
					self.xmpp.config["modules"] = [m for m in self.xmpp.config["modules"] if m != args[1]]
					self.xmpp.reply(msg, "Disabled " + args[1])
				elif args[0] == "write":
					try:
						self.xmpp.write_config()
					except:
						self.xmpp.reply(msg, "Error writing config :(")
						return
					self.xmpp.reply(msg, "Wrote config successfully!")
				elif args[0] == "reload":
					try:
						self.xmpp.load_config()
					except:
						self.xmpp.reply(msg, "Error reloading config :(")
						return
					self.xmpp.reply(msg, "Reloaded config successfully!")
