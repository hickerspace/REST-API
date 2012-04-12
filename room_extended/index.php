<?php
# this is the legacy redirection (listed in hackerspaces.nl's SpaceAPI)

$protocol = isHttps() ? "https" : "http";
$host  = $_SERVER["HTTP_HOST"];

// get parent directory of parent directory
$uri   = rtrim(dirname(dirname($_SERVER['PHP_SELF'])), '/\\');

# RFC 2616 requires absolute URIs
header("HTTP/1.1 301 Moved Permanently");
header("Location: $protocol://$host$uri/info/");
?>
