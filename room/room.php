<?php
# helper functions for room status

include_once("{WWW-DIRECTORY}/api/conf.php");

# determine the status of our space
function isOpen($openTime, $people) {
	global $ROOM_TIMEOUT, $PEOPLE_LIMIT, $PEOPLE_LIMIT_FR;

	# mark as open if room timeout is not yet reached
	$open = ($openTime > (time() - $ROOM_TIMEOUT*60));

	# on friday evenings/saturday mornings, use special rule
	$fridayNights = ( date("N", $openTime) == 5 && date("G", $openTime) >= 18 ) || ( date("N", $openTime) == 6 && date("G", $openTime) <= 3 );
	$enoughPeople = ( ($fridayNights && $PEOPLE_LIMIT_FR) || $people >= $PEOPLE_LIMIT);

	return ($open && $enoughPeople);
}

# return current space status
function getStatus($bool = false) {
	global $ROOM_TIMEOUT;

	$statusInfo = getRoomInfo();

	if (isOpen($statusInfo["lastChangeSignal"], $statusInfo["people"])) {
		$open = true;
		$status = "open";
		$since = $statusInfo["lastStatusSignal"];
	} else {
		$open = false;
		$status = "closed";
		$since = $statusInfo["lastChangeSignal"] + $ROOM_TIMEOUT*60;
	}

	if ($bool) {
		return $open;
	} else {
		return array("roomStatus" => $status, "since" => $since);
	}
}

function getRoomInfo() {
	global $ROOM_STATUS_FILE;

	# retrieve room information
	$fp = fopen($ROOM_STATUS_FILE, "r");
	# timestamp of last change-signal
	$lastChangeSignal = intval(fgets($fp));
	# timestamp of next to last change-signal
	$lastStatusSignal = intval(fgets($fp));
	# people online (= active registered devices)
	$people = intval(fgets($fp));
	fclose($fp);

	return array("lastChangeSignal" => $lastChangeSignal, "lastStatusSignal" => $lastStatusSignal, "people" => $people);
}

function setRoomInfo($lastChangeSignal, $lastStatusSignal, $people) {
	global $ROOM_STATUS_FILE;

	$fp = fopen($ROOM_STATUS_FILE, "w");
	fputs($fp, $lastChangeSignal."\n".$lastStatusSignal."\n".$people);
	fclose($fp);

}
?>
