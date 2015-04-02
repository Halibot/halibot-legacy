from module import XMPPModule
import json

class Config(XMPPModule):

	def __init__(self, xmpp):
		XMPPModule.__init__(self, xmpp)
		if not 'modules' in self.xmpp.config:
			self.xmpp.config['modules'] = []

	def enable(self, mods):
		mods = list(set(mods).intersection(set(self.xmpp.modavail)))
		if len(mods) > 0:
			self.xmpp.config['modules'].extend(mods)
			return 'Enabled ' + ', '.join(mods)
		return 'Nothing has been changed.'

	def disable(self, mods):
		if len(mods) > 0:
			mods = list(filter(lambda m: m in self.xmpp.config['modules'], mods))
			self.xmpp.config['modules'] = list(filter(lambda m: not m in mods, self.xmpp.config['modules']))
			return 'Disabled ' + ', '.join([str(m) for m in mods])
		return 'Nothing has been changed.'

	def getvalue(self, path):
		t = p = self.xmpp.config

		# hack get for root
		if path == '/':
			return ({'foo': t}, 'foo')

		# normal get
		ks = filter(lambda k: len(k) > 0, path.split('/'))
		for k in ks:
			if not k in t:
				return (None, None)
			p = t
			t = t[k]
		return (p, k)

	def get(self, stuff):
		ms = []
		for p in stuff:
			t, k = self.getvalue(p)
			ms.append(p + ': ' + str(t[k] if t else '<not set>'))
		return '\n'.join(ms)

	def set(self, args):
		if len(args) < 1:
			return 'Set requires at least 1 argument'

		t, k = self.getvalue(args[0])
		if not t:
			return 'There is no such key within the config.'
		if len(args) == 1:
			t.pop(k, None)
		else:
			try:
				t[k] = json.loads(' '.join(args[1:]))
			except Exception as e:
				return str(e)

		return args[0] + ' set.'

	def handleMessage(self, msg):
		cmd,args = (msg['body'].split(" ",1)[0], msg['body'].split(" ")[1:])
		if cmd == "!config" and len(args) >= 1 and self.xmpp.isadmin(msg=msg):
			if args[0] == "enable":
				reply = self.enable(args[1:])
			elif args[0] == "disable":
				reply = self.disable(args[1:])
			elif args[0] == "write":
				try:
					self.xmpp.write_config()
					reply = "Wrote config successfully!"
				except:
					reply = "Error writing config :("
			elif args[0] == "reload":
				try:
					self.xmpp.load_config()
					reply = "Reloaded config successfully!"
				except:
					reply = "Error reloading config :("
			elif args[0] == "get":
				reply = self.get(args[1:])
			elif args[0] == 'set':
				reply = self.set(args[1:])
			else:
				reply = "I could not comprehend your query."
			self.xmpp.reply(msg, reply)

	def help(self, feature):
		if feature in ['enable', '!enable']:
			return '''
Enables halibot modules, does not reload the modules.

usage: !config enable [module1] [module2] ...
'''
		if feature in ['disable', '!disable']:
			return '''
Disables halibot modules, does not reload the modules.

usage: !config disable [module1] [module2] ...
'''
		if feature in ['get', '!get']:
			return '''
Gets keys in the halibot config.

usage: !config get [key path1] [key path2] ...
'''
		if feature in ['set', '!set']:
			return '''
Sets a key path to a value in the halibot config.

usage: !config set [path] [json value]
'''
		if feature in ['write', '!write']:
			return '''
Writes the halibot config from to file.

usage: !config reload
'''
		if feature in ['reload', '!reload']:
			return '''
Reloads the halibot config from file.

usage: !config reload
'''
		return '''
Provides an interactive interface to the halibot conifgurable config.
 Features:
  enable  - Enables halibot modules.
  disable - Disables halibot modules.
  get     - Gets values from the halibot config.
  set     - Sets a value for a halibot config key.
  write   - Writes the config to a file.
  reload  - Reloads the config to a file.
'''

