from logger import log
from conf import *
from datetime import *
import time
import simplejson
from flask import jsonify

"""
Check if enough people are avaiable depending on weekday and time to mark the room as "open" or "closed".
This method can be called with datetime object or unix timestamp.
"""
def determineStatus(openingTime, people):
	if isinstance(openingTime, float) or isinstance(openingTime, (int, long)):
		openingTime = datetime.fromtimestamp(openingTime)

	status = openingTime > (datetime.now() - timedelta(minutes=ROOM_TIMEOUT))

	openNights = []
	for eventWeekday in EVENT_WEEKDAYS:
		openNights.append((openingTime.weekday() == eventWeekday and openingTime.hour >= MEET_HOUR_BEGIN) \
			or (openingTime.weekday() == eventWeekday + 1 and openingTime.hour <= MEET_HOUR_END))

	enoughPeople = (any(openNights) and people > EVENT_PEOPLE_LIMIT) or people >= PEOPLE_LIMIT

	return status and enoughPeople

"""
JSON output for /room.
"""
def getStatus():
	try:
		f = open(ROOM_STATUS_FILE, 'r')
		roomInternal = simplejson.loads(f.read())

		if determineStatus(roomInternal['lastOpenSignal'], roomInternal['people']):
			status = {	'roomStatus': 'open',
						'since': int(roomInternal["lastStatusSignal"]) }
		else:
			since = datetime.fromtimestamp(roomInternal["lastOpenSignal"]) + timedelta(minutes=ROOM_TIMEOUT)
			sinceInSecs = time.mktime(since.timetuple())

			status = {	'roomStatus': 'closed',
						'since': int(sinceInSecs) }

		return status

	except IOError:
		log.exception("Could not read %s." % ROOM_STATUS_FILE)
		message = { 'success': False, 'status': 'Room status record unreadable.' }
		resp = jsonify(message)
		resp.status_code = 500
		return resp
	else:
		f.close()

"""
Boolean return for room status.
"""
def isRoomOpen():
	try:
		f = open(ROOM_STATUS_FILE, 'r')
		roomInternal = simplejson.loads(f.read())

		if determineStatus(roomInternal['lastOpenSignal'], roomInternal['people']):
			return True
		else:
			return False
	except IOError:
		log.exception("Could not read %s." % ROOM_STATUS_FILE)
		message = { 'success': False, 'status': 'Room status record unreadable.' }
		resp = jsonify(message)
		resp.status_code = 500
		return resp
	else:
		f.close()


"""
Munin plugin data source. This returns only the number of people in the usual munin way.
"""
def getMuninStatus():
	try:
		f = open(ROOM_STATUS_FILE, 'r')
		roomInternal = simplejson.loads(f.read())

		if determineStatus(roomInternal['lastOpenSignal'], roomInternal['people']):
			people = int(roomInternal['people'])
		else:
			people = 0

		return 'room.value %d' % people

	except IOError:
		log.exception("Could not read %s." % ROOM_STATUS_FILE)
		return 'room.value 0'
	else:
		f.close()


"""
This method gets called when a new status gets submitted ("/submit-room")
"""
def submitStatus(people):
	if not determineStatus(datetime.now(), people):
		# people limit not reached, but thx anyway
		return jsonify({ 'success': True })

	try:
		with open(ROOM_STATUS_FILE, 'r') as f:
			roomInternal = simplejson.loads(f.read())

		with open(ROOM_STATUS_FILE, 'w') as f:

			if determineStatus(roomInternal['lastOpenSignal'], roomInternal['people']) != \
				determineStatus(datetime.now(), people):

				newStatus = {	'lastOpenSignal': time.time(),
								'lastStatusSignal': time.time(),
								'people': people }

				f.write(simplejson.dumps(newStatus))
			else:
				newStatus = {	'lastOpenSignal': time.time(),
								'lastStatusSignal': roomInternal['lastStatusSignal'],
								'people': people }

				f.write(simplejson.dumps(newStatus))

		return jsonify({ 'success': True })

	except IOError:
		log.exception("Could not read/write %s." % ROOM_STATUS_FILE)
		message = { 'success': False, 'status': 'Room status record unwriteable/unreadable.' }
		resp = jsonify(message)
		resp.status_code = 500
		return resp

