# path to REST API files
API_PATH = "/home/user/restapi"
# access tuples
API_ACCESS = [ ("api-user", "APIKEY") ]
# after this number of minutes, the room will be automatically marked as "closed"
ROOM_TIMEOUT = 15
# weekdays with events
EVENT_WEEKDAYS = [3, 4]
# begin of meeting
MEET_HOUR_BEGIN = 18
# end of meeting
MEET_HOUR_END = 2
# people needed to open the room on events
EVENT_PEOPLE_LIMIT = 1
# people needed to open the room on normal days
PEOPLE_LIMIT = 3
# file to save room status in
ROOM_STATUS_FILE = API_PATH + "/data/room_status.json"
