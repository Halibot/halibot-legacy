from module import XMPPModule
import requests

class Xkcd(XMPPModule):
	
	def help(self, feature):
		return '''
Links to XKCD and stuff. Not very useful, really.

usage: !xkcd today
usage: !xkcd [number]
'''

	def handleMessage(self, msg):
		if msg['body'].split(' ')[0] == '!xkcd':
			string = ' '.join(msg['body'].split(' ')[1:])

			if string == 'today':
				r = requests.get("http://xkcd.com/info.0.json")
				if r.status_code == 200:
					reply = 'xkcd {0} - "{1}": {2}'.format(string, r.json()["title"], r.json()["img"])
				else:
					reply = "Could not find that one, does it even exist?"
				self.xmpp.reply(msg, reply)
			else:
				try:
					int(string)
				except:
					return

				r = requests.get("http://xkcd.com/{0}/info.0.json".format(string))
				if r.status_code == 200:
					reply = 'xkcd {0} - "{1}": {2}'.format(string, r.json()["title"], r.json()["img"])
				else:
					reply = "Could not find that one, does it even exist?"
				self.xmpp.reply(msg, reply)

