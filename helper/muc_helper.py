import subprocess as sp
import xmpp, urllib, urllib2

# api settings
API_URL = "https://hickerspace.org/api/muc/"
API_USER = "api-user"
API_PASSWORD = "APIKEY"

# jabber settings for status user
JABBER_SERVER = "hickerspace.org"
JABBER_USER = "JABBERUSER"
JABBER_PASSWORD = "JABBERPASSWORD"

# muc settings
JABBER_MUC = "hick"
JABBER_MUC_SERVER = "conference.hickerspace.org"

"""
Returns bot status and number of users online in our MUC.
"""
def determineStatus():
	result = { "mucUsers": 0, "botOnline": False }

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


passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, API_URL, API_USER, API_PASSWORD)
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
req = urllib2.Request(API_URL)
urllib2.urlopen(req, urllib.urlencode(determineStatus()))

