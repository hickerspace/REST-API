from flask import Flask, url_for, request, jsonify
from auth import requires_auth
import logging

app = Flask(__name__)
file_handler = logging.FileHandler('hickerspace.org/wsgi-scripts/restapi/restapi.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def api_root():
	return 'Welcome to the Hickerspace REST API. See http://hickerspace.org/wiki/REST-API for documentation.'

@app.route('/info')
def api_info():
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
						'jabber': 'hick@conference.hickerspace.org'
					},
		'logo': 'https://hickerspace.org/images/hickerspace.png',
		'open': '$open',
		'lastchange': '$since',
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
	return jsonify(message)

@app.route('/articles/<articleid>')
@requires_auth
def api_article(articleid):
	return 'You are reading ' + articleid

if __name__ == '__main__':
	app.run()

