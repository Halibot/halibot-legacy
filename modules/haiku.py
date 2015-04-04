from module import XMPPModule

# rough count of number of syllables in a given word
def sylcnt(word):
	lastvowel = False
	syl = 0

	exceptions = {
		'maybe': 2,
		'something': 2,
		'sometimes': 2
	}

	if word in exceptions:
		return exceptions[word]

	# remove e, es from end of words
	if word[-1] == 'e':
		word = word[0:-1]
	elif word[-2:] == 'es':
		word = word[1:-2]

	for i in range(len(word)):
		c = word[i]
		vowel = (c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u' or c == 'y')
		if not lastvowel and vowel:
			syl += 1
		lastvowel = vowel

	if syl == 0:
		syl = 1
	return syl

# filters non-alphanumeric characters and lowercases everything
def clean(x):
	y = ''
	for i in range(len(x)):
		if x[i].isalpha():
			y += x[i]
	return y.lower()

# This function determines is a string can be split into lines deterministic of a given structure
# Returns false if it cannot be so, the stanza of poem if it can
def haiku(line, counts):
	words = filter(lambda w: len(w) > 0, line.split(' '))
	i = 0
	cnt = 0
	stanza = [[]]

	for w in words:
		if i >= len(counts):
			return False

		w = clean(w)

		if len(w) > 0:
			cnt += sylcnt(w)
			stanza[i].append(w)

			if cnt == counts[i]:
				i += 1
				cnt = 0
				stanza.append([])
			elif cnt > counts[i]:
				return False

	if i == len(counts):
		stanza.pop()
		return stanza
	return False

# makes a string from a stanza
def make_poem(stanza):
	formed = ''
	for line in stanza:
		first = True
		for word in line:
			if first:
				formed += word[0].upper() + word[1:]
				first = False
			else:
				formed += ' ' + word
		formed += '\n'
	return formed

class Haiku(XMPPModule):
	def init(self):
		if 'haiku' in self.xmpp.config.keys():
			self.forms = self.xmpp.config['haiku']['forms']
		else:
			self.forms = [{
				'name': 'haiku',
				'form': [5, 7, 5]
			}, {
				'name': 'tanka',
				'form': [5, 7, 5, 7, 7]
			}]

	def help(self, feature):
		if feature == 'sylcnt' or feature == '!syscnt':
			return '''
Counts syllables in words as a debug tool.

usage: !sylcnt [words...]
'''
		for p in self.forms:
			if feature == p['name']:
				return p['name'] + 's are of the form ' + ', '.join([str(i) for i in p['form']])
		s = '''
This module makes poems.
When your words are in poem form.
Quite many forms there are.

Debug subfeatures:
 sylcnt

Poems recognized ("!help haiku [form]" for more information):
'''
		s += '\n'.join([' ' + p['name'] for p in self.forms])
		return s + '\n'

	def handleMessage(self, msg):
		if msg['body'][0:8] == '!sylcnt ':
			words = msg['body'][8:].split(' ')
			reply = ''
			first = True
			for w in words:
				if first:
					first = False
				else:
					reply += '\n'
				w = clean(w)
				c = sylcnt(w)
				reply  += w + ': ' + str(c)
			self.xmpp.reply(msg, reply)
		else:
			for pair in self.forms:
				name = pair['name']
				form = pair['form']
				s = haiku(msg['body'], form)
				if s:
					reply = make_poem(s)
					reply = 'I proffer that your prose is a poem, a ' + name + ':\n' + reply
					self.xmpp.reply(msg, reply)
