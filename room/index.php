<?php
include_once("{WWW-DIRECTORY}/api/conf.php");
include("room.php");

header("Content-Type: application/json");

$people = intval($_POST["people"]);

# POST REQUEST - set Status
if (count($_POST) > 0) {

	# no API key
	if (!isset($_POST["apikey"])) {
		$returnArr = array("success" => false, "reason" => "Please provide API key.");

	# people online missing
	} else if (!isset($people)) {
		$returnArr = array("success" => false, "reason" => "Please provide number of people online.");

	# API key is incorrect
	} else if (!isAuthd($_POST["apikey"])) {
		trigger_error($_SERVER["REMOTE_ADDR"]." tried to submit an roomstatus update with API key '".$_POST["apikey"]."'");
		$returnArr = array("success" => false, "reason" => "Please provide *correct* API key.");

	# everything ok
	} else if (isOpen(time(), $people)) {

		$statusInfo = getRoomInfo();

		# status changed since last run?
		if (isOpen($statusInfo["lastChangeSignal"], $statusInfo["people"]) != isOpen(time(), $people)) {
			# set last change signal as well as last status signal
			setRoomInfo(time(), time(), $people);
		} else {
			# set last change signal and leave last status signal alone
			setRoomInfo(time(), $statusInfo["lastStatusSignal"], $people);
		}

		$returnArr = array("success" => true);

	} else {
		# people limit not reached, but thx anyway
		$returnArr = array("success" => true);

	}

	echo json_encode($returnArr);
	
} else { # GET REQUEST - get Status

	echo json_encode(getStatus());
}
?>
