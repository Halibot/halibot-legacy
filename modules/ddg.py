from module import XMPPModule
import requests

class Ddg(XMPPModule):
	
	def help(self, feature):
		return '''
Searches DuckDuckGo for a phrase.

usage: !ddg [phrase...]
'''

	def handleMessage(self, msg):
		if msg['body'].split(' ')[0] == '!ddg':
			string = ' '.join(msg['body'].split(' ')[1:])

			if string == '':
				self.xmpp.reply(msg, "It is kind of hard to search for nothing...")
				return

			r = requests.get("http://api.duckduckgo.com/?q={}&format=json&no_html=1".format(string))
			if r.status_code == 200:
				if r.json()['Abstract'] != '':
					self.xmpp.reply(msg, r.json()['Abstract'])
				else:
					self.xmpp.reply(msg, "No result found :(")
			else:
				self.xmpp.reply(msg, "I cannot quack, I can only cry")

