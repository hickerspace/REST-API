from flask import jsonify, send_from_directory
from logger import log
import os
import glob
import time
import ledticker, room
from conf import *
from subprocess import Popen, PIPE
from misc import error504

"""
Call a bash script which creates a mp3 with espeak content
and moves it into our restapi directory.
"""
def announce(lang, text):
	if not room.isRoomOpen():
		message = { 'success': False, 'status': 'Room is not open. Announcements are forbidden at the moment.' }
		resp = jsonify(message)
		resp.status_code = 403
	elif lang in ['de', 'en']:
		espeak = Popen([ESPEAK_LOCATION, lang, text], stdout=PIPE, stderr=PIPE)
		returnMsg = espeak.communicate()[0]
		if espeak.returncode > 0:
			log('espeak returned "%s"' % returnMsg)
			message = { 'success': False, 'status': 'Unknown error. Error logged.' }
		else:
			message = { 'success': True }

		resp = jsonify(message)
	else:
		message = { 'success': False, 'status': 'Language not found.' }
		resp = jsonify(message)
		resp.status_code = 403

	return resp

"""
When the mp3 announcement file is ready, call this method to deliver it.
"""
def serveAnnouncement(announcement):
	try:
		dlLocation = 'data/downloadable.mp3'
		os.rename(announcement, API_PATH+'/'+dlLocation)
		return send_from_directory(API_PATH, dlLocation, as_attachment=True)
	except OSError:
		log.exception('Could not move %s.' % announcement)
		message = { 'success': False, 'status': 'Announcement is not ready yet.' }
		resp = jsonify(message)
		resp.status_code = 403
		return resp

"""
Determine oldest announcement and return it.
"""
def serveOldestAnnouncement():
	# get mp3 announces sorted by creation time, oldest first
	mtime = lambda f: os.stat(f).st_mtime
	announces = list(sorted(glob.glob(ANNOUNCE_LOCATION), key=mtime))

	if len(announces) > 0:
		# return oldest announcement
		return serveAnnouncement(announces[0])
	else:
		return error504()

