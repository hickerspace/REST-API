from gevent import monkey; monkey.patch_all()

from gevent.event import Event
from flask import Flask, request, jsonify, redirect, render_template, Response
from conf import *
from auth import requires_auth
from httpaccesscontrol import crossdomain
from misc import parameters_given, getParam, paramExists, isTrue, error405, error504, getStatus, setStatus
from logger import log
import info, room, ledticker, announce, twitterfeed
from os import stat
import datetime
from flask.ext.cache import Cache

app = Flask(__name__)
app.url_map.strict_slashes = False
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 10})

# events that get fired when new data is available
announceEvent = Event()
ampelEvent = Event()
ledtickerEvent = Event()

"""
Error handlers
"""
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

"""
API methods
"""
@app.route('/api')
def api_root():
	return render_template('welcome.html')

"""
Submit new audio announcements.
"""
@app.route('/api/announce', methods=['POST'])
@requires_auth()
@parameters_given(['lang', 'text'])
def api_announce():
	lang = getParam('lang')
	text = getParam('text')
	returnValue = announce.announce(lang, text)
	if returnValue.status_code == 200:
		announceEvent.set()
		announceEvent.clear()
	return returnValue

"""
Submit/get traffic light status information.
"""
@app.route('/api/ampel', methods=['GET', 'POST'])
@crossdomain(origin='*')
@requires_auth(True)
@parameters_given(['red', 'yellow', 'green'])
def api_ampel():
	if request.method == 'GET':
		return jsonify(getStatus(AMPEL_FILE))

	elif request.method == 'POST':
		try:
			# convert lights to boolean
			red = isTrue(getParam('red'))
			yellow = isTrue(getParam('yellow'))
			green = isTrue(getParam('green'))
			mode = getParam('mode') if paramExists('mode') else 'custom'

			if mode == 'random':
				red, yellow, green = True, True, True

			status = { 'red': red, 'yellow': yellow, 'green': green, 'mode': mode }

			returnValue = setStatus(AMPEL_FILE, status)
			ampelEvent.set()
			ampelEvent.clear()
			return jsonify(returnValue)
		except TypeError:
			message = { 'success': False, 'status': 'Please provide boolean \
				values (true, 1, false, 0) for red, yellow and green.' }
			resp = jsonify(message)
			resp.status_code = 500
			return resp

"""
Submit/get Mate-O-Meter status information.
"""
@app.route('/api/mate-o-meter', methods=['GET', 'POST'])
@crossdomain(origin='*')
@requires_auth(True)
@parameters_given(['bottles'])
def api_mateometer():
	if request.method == 'GET':
		return jsonify(getStatus(MATE_FILE))
	elif request.method == 'POST':
		try:
			bottles = int(getParam('bottles'))
			if bottles > 0 and bottles < 20:
				status = { 'bottles': bottles }
				returnValue = setStatus(MATE_FILE, status)
				return jsonify(returnValue)
			else:
				raise ValueError("Botte value not in allowed range (0-20).")
		except ValueError:
			message = { 'success': False, 'status': 'Please provide bottles attribute (0-20).' }
			resp = jsonify(message)
			resp.status_code = 500
			return resp


"""
Long polling method for audio announcements (private method).
"""
@app.route('/api/poll/announce')
@requires_auth()
def api_poll_announce():
	announceEvent.wait(REQUEST_TIMEOUT)
	return announce.serveOldestAnnouncement()

"""
Long polling method for ledticker updates (private method).
"""
@app.route('/api/poll/ledticker')
@requires_auth()
def api_poll_ledticker():
	ticker = ledticker.LedTicker(LEDTICKER_FILE)
	flag = False
	while not ticker.items_available():
		flag = ledtickerEvent.wait(REQUEST_TIMEOUT)

		if not flag:
			return error504()

	return ticker.get_output()

"""
Long polling method for traffic light updates.
"""
@app.route('/api/poll/ampel')
@crossdomain(origin='*')
def api_poll_ampel():
	flag = ampelEvent.wait(REQUEST_TIMEOUT)
	if not flag:
		return error504()
	return jsonify(getStatus(AMPEL_FILE))

"""
Submit ledticker updates and convert text messages to ledticker messages.
"""
@app.route('/api/ledticker', methods=['POST'])
@requires_auth()
@parameters_given(['text'])
def api_ledticker():
	"""
	if request.method == 'GET':
		text = request.args.get('text', '')
		ticker = ledticker.LedTicker()
		ticker.add_item(text)
		return ticker.get_output()

	if request.method == 'POST':
	"""

	text = getParam('text')
	lowPriority = isTrue(getParam('lowpriority')) if paramExists('lowpriority') else False

	ticker = ledticker.LedTicker(LEDTICKER_FILE)

	longAgo = False
	if lowPriority:
		mtime = stat(LEDTICKER_FILE).st_mtime
		longAgo = (datetime.datetime.fromtimestamp(mtime) + datetime.timedelta(seconds=30)) < datetime.datetime.now()

	if not lowPriority or (lowPriority and ticker.items_available() == 0 and longAgo):
		if not lowPriority:
			log.info("Received high priority message: %s" % text)
		ticker.add_item(text)
		ledtickerEvent.set()
		ledtickerEvent.clear()
	return jsonify({ 'success': True })

"""
Submit/get room status information.
"""
@app.route('/api/room', methods=['GET', 'POST'])
@parameters_given(['people'])
@crossdomain(origin='*')
@requires_auth(True)
def api_room():
	if request.method == 'POST':
		people = getParam('people')
		return room.submitStatus(people)
	elif request.method == 'GET':
		return jsonify(room.getStatus())

"""
Get general information + room status.
"""
@app.route('/api/room_extended')
@app.route('/api/info')
@crossdomain(origin='*')
def api_info():
	return jsonify(info.info())

"""
Get XMPP multi-user chat status info.
"""
@app.route('/api/muc', methods=['GET', 'POST'])
@parameters_given(['botOnline', 'mucUsers'])
@crossdomain(origin='*')
@requires_auth(True)
def api_muc():
	if request.method == 'GET':
		return jsonify(getStatus(MUC_FILE))
	elif request.method == 'POST':
		botOnline = isTrue(getParam('botOnline'))
		mucUsers = int(getParam('mucUsers'))
		status = { 'botOnline': botOnline, 'mucUsers': mucUsers }
		return jsonify(setStatus(MUC_FILE, status))

"""
Hickernews Twitter atom feed.
"""
@app.route('/api/twitter/hickernews.atom')
@cache.cached(timeout=300)
def api_hickernews_feed():
	return twitterfeed.getUserTimeline("Hickernews", request.url)

"""
Hickerspace Twitter atom feed.
"""
@app.route('/api/twitter/hickerspace.atom')
@cache.cached(timeout=300)
def api_hickerspace_feed():
	return twitterfeed.getUserTimeline("Hickerspace", request.url)


"""
Wiki resources which should be available also via this API
"""
@app.route('/api/wiki/new')
@crossdomain(origin='*')
def api_wiki_new():
	return redirect('http://hickerspace.org/wiki/New.json')

@app.route('/api/wiki/userspace')
@crossdomain(origin='*')
def api_wiki_userspace():
	return redirect('http://hickerspace.org/wiki/Userspace.json')

@app.route('/api/wiki/updated')
@crossdomain(origin='*')
def api_wiki_updated():
	return redirect('http://hickerspace.org/wiki/Updated.json')

"""
Server for testing purposes.
"""
if __name__ == '__main__':
	from gevent import pywsgi
	import sys
	pywsgi.WSGIServer(('', 8000), log=sys.stdout).serve_forever()
