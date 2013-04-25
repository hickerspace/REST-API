import room

def info():
	roomIsOpen = room.isRoomOpen()
	message = {
		'api': '0.12',
		'space': 'Hickerspace',
		'url': 'https://hickerspace.org',
		'icon': {
			'open': 'https://hickerspace.org/images/open.png',
			'closed': 'https://hickerspace.org/images/closed.png'
		},
		'address': 'Kulturfabrik Loeseke (Projektwerkstatt), Langer Garten 1, 31137 Hildesheim, Germany',
		'lat': 52.16175,
		'lon': 9.957776,
		'contact': {
			'irc': 'irc://irc.freenode.net:6667/#hickerspace',
			'twitter': '@hickernews',
			'jabber': 'hick@conference.hickerspace.org',
			'email': 'kontakt@hickerspace.org',
			'ml': 'hickerspace@hickerspace.org'
		},
		'logo': 'https://hickerspace.org/images/hickerspace.png',
		'status': infoMessage(roomIsOpen),
		'lastchange': room.getStatus()['since'],
		'open': roomIsOpen,
		'icon': {
			'open': 'https://hickerspace.org/images/open.png',
			'closed': 'https://hickerspace.org/images/closed.png'
		},
		'feeds': [
			{
				'name': 'News via Twitter',
				'type': 'application/rss+xml',
				'url': 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=hickernews'
			},
			{
				'name': 'New Wiki Articles',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/New.xml'
			},
			{
				'name': 'Wiki Articles Updated Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Updated.xml'
			},
			{
				'name': 'Wiki Articles in Userspace Updated Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Userspace.xml'
			},
			{
				'name': 'Wiki Articles Discussed Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Discussion.xml'
			},
			{
				'name': 'Event Calendar',
				'type': 'text/calendar',
				'url': 'https://hickerspace.org/wiki/Spezial:Semantische_Suche/-5B-5BTermin:%2B-5D-5D/-3FVollerTitel%3Dsummary/-3FDatum%3Dstart/-3FEnddate%3Dend/format%3Dicalendar/limit%3D200/searchlabel%3DKalender-20abonnieren-20(iCalendar-2DFormat)/offset%3D0'
			}
		]
	}
	return message



def info_0_13_draft():
	roomIsOpen = room.isRoomOpen()
	message = {
		'api': '0.13',
		'space': 'Hickerspace',
		'url': 'https://hickerspace.org',
		'icon': {
			'open': 'https://hickerspace.org/images/open.png',
			'closed': 'https://hickerspace.org/images/closed.png'
		},
		'location': {
			'address': 'Kulturfabrik Loeseke (Projektwerkstatt), Langer Garten 1, 31137 Hildesheim, Germany',
			'lat': 52.16175,
			'lon': 9.957776
		},
		'contact': {
			'irc': 'irc://irc.freenode.net:6667/#hickerspace',
			'twitter': '@hickernews',
			'jabber': 'hick@conference.hickerspace.org',
			'email': 'kontakt@hickerspace.org',
			'ml': 'hickerspace@hickerspace.org'
		},
		'logo': 'https://hickerspace.org/images/hickerspace.png',
		'status': {
			'open': roomIsOpen,
			'lastchange': room.getStatus()['since'],
			'message': infoMessage(roomIsOpen),
			'icon': {
				'open': 'https://hickerspace.org/images/open.png',
				'closed': 'https://hickerspace.org/images/closed.png'
			}
		},
		'feeds': [
			{
				'name': 'News via Twitter',
				'type': 'application/rss+xml',
				'url': 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=hickernews'
			},
			{
				'name': 'New Wiki Articles',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/New.xml'
			},
			{
				'name': 'Wiki Articles Updated Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Updated.xml'
			},
			{
				'name': 'Wiki Articles in Userspace Updated Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Userspace.xml'
			},
			{
				'name': 'Wiki Articles Discussed Lately',
				'type': 'application/rss+xml',
				'url': 'https://hickerspace.org/wiki/Discussion.xml'
			}
		]
	}
	return message




def infoMessage(roomIsOpen):
	return 'Open for public!' if roomIsOpen else 'We\'re closed.'

