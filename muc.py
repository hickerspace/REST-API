import subprocess as sp
import xmpp
from conf import *

"""
Returns bot status and number of users online in our MUC.
"""
def mucStatus():
	result = { 'mucUsers' : 0, 'botOnline' : False }

	# connect to jabber server
	con = xmpp.Client(JABBER_SERVER)
	con.connect()
	if con.auth(JABBER_USER, JABBER_PASSWORD, 'default'):
		# discover rooms and users
		infos = xmpp.features.discoverItems(con, JABBER_MUC_SERVER)
		for info in infos:
			if '%s (' % JABBER_MUC in info['name']:
				mucUsers = int(info['name'].replace('%s (' % JABBER_MUC, '').replace(')', ''))
		result['mucUsers'] = mucUsers

	# check bot activity via ps command
	ps = sp.Popen(['ps', '-A', 'x'], stdout=sp.PIPE, stderr=sp.PIPE)
	for line in ps.communicate():
		if 'whistler-1.1/start.sh' in line and result['mucUsers'] > 0:
			result['botOnline'] = True
			result['mucUsers'] = result['mucUsers'] - 1

	return result
