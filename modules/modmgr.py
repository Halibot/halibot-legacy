import urllib, os, os.path
from module import XMPPModule
from halutils import splitArgList

# This function does the actual installation of a module
def install(mod):
    # If the string is just alphanumeric, consider the module to be in halibot-modules
    if url.isalnum():
        url = 'https://github.com/richteer/halibot-modules/blob/master/' + url + '.py'
    filename = 'modules/' + os.path.basename(url)

    try:
        urllib.urlretrieve(url, filename)
    except IOError:
        return False

    return True

# The function removes a module
def remove(mod):
    if not mod.isalnum:
        return False

    try:
        os.remove('modules/' + mod + '.py')
    except OSError:
        return False

    return True

# The module manager class
class ModMgr(XMPPModule):

    # A generic output function for the install/remove commands
    def showResults(self, how, ls, good, msg):
        bad = list(set(ls) - set(goof))

        if len(good) + len(bad) > 0:
            if len(good) > 0:
                self.xmpp.reply(msg, 'Successfully ' + how + 'ed: ' + ', '.join(good))
            if len(bad) > 0:
                self.xmpp.reply(msg, 'Failed to ' + how + ': ' + ', '.join(good))
        else:
            self.xmpp.reply(msg, 'You need to tell me what you want me to ' + how)

    def installList(self, ls, msg):
        good = filter(self.install, ls)
        self.showResults('install', ls, good, msg)

    def removeList(self, ls, msg):
        good = filter(self.remove, ls)
        self.showResults('remove', ls, good, msg)

    def listAll(self):
        self.xmpp.reply(msg,
                ', '.join(map(
                    lambda p: os.path.splitext(p)[0],
                    os.listdir('modules')
                ))
        )

    def handleMessage(self, msg):
        cmd, args = splitArgList(msg)

        if cmd == '!module':
            subcmd = args.pop(0)

            # install and remove require admin access
            if subcmd == 'install':
                if self.xmpp.isadmin(msg=msg):
                    self.installList(args, msg)
            elif subcmd == 'remove':
                if self.xmpp.isadmin(msg=msg):
                    self.removeList(args, msg)
            elif subcmd == 'list':
                self.listAll()
            else:
                self.xmpp.reply(msg, 'Unknown module subcommand "' + subcmd +'"')

    # The help function
    def help(self, feature):
        return {
            None: '''
The module manager allows the installation and removal of modules.
  Features:
    !module install <module-name|web-address>
    !module remove <module-name>
    !module list
''',
            'install': '''
Installs modules found in haibot-modules or from a web address.
  Usage: !module install <module-name|web-address> ...
''',
            'remove': '''
Removes modules of the given names.
  Usage: !module remove <module-name> ...
''',
            'list': '''
Lists all currently installed (not necessarily enabled) modules.
'''
        }[feature]
