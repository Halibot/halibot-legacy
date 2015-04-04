from module import XMPPModule
from aspell import Speller
import re

class Spell(XMPPModule):

	priority = 40

	def init(self):
		spell = xmpp.config.get('spell')
		self.aggro = (spell and spell.get('aggro')) or False
		self.lang = (spell and spell.get('lang')) or 'en'

		self.rgx = re.compile(r"[^a-zA-Z']")
		self.speller = Speller('lang', self.lang)

	def ignore(self, msg, words):
		if len(words) > 1:
			for m in words:
				for w in self.rgx.split(m):
					self.speller.addtoSession(w)
			self.xmpp.reply(msg, 'These words are now a component of the descriptivist English language: ' + ', '.join(words[1:]))
		else:
			self.xmpp.reply(msg, 'Ah, good, I see you are a prescriptivist as well.')

	def correct(self, msg, words):
		for m in words:
			for w in self.rgx.split(m):
				if w.isalpha() and not self.speller.check(w):
					if (len(self.speller.suggest(w)) > 0):
						self.xmpp.reply(msg, "'" + w + "'? Did you mean '" + self.speller.suggest(w)[0] + "'?")

	def handleMessage(self, msg):
		words = msg['body'].split(' ')

		if words[0] == '!spellignore':
			self.ignore(msg, words[1:])
		elif words[0] == '!spellcheck':
			self.correct(msg, words[1:])
		elif self.aggro:
			self.correct(msg, words)

	def help(self, feature):
		if feature in ['spellignore', '!spellignore', 'ignore']:
			return '''
Tells the spell checker to ignore the given words as spelling errors.

usage: !spellignore [word1] [word2] ...
'''
		if feature in ['spellcheck', '!spellcheck', 'check']:
			return '''
Spell checks the given phrase.

usage: !spellcheck [word1] [word2] ...
'''
		if feature == 'lang':
			return '\nCurrent language in use: ' + self.lang + '\n'
		if self.aggro:
			s = '''
When a charlatan spels something incorrectly, correct them.'''
		else:
			s = '''
Corrects the spelling of those who request it.'''
		return s + '''
 Features:
  lang         - Information on the language that is being checked for.
  !spellignore - Inform the spell checker that it is wrong.
  !spellcheck  - Checks to see if a phrase is correct
'''
