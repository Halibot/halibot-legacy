from module import XMPPModule
from aspell import Speller

class Spell(XMPPModule):
	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)

		self.lang = xmpp.config['spell']['lang'] if 'spell' in xmpp.config else 'en'
		self.speller = Speller('lang', self.lang)

	def help(self, feature):
		if feature in ['spellignore', '!spellignore']:
			return '''
Tells the spell checker to ignore the given words as spelling errors.

usage: !spellignore [word1] [word2] ...
'''
		if feature == 'lang':
			return '\nCurrent language in use: ' + self.lang + '\n'
		return '''
When a charlatan spels something incorrectly, correct them.

 Features:
  spellignore - Inform the spell checker that it is wrong.
  lang        - Information on the language checked.
'''

	def handleMessage(self, msg):
		words = msg['body'].split(' ')

		if words[0] == '!spellignore':
			if len(words) > 1:
				for w in words[1:]:
					self.speller.addtoSession(w)
				self.xmpp.reply(msg, 'These words are now a component of the descriptivist English language: ' + ', '.join(words[1:]))
		elif len(words[0]) == 0 or words[0][0] != '!':
			for w in words:
				if w.isalpha() and not self.speller.check(w):
					if (len(self.speller.suggest(w)) > 0):
						self.xmpp.reply(msg, "'" + w + "'? Did you mean '" + self.speller.suggest(w)[0] + "'?")

