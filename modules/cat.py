from module import XMPPModule
import re, requests

regex = None

def cat(string):
	global regex

	if not regex:
		regex = re.compile('<img src="(.*)">')

	picformat = ""
	print(string)
	if string in ["gif", "jpg", "png"]:
		picformat = "&type=" + string

	r = requests.get("http://thecatapi.com/api/images/get?format=html" + picformat)
	print("http://thecatapi.com/api/images/get?format=html" + picformat)
	m = regex.search(r.text)

	if m:
		return m.group(1)
	else:
		print("Error extracting the image url!")
		return None

def catfacts(string):
	return requests.get("http://catfacts-api.appspot.com/api/facts").json()["facts"]

class Cat(XMPPModule):

	def handleMessage(self, msg):
		if msg['body'].split(" ")[0] in commands.keys():
			reply = commands[msg['body'].split(" ")[0]](" ".join(msg['body'].split(" ")[1:]))
		else:
			return

		if reply:
			self.xmpp.reply(msg, reply)

	def help(self, feature):
		if feature in ["!cat", "cat"]:
			return '''
Usage: !cat [jpg | png | gif]

Reply with a link to a cat picture. Provide any of the three optional arguments to specify the file type.
'''
		elif feature in ["!catfact", "catfact"]:
			return '''
Usage: !catfact

Reply with a random catfact. That is all.
'''
		return '''
Because all XMPP servers need cats!
 Features:
   !cat     - Display a link to a random cat picture
   !catfact - Print a random cat fact!
'''

commands = {
	"!cat":cat,
	"!catfact":catfacts
}
