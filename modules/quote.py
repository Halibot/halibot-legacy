from module import XMPPModule
import random
import os


class Quotes(XMPPModule):

	quotes = []

	def init(self):
		self.loadquotes()

	def loadquotes(self):
		with open("quotes.txt", "r") as f:
			self.quotes = f.read().splitlines()

	def handleMessage(self, msg):
		cmd, string = (msg['body'].split(' ',1)[0], " ".join(msg['body'].split(' ',1)[1:]))
		if cmd in self.commands.keys():
			self.xmpp.reply(msg, self.commands[cmd](self,string))
		elif cmd in self.admincommands.keys() and self.xmpp.isadmin(msg=msg):
			self.xmpp.reply(msg, self.admincommands[cmd](self, string))

	def quote_handler(self, string):
		if len(self.quotes) == 0:
			return "Error: quotes.txt wasn't initialized properly?"
		if string == None:
			return self.quotes[random.randint(0, len(self.quotes)-1)]
		temp = [q for q in self.quotes if string.lower() in q.lower()]
		if len(temp) == 0:
			return "No quotes match your string"
		return temp[random.randint(0, len(temp)-1)]

	def quoteadd_handler(self, string):
		if string == None:
			return "No quote supplied!"
		if len(self.quotes) >= 50:
			return "Too many quotes in the buffer, sorry :("
		self.quotes.append(string)
		return "Added! :)"

	def writequotes_handler(self, string):
		try:
			with open("quotes.txt","w") as f:
				f.write("\n".join(self.quotes))
		except:
			return "Could not write to 'quotes.txt', sorry..."
		return "Updated 'quotes.txt'!"


	commands = {
		"!quote":quote_handler,
		"!quoteadd":quoteadd_handler
	}
	admincommands = {
		"!writequotes":writequotes_handler,
		"!reloadquotes":loadquotes
	}

	def help(self, feature):
		if feature in ["!quote", "quote"]:
			return '''
Usage: !quote [string]

Respond with a random quote from "quotes.txt". Providing an optional string reduces the pool to only quotes containing that substring.
'''
		elif feature in ["!quoteadd", "quoteadd"]:
			return '''
Usage !quoteadd <string>

Add the <string> to the internal list of quotes. Note, this does not persist if the module is reloaded. Be sure to !writequotes to persist new quotes!
'''

		return '''
Fill your chat with random quotes from a file.
 Features:
   !quote    - Print a random quote
   !quoteadd - Add a quote to the internal quote database
'''
