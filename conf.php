<?php
# API LOCATION
$API_LOCATION = "http://hickerspace.org/api/";

# API Key
$API_KEY = "";

# room status file
$ROOM_STATUS_FILE = "{WWW-DIRECTORY}/api/room/room_status.txt";

# timeout in minutes when to mark room closed (after last "open message")
$ROOM_TIMEOUT = 20;

# people limit for status "open"
$PEOPLE_LIMIT = 3;

# lower people limit for status "open" on fridays after 19.00
$PEOPLE_LIMIT_FR = 1;

# FUNCTIONS
function isHttps() {
	return isset($_SERVER["HTTPS"]);
}

function isAuthd($apikey) {
	global $API_KEY;
	return ($apikey == $API_KEY);
}
?>
