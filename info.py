import room

def info():
	message = {
		'api': '0.12',
		'space': 'Hickerspace',
		'url': 'https://hickerspace.org',
		'icon': {
					'open': 'https://hickerspace.org/images/open.png',
					'closed': 'https://hickerspace.org/images/closed.png'
				},
		'address': 'Kulturfabrik Loeseke (Projektwerkstatt), Langer Garten 1, 31137 Hildesheim, Germany',
		'contact': {
						'irc': 'irc://irc.freenode.net:6667/#hickerspace',
						'twitter': '@hickernews',
						'jabber': 'hick@conference.hickerspace.org',
						'email': 'kontakt@hickerspace.org',
						'ml': 'hickerspace@hickerspace.org'
					},
		'logo': 'https://hickerspace.org/images/hickerspace.png',
		'open': room.isRoomOpen(),
		'lastchange': room.getStatus()['since'],
		'lat': 52.16175,
		'lon': 9.957776,
		'feeds': [
					{
						'name': 'News via Twitter',
						'type': 'application/rss+xml',
						'url': 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=hickernews'
					},
					{	'name': 'New Wiki Articles',
						'type': 'application/rss+xml',
						'url': 'https://hickerspace.org/wiki/New.xml'
					},
					{	'name': 'Wiki Articles Updated Lately',
						'type': 'application/rss+xml',
						'url': 'https://hickerspace.org/wiki/Updated.xml'
					},
					{	'name': 'Wiki Articles in Userspace Updated Lately',
						'type': 'application/rss+xml',
						'url': 'https://hickerspace.org/wiki/Userspace.xml'
					},
					{	'name': 'Wiki Articles Discussed Lately',
						'type': 'application/rss+xml',
						'url': 'https://hickerspace.org/wiki/Discussion.xml'
					}
				]
		}
	return message
