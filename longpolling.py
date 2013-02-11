from flask import jsonify, send_from_directory
from logger import log
import os
import time
import ledticker
from conf import *

"""
Call a bash script which creates a mp3 with espeak content
and moves it into our restapi directory.
"""
def announce(lang, text):
	if lang in ['de', 'en']:
		os.system('bash %s/../../espeak/espeak_%s.sh \'%s\'' % (API_PATH, lang, text))
		message = {'status': 'Ok'}
		resp = jsonify(message)
	else:
		message = {'message': 'Language not found.'}
		resp = jsonify(message)
		resp.status_code = 403

	return resp

"""
When the mp3 announcement file is ready, call this method to deliver it.
"""
def serveAnnouncement():
	try:
		os.rename(API_PATH+'/'+ESPEAK_FILE, API_PATH+'/'+ANNOUNCE_DL)
		return send_from_directory(API_PATH, ANNOUNCE_DL, as_attachment=True)
	except OSError:
		log.exception('Could not move %s.' % ESPEAK_FILE)
		return jsonify({ 'status': 'Announcement is not ready yet.' })

"""
Use long polling to deliver different content to our router. This is
necessary due to our network situation: Incoming connections are not
possible, because of the inability to create port forwardings.
"""
def longPolling():
	ticker = ledticker.LedTicker(API_PATH + "/data/ledticker.txt")

	while not os.path.exists(API_PATH+'/'+ESPEAK_FILE) and ticker.items_available() == 0:
		time.sleep(1)

	if ticker.items_available() != 0:
		# return new ticker messages if available
		return ticker.get_output()

	elif os.path.exists(API_PATH+'/'+ESPEAK_FILE):
		# return new announcements (as mp3s) if available
		return serveAnnouncement()

