import os

# timeout per request in seconds (adjust WSGI/proxy timeout settings)
REQUEST_TIMEOUT = 120

# path to REST API files
API_PATH = os.path.abspath(os.path.dirname(__file__))

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
ROOM_STATUS_FILE = "%s/data/room.json" % API_PATH

# file to save MUC status in
MUC_FILE = "%s/data/muc.json" % API_PATH

# store traffic light info in this file
AMPEL_FILE = "%s/data/ampel.json" % API_PATH

# store mate info in this file
MATE_FILE = "%s/data/mate.json" % API_PATH

# stores ledticker messages
LEDTICKER_FILE = "%s/data/ledticker.txt" % API_PATH

# stores expanded twitter urls
EXPANDED_URLS = "%s/data/expanded_urls.json" % API_PATH

# location of the espeak script
ESPEAK_LOCATION = "%s/data/espeak/espeak.sh" % API_PATH

# temporary announce file location
ANNOUNCE_LOCATION = "%s/data/announces/*.mp3" % API_PATH

# jabber info for status user
JABBER_SERVER = "hickerspace.org"
JABBER_USER = "JABBERUSER"
JABBER_PASSWORD = "JABBERPASSWORD"

# muc info
JABBER_MUC = "hick"
JABBER_MUC_SERVER = "conference.hickerspace.org"

# twitter credentials
TWIT_CONSUMER_KEY = "CONSUMERKEY"
TWIT_CONSUMER_SECRET = "CONSUMERKEYSECRET"
TWIT_ACCESS_TOKEN = "ACCESSTOKEN"
TWIT_ACCESS_TOKEN_SECRET = "ACCESSTOKENSECRET"
