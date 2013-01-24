<?php
include_once("{WWW-DIRECTORY}/api/conf.php");
include("../room/room.php");

$normalStatus = getStatus();

$open = getStatus(true);

# SpaceAPI rel0.12 (see specs at https://hackerspaces.nl/spaceapi/)
$extendedStatus = array("api" => "0.12",
												"space" => "Hickerspace",
												"url" => "https://hickerspace.org",
												"icon" => array("open" => "https://hickerspace.org/images/open.png",
																				"closed" => "https://hickerspace.org/images/closed.png"),
												"address" => "Kulturfabrik Loeseke (Projektwerkstatt), Langer Garten 1, 31137 Hildesheim, Germany",
												"contact" => array(			"irc" => "irc://irc.freenode.net:6667/#hickerspace",
																								"twitter" => "@hickernews",
																								"jabber" => "hick@conference.hickerspace.org"),
												"logo" => "https://hickerspace.org/images/hickerspace.png",
												"open" => $open,
												"lastchange" => $normalStatus["since"],
												"lat" => 52.16175,
												"lon" => 9.957776,
												"feeds" => array(
																				array(	"name" => "News via Twitter",
																								"type" => "application/rss+xml",
																								"url" => "https://twitter.com/statuses/user_timeline/hickernews.rss"),
																				array(	"name" => "New Wiki Articles",
																								"type" => "application/rss+xml",
																								"url" => "https://hickerspace.org/wiki/New.xml"),
																				array(	"name" => "Wiki Articles updated lately",
																								"type" => "application/rss+xml",
																								"url" => "https://hickerspace.org/wiki/Updated.xml"),
																				array(	"name" => "Wiki Articles updated lately in Userspace",
																								"type" => "application/rss+xml",
																								"url" => "https://hickerspace.org/wiki/Userspace.xml"),
																				array(	"name" => "Wiki Articles discussed lately",
																								"type" => "application/rss+xml",
																								"url" => "https://hickerspace.org/wiki/Discussion.xml")));

header("Content-Type: application/json");
echo json_encode($extendedStatus);

?>
