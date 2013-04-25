Python (flask) implementation of our REST-API.

Overview
========

* room status (for SpaceAPI etc.)
* extended information about our hackspace
* audio announcement system via long polling
* LED ticker via long polling (see [ledticker](https://github.com/hickerspace/ledticker/))
* traffic light via long polling and normal request (see [traffic light](https://hickerspace.org/wiki/Verkehrsampel))
* Mate-O-Meter (measures our Club-Mate stock) (see [Mate-O-Meter](https://hickerspace.org/wiki/Mate-O-Meter))
* MUC (xmpp) status
* wiki status (just some redirects)

Dependencies
============

* flask
* gevent
* simplejson
* python-xmpp (see /helper)
* bash, espeak, sox, lame (see /data/espeak/espeak.sh)

Notes
=====
* enable [WSGIPassAuthorization](http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIPassAuthorization) to pass through authorisation headers:
* scripts in /helper update the API via http calls and must be called via cron or something similar (calls from other servers are supported)
